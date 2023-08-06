from itertools import product

from otree.api import Submission, SubmissionMustFail

from . import pages
from ._builtin import Bot

correct_names = [
    "Detlef Mueller",
    "Detlef Müller",
    "Detlef Hans Dieter Müller",
    " Detlef Hans Dieter Müller  ",
]


incorrect_names = ["ichnureinennamenhaben", "Chloé IsNotAllowed", "陈玉"]

# Combination iban + bic
correct_iban_bic = [
    ["DE40100100100000012345", ""],
    ["DE75512108001245126199", ""],
    ["de75512108001245126199", ""],
    ["de 75 512 108 001 245  126199", ""],
    ["DE75512108001245126199", "-"],
    ["DE75512108001245126199", "nix"],
    ["GR1601101250000000012300695", "ETHNGRAA"],
    ["GB33BUKB20201555555555", "BUKBGB22"],
    ["FR7630006000011234567890189", "AGRIFRPP"],
    ["AT611904300234573201", "GIBAATWW"],
    ["AT611904300234573201", ""],
]

incorrect_iban_bic = [
    ["DE40100100100000012346", ""],
    ["GR1601101250000000012300695", ""],
    ["GB33BUKB20201555555555", ""],
    ["FR7630006000011234567890189", ""],
    ["AT6119043002345732012", "GIBAATWW"],
    ["AT61190430023453201", "GIBAATWW"],
]

all_good_cases = product(correct_names, correct_iban_bic)
all_bad_cases_1 = product(correct_names, incorrect_iban_bic)
all_bad_cases_2 = product(incorrect_names, correct_iban_bic)
all_very_bad_cases = product(incorrect_names, incorrect_iban_bic)


all_good_cases_dict = [
    {"full_name": entry[0], "iban": entry[1][0], "bic": entry[1][1], "is_correct": True}
    for entry in all_good_cases
]

all_bad_cases_dict_1 = [
    {
        "full_name": entry[0],
        "iban": entry[1][0],
        "bic": entry[1][1],
        "is_correct": False,
    }
    for entry in all_bad_cases_1
]

all_bad_cases_dict_2 = [
    {
        "full_name": entry[0],
        "iban": entry[1][0],
        "bic": entry[1][1],
        "is_correct": False,
    }
    for entry in all_bad_cases_2
]

all_very_bad_cases_dict = [
    {
        "full_name": entry[0],
        "iban": entry[1][0],
        "bic": entry[1][1],
        "is_correct": False,
    }
    for entry in all_very_bad_cases
]

all_cases = (
    all_good_cases_dict
    + all_bad_cases_dict_1
    + all_bad_cases_dict_2
    + all_very_bad_cases_dict
)


class PlayerBot(Bot):

    cases = all_cases

    def play_round(self):
        if self.case["is_correct"]:
            yield Submission(pages.PaymentInfos, self.case, check_html=False)
        else:
            yield SubmissionMustFail(pages.PaymentInfos, self.case, check_html=False)
