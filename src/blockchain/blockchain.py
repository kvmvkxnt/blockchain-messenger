'''This module handles all operations relared to block or blockchain'''

from .transaction import Transaction
from typing import List, Dict
import json5 as json
import hashlib
from .consensus import Validator, ProofOfWork
from utils.logger import Logger
from cryptography.hazmat.primitives.asymmetric import dh
import time

log = Logger("blockchain")


class Block:
    '''
    Block in the blockchain

    :ivar index: Index of the block
    :type index: int
    :ivar previous_hash: Hash of the previous block
    :type previous_hash: str
    :ivar timestamp: Time the block was mined and created
    :type timestamp: float
    :ivar transactions: List of transactions in the block
    :type transactions: list[Transaction],
    :ivar nonce: A number used once during the mining process for the block
    :type nonce: int
    :ivar hash: Hash of the current block
    :type hash: str
    '''

    def __init__(self, index: int, previous_hash: str, timestamp: float,
                 transactions: List[Transaction], nonce: int = 0,
                 hash: str = None) -> None:
        '''
        Initializes the block

        :param index: Index of the block
        :type index: int
        :param previous_hash: Hash of the previous block
        :type previous_hash: str
        :param timestamp: Time the block was mined and created
        :type timestamp: float
        :param transactions: List of transactions in the block
        :type transactions: list[Transaction],
        :param nonce: Number used once during the mining process for the block
        :type nonce: int
        :param hash: Hash of the current block
        :type hash: str
        '''
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash() if not hash else hash

    def to_dict(self) -> Dict[str, str]:
        '''
        Returns block as dictionary

        :return: Block as dictionary
        :rtype: dict(str, str)
        '''
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": [transaction.to_dict() for transaction
                             in self.transactions],
            "nonce": self.nonce
        }

    def calculate_hash(self) -> str:
        '''
        Calculates the SHA-256 hash of the block's content

        :return: Hash of the block
        :rtype: str
        '''
        block_string = json.dumps(
            self.to_dict(), sort_keys=True, ensure_ascii=False
        )
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    '''
    Handles blockchain

    :ivar difficulty: The difficulty level for mining blocks
    :type difficulty: int
    :ivar chain: List of blocks in the blockchain
    :type chain: list[Block]
    :ivar pending_transactions: List of pending transactions
    :type pending_transactions: list[Transaction]
    '''

    def __init__(self, difficulty: int = 4) -> None:
        '''
        Initializes blockchain

        :param difficulty: Difficulty level for mining blocks
        :type difficulty: int
        '''

        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty: int = difficulty
        self.pending_transactions: List[Transaction] = []

    def __len__(self) -> int:
        '''
        Returns length of the chain

        :return: Length of the chain
        :rtype: int
        '''

        return len(self.chain)

    def create_genesis_block(self) -> Block:
        '''
        Creates genesis block: the first block in the chain

        :return: Block to be the first in the chain
        :rtype: Block
        '''

        return Block(0, "0", 0, [])

    def get_latest_block(self) -> Block:
        '''
        Returns the latest block in the chain

        :return: The latest block in the chain
        :rtype: Block
        '''

        return self.chain[-1]

    def add_transaction(self, transaction: Transaction) -> None:
        '''Adds transaction to the pending_transactions if it is valid'''

        if self.is_transaction_valid(transaction):
            self.pending_transactions.append(transaction)
        else:
            log.warning("Transaction is invalid")

    def is_transaction_valid(self, transaction: Transaction) -> bool:
        '''
        Validates the transaction

        :param transaction: Transaction to be validates and added to blockchain
        :type transaction: Transaction
        :return: If transaction is valid or not
        :rtype: bool
        '''

        if transaction.sender:
            if not transaction.is_valid(transaction.sender_rsa_public_key):
                return False

            sender_balance = self.get_balance(transaction.sender)
            if sender_balance < transaction.amount:
                return False

        return True

    def get_balance(self, address: dh.DHPublicKey) -> float:
        '''
        Calculates the balance of a specific address.

        :param address: Address the balance of needs to be returned
        :type address: dh.DHPublicKey
        :return: The balance of the address
        :rtype: float
        '''

        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount

        return balance

    def mine_pending_transactions(self, miner_address: dh.DHPublicKey) \
            -> tuple[Block, Transaction] | tuple[None, None]:
        '''
        Mines pending transactions

        :param miner_address: Miner's address
        :type minder_address: dh.DHPublicKey
        :return: Mined block and reward transaction or None
        :rtype: tuple(Block, Transaction) or tuple(None, None)
        '''

        if not self.pending_transactions:
            log.info("No transactions to mine!")
            return None, None

        new_block = Block(
            index=len(self),
            previous_hash=self.get_latest_block().hash,
            timestamp=time.time(),
            transactions=self.pending_transactions
        )

        reward_transaction = Transaction(None, miner_address, 1, None, None,
                                         None, time.time())
        miner = ProofOfWork(self.difficulty)

        miner.mine(new_block)
        miner.validate(new_block)

        if Validator.validate_block(new_block, self.chain[-1]):
            self.chain.append(new_block)
            self.pending_transactions = [reward_transaction]
            return new_block, reward_transaction
        else:
            log.warning("Invalid block. Block was not added to the chain.")
            return None, None

    def is_chain_valid(self) -> bool:
        '''
        Validates the entire chain using validator

        :return: If chain is valid or not
        :rtype: bool
        '''

        return Validator.validate_block(self)
