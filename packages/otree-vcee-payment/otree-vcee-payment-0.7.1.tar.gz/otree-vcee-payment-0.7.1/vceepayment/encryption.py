import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

# Generates a private/public key pair, using rsa with key size 4096
# key_size of 4096 is such an overkill
# But given that we are not encrypting much, it shouldn't matter
# public_exponent: commonly used one,


def generate_key_pair():
    """ Create private/public key pair and saves them. """
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=4096, backend=default_backend()
    )
    public_key = private_key.public_key()

    # Saving the private key
    serial_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    with open("../private_noshare.pem", "wb") as f:
        f.write(serial_private)

    # Saving the public key
    serial_pub = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open("../public_shared.pem", "wb") as f:
        f.write(serial_pub)


def read_public_key(filename="public_shared.pem"):
    with open("public_shared.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(), backend=default_backend()
        )
    return public_key


def encrypt_payment_data(payment_data: dict):
    """Encrypt the payment data.
    dict of payment data -> dict of encrypted payment data"""
    public_key = read_public_key()
    for key in payment_data.keys():
        entry = bytes(str(payment_data[key]), "utf-8")
        encrypted_entry = public_key.encrypt(
            entry,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        payment_data[key] = base64.standard_b64encode(encrypted_entry)
    return payment_data
