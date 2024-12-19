import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from src.blockchain.blockchain import Block


class TestBlock(unittest.TestCase):
    def setUp(self):
        self.index = 1
        self.previous_hash = "0000abcd"
        self.timestamp = 1678901234.567
        self.transactions = []
        self.nonce = 0
        self.hash = "1234abcd"
        self.block = Block(
            index=self.index,
            previous_hash=self.previous_hash,
            timestamp=self.timestamp,
            transactions=self.transactions,
            nonce=self.nonce,
            hash=self.hash
        )

    def test_block_initialization(self):
        self.assertEqual(self.block.index, self.index)
        self.assertEqual(self.block.previous_hash, self.previous_hash)
        self.assertEqual(self.block.timestamp, self.timestamp)
        self.assertEqual(self.block.transactions, self.transactions)
        self.assertEqual(self.block.nonce, self.nonce)
        self.assertEqual(self.block.hash, self.hash)


if __name__ == "__main__":
    unittest.main()
