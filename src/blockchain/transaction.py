'''This module contains transaction handler'''

import json5 as json
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, dh
from typing import Dict
from utils.logger import Logger
from crypto.signatures.DigitalSignature import verify

log = Logger("transactions")


class Transaction:
    '''
    This class creates transactions and contains its functions

    :ivar sender: Sender public DH key
    :type sender: bytes or None
    :ivar recipient: Recipient public DH key
    :type recipient: bytes
    :ivar amount: Amount of currency being sent to recipient
    :type amount: float
    :ivar content: Message being sent to recipient
    :type content: bytes or None
    :ivar sender_rsa_public_key: Sender's RSA public key used to sign the \
    transaction
    :type sender_rsa_public_key: bytes or None
    :ivar signature: Sender's signature
    :type signature: bytes or None
    :ivar timestamp: The time transaction was created
    :type timestamp: float
    '''

    def __init__(self,
                 sender: dh.DHPublicKey,
                 recipient: dh.DHPublicKey,
                 amount: float,
                 content: bytes,
                 sender_rsa_public_key: rsa.RSAPublicKey,
                 signature: bytes,
                 timestamp: float
                 ) -> None:
        '''
        Initializes a new transaction instance.

        :param sender: Sender public DH key
        :type sender: bytes or None
        :param recipient: Recipient public DH key
        :type recipient: bytes
        :param amount: Amount of currency being sent to recipient
        :type amount: float
        :param content: Message being sent to recipient
        :type content: bytes or None
        :param sender_rsa_public_key: Sender's RSA public key used to sign the\
        transaction
        :type sender_rsa_public_key: bytes or None
        :param signature: Sender's signature
        :type signature: bytes or None
        :param timestamp: The time transaction was created
        :type timestamp: float
        '''
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.content = content
        self.sender_rsa_public_key = sender_rsa_public_key
        self.signature = signature
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, str]:
        '''
        Returns transaction as dictionary

        :return: Transaction as dictionary
        :rtype: dict(str, str)
        '''
        return {
            "sender": (self.sender.hex() if self.sender else None),
            "recipient": self.recipient.hex(),
            "amount": self.amount,
            "content": (self.content.hex() if self.content else None),
            "sender_rsa_public_key": (self.sender_rsa_public_key.hex()
                                      if self.sender_rsa_public_key else None),
            "signature": (self.signature.hex() if self.signature else None),
            "timestamp": self.timestamp
        }

    def calcuclate_hash(self) -> str:
        '''
        Calculates tha SHA-256 hash of the transaction,
        excluding singature.

        :return: Hash of the transaction
        :rtype: str
        '''
        transaction_dict = self.to_dict()
        transaction_dict.pop("signature", None)
        transaction_string = json.dumps(
            transaction_dict, sort_keys=True, ensure_ascii=False
        )
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def is_valid(self, public_key: rsa.RSAPublicKey) -> bool:
        '''
        Validates transaction using sender's RSA public key

        :param public_key: Sender's public key
        :type public_key: rsa.RSAPublicKey
        :return: If transaction is valid or not
        :rtype: bool
        '''

        if not self.signature:
            log.warning("No signature in this transaction")
            return False
        if not public_key:
            log.warning("No public key provided")
            return False

        # Using the verify static method from crypto/signatures.py
        verify(public_key, self.content, self.signature)
