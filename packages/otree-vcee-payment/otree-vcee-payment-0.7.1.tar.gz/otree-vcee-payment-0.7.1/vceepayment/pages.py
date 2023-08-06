import csv

from schwifty import BIC, IBAN, exceptions

from ._builtin import Page, WaitPage
from .encryption import encrypt_payment_data
from .models import output_col_names

replacements = {
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "ß": "ss",
    "Ä": "Ae",
    "Ö": "Oe",
    "Ü": "Ue",
}


def clean_up(payment_data: dict):
    """Remove obvious mistakes from the payment data.

    Only mistakes where the replacement is clear and it does not need to be send back to the user."""
    for key in payment_data:
        payment_data[key] = (
            payment_data[key].replace(",", " ").replace("  ", " ").strip()
        )
    payment_data["iban"] = (
        payment_data["iban"].upper().replace(" ", "").replace(".", "")
    )
    payment_data["bic"] = payment_data["bic"].upper().replace(" ", "").replace(".", "")
    for key in replacements.keys():
        payment_data["full_name"] = payment_data["full_name"].replace(
            key, replacements[key]
        )
    return payment_data


def sort_and_clean_data(post_data):
    payment_data = {col: post_data[col] for col in output_col_names}
    payment_data = clean_up(payment_data)
    return payment_data


class WaitingForOthers(WaitPage):
    def is_displayed(self):
        return not self.session.config["disable_waiting_for_others"]


class PaymentInfos(Page):
    def vars_for_template(self):
        return {
            "final_payoff": self.participant.payoff_plus_participation_fee(),
            "saved": self.participant.vars["temp_values"],
        }

    def error_message(self, value):
        payment_data = sort_and_clean_data(self.request.POST)
        self.participant.vars[
            "temp_values"
        ] = payment_data  # temp saves them, removed in before_next_page

        name = payment_data["full_name"].split()
        if len(name) < 2:
            return "Please enter first and last name."
        for name_part in name:
            if not name_part.isascii() or not name_part.isalpha():
                return "Please only use the standard latin alphabet."

        try:
            iban = IBAN(payment_data["iban"])
        except exceptions.SchwiftyException as error:
            return error
        if iban.country_code not in ["AT", "DE"]:
            try:
                BIC(payment_data["bic"])
            except exceptions.SchwiftyException as error:
                return error

    def before_next_page(self):
        payment_data = sort_and_clean_data(self.request.POST)
        self.participant.vars[
            "temp_values"
        ].clear()  # removes temp saved iban/name, etc
        # transforming to int as is otherwise in c(), which might cause problems when encrypting/saving
        # amount * 100 to prevent floating problems
        payment_data["amount"] = int(
            self.participant.payoff_plus_participation_fee() * 100
        )
        if self.session.config["encrypt_payment_file"]:
            payment_data = encrypt_payment_data(payment_data)
        with open("payment_info.csv", "a") as output_file:
            csv.DictWriter(output_file, fieldnames=payment_data.keys()).writerow(
                payment_data
            )
            output_file.close()


class ConfirmationPage(Page):
    pass


page_sequence = [WaitingForOthers, PaymentInfos, ConfirmationPage]
