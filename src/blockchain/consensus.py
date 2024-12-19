'''Consensus module handles PoW validation and mining process'''

from .blockchain import Block, Blockchain
from utils.logger import Logger

log = Logger("consensus")


class ProofOfWork:
    '''
    This class is used to mine and find hash of new block

    :ivar difficulty: difficulty of mining the block
    :type difficulty: int
    '''

    def __init__(self, difficulty: int):
        '''
        Initializes ProofOfWork class

        :param difficulty: difficulty of mining the block
        :type difficulty: int
        '''
        self.difficulty = difficulty

    def mine(self, block: Block) -> str:
        '''
        Processes block mining by finding hash that meets the difficulty
        criteria

        :param block: Block to be mined
        :type block: Block
        :return: The hash of the mined block
        :rtype: str
        '''

        while not self.validate(block):
            block.nonce += 1
            block.hash = block.calculate_hash()
        log.info(f"Block mined: {block.hash}")
        return block.hash

    def validate(self, block: Block) -> bool:
        '''
        Validates that a block's hash meets difficulty criteria

        :param block: Block that needs to be validated
        :type block: Block
        :return: If Block is valid or not
        :rtype: bool
        '''

        target = self.get_target()
        return block.hash.startswith(target)

    def get_target(self) -> str:
        '''
        Returns the target string based on the difficulty

        :return: Target string
        :rtype: str
        '''

        return "0" * self.difficulty


class Validator:
    '''Class that handles validations of blocks and blockchain'''

    def validate_blockchain(self, blockchain: Blockchain) -> bool:
        '''
        Validates the integrity of the entrire blockchain

        :param blockchain: Blockchain to be validated
        :type blockchain: Blockchain
        :return: If blockchain is valid or not
        :rtype: bool
        '''

        for i in range(1, len(blockchain)):
            current_block = blockchain.chain[i]
            previous_block = blockchain.chain[i-1]
            if not self.validate_block(current_block, previous_block):
                return False
        return True

    def validate_block(self, current_block: Block, previous_block: Block) \
            -> bool:
        '''
        Validates a single block in relation to previous block

        :param current_block: Block that needs to be validated
        :type current_block: Block
        :param previous_block: Block behind the current block
        :type previous_block: Block
        :return: If block is valid or not
        :rtype: bool
        '''

        index = current_block.index
        if current_block.hash != current_block.calculate_hash():
            log.warning(f"Block {index} has invalid hash.")
            return False

        if current_block.previous_hash != previous_block.hash:
            log.warning(f"Block {index} has invalid previous hash")
            return False

        if current_block.timestamp <= previous_block.timestamp:
            log.warning(f"Block {index} has invalid timestamp")
            return False

        return True
