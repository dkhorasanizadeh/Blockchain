from hashlib import sha256
import json
import time
import os

STARTING_RATE = int(os.getenv("STARTING_RATE")) or 10
INCREASE_COEFFICIENT = int(os.getenv("INCREASE_COEFFICIENT")) or 10
INCREASE_BY_LENGTH = int(os.getenv("INCREASE_BY_LENGTH")) or 10
STARTING_DIFFICULTY = int(os.getenv("STARTING_DIFFICULTY")) or 3

class Block:
    def __init__(
        self, previous_block_hash, message="", difficulty=2, nonce=0
    ):
        self.timestamp = time.time()
        self.previous_block_hash = previous_block_hash
        self.message = message
        self.difficulty = difficulty
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_data = json.dumps(self.__dict__, sort_keys=True)
        block_data = (
            str(self.timestamp)
            + str(self.previous_block_hash)
            + self.message
            + str(self.difficulty)
            + str(self.nonce)
        )
        return sha256(block_data.encode()).hexdigest()

    def mine(self, chain):
        with chain.mutex:
            last_block = chain.last_block()
            chain_length = len(chain.chain)
        while not self.hash.startswith("0" * self.difficulty):
            self.timestamp = time.time()
            self.difficulty = self.adjust_difficulty(last_block, chain_length)
            self.nonce += 1
            self.hash = self.compute_hash()

    def validate_block(self, chain):
        valid = (
            self.previous_block_hash == chain.last_block().hash and
            self.hash == self.compute_hash() and
            self.hash.startswith("0" * self.difficulty) and
            abs(self.difficulty - chain.last_block().difficulty) <= 1
        )
        return valid

    def __str__(self):
        return str(self.__dict__)

    def adjust_difficulty(self, last_block, chain_length):
        if self.timestamp - last_block.timestamp < \
            (STARTING_RATE + INCREASE_COEFFICIENT*(chain_length//INCREASE_BY_LENGTH)):
            return last_block.difficulty + 1
        return max(last_block.difficulty - 1,1)

    @staticmethod
    def initial_block():
        initial_block = Block('0')
        initial_block.hash = '0'
        initial_block.timestamp = 1
        initial_block.message = 'Initial block'
        initial_block.difficulty = STARTING_DIFFICULTY
        initial_block.nonce = 0
        return initial_block
