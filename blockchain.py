import time
from block import Block


class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.create_initial_block()

    def create_initial_block(self):
        initial_block = Block(
            timestamp=time.time(), previous_block_hash="0", difficulty=self.difficulty
        )
        self.chain.append(initial_block)

    def last_block(self):
        return self.chain[-1]

    def add_block(self, block: Block):
        last_block: Block = self.last_block()
        if block.previous_block_hash != last_block.hash:
            return False
        if not block.validate_proof():
            return False
        self.chain.append(block)
        return True

    def create_and_add_block(self, message):
        last_block: Block = self.last_block()
        new_block = Block(
            timestamp=time.time(),
            previous_block_hash=last_block.hash,
            message=message,
            difficulty=self.difficulty,
        )
        if not new_block.validate_proof():
            return False
        self.add_block(new_block)
        return True

    def validate_blockchain(self):
        for i in range(len(self.chain) - 1):
            if self.chain[i].hash != self.chain[i + 1].previous_block_hash:
                return False
        return True

    def show_blockchain(self):
        for block in self.chain:
            block.show_block()
            print()
