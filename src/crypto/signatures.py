'''This module handles digital signatures'''

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    Encoding,
    PrivateFormat,
    NoEncryption,
    PublicFormat
)


class DigitalSignature:
    '''
    Signatures, key generation

    :ivar private_key: Sender's RSA private key
    :type private_key: bytes
    :ivar public_key: Sender's RSA public_key
    :type public_key: bytes
    '''

    def __init__(self):
        """Generating RSA key pair"""

        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def get_private_key(self) -> bytes:
        '''
        Returns private key in PEM format

        :return: Private key in PEM format
        :rtype: bytes
        '''
        return self.private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption()
        )

    def get_public_key(self) -> bytes:
        '''
        Returns public key in PEM format

        :return: Public key in PEM format
        :rtype: bytes
        '''
        return self.public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        )

    def sign(self, message: bytes) -> bytes:
        '''
        Creates messages's digital signature

        :param message: Message to be signed
        :type message: bytes
        :return: Signature of the message
        :rtype: bytes
        '''
        return self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    @staticmethod
    def verify(public_key_pem: bytes, message: bytes, signature: bytes) \
            -> bool:
        '''
        Verifys digital signature of the message

        :param public_key_pem: Signer's public key
        :type public_key_pem: bytes
        :param message: Encrypted message
        :type message: bytes
        :param signature: Signature to be verified
        :type signature: bytes
        :return: If signature is valid or not
        :rtype: bool
        '''
        public_key = load_pem_public_key(public_key_pem)
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Verification failed: {e}")
            return False
