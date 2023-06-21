from hashlib import sha256
import json


class Block:
    def __init__(
        self, timestamp, previous_block_hash, message="", difficulty=2, nonce=0
    ):
        self.timestamp = timestamp
        self.previous_block_hash = previous_block_hash
        self.message = message
        self.difficulty = difficulty
        self.nonce = nonce
        self.mine()

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

    def mine(self):
        self.hash = self.compute_hash()
        # proof of work
        while not self.hash.startswith("0" * self.difficulty):
            self.nonce += 1
            self.hash = self.compute_hash()

    def validate_proof(self):
        return (
            self.hash.startswith("0" * self.difficulty)
            and self.hash == self.compute_hash()
        )

    def show_block(self):
        print(self.__dict__)
