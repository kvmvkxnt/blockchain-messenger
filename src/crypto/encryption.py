"""
This module represents message encryption / decryption.\
In project dh shared key will be used with this module \
to encrypt / decrypt messages.
"""

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


class SymmetricEncryption:
    """
    Encryption class

    :ivar key: key that will be used to encrypt message
    :type key: bytes
    """

    def __init__(self, key: bytes) -> None:
        '''
        Initializes with the given key

        :param key: DH public key
        :type key: bytes
        '''

        self.key = key

    def encrypt(self, plaintext: str) -> bytes:
        '''
        Encrypts message with given shared key

        :param plaintext: Text that needs to be encrypted
        :type plaintext: str
        :return: encrypted message
        :rtype: bytes
        '''

        iv = os.urandom(16)  # Random initialization vector
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv),
                        backend=default_backend())
        encryptor = cipher.encryptor()

        # Padding before data ciphering
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padder_data = padder.update(plaintext.encode()) + padder.finalize()

        # Data ciphering
        ciphertext = encryptor.update(padder_data) + encryptor.finalize()
        return iv + ciphertext

    def decrypt(self, ciphertext: bytes) -> str:
        '''
        Decrypts message with given shared key

        :param ciphertext: Encrypted message that needs to be decrypted
        :type ciphertext: bytes
        :return: Decrypted message
        :rtype: str
        '''

        iv = ciphertext[:16]  # Ectracting initialization vector
        actual_ciphertext = ciphertext[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv),
                        backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypting data
        padded_data = decryptor.update(actual_ciphertext) \
            + decryptor.finalize()

        # Padding deletion
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
        return plaintext.decode()
