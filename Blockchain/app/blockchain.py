#pylint: disable=import-error, missing-module-docstring, missing-function-docstring, missing-class-docstring
import pickle
from threading import Lock

from block import Block


class Blockchain:
    def __init__(self):
        self.chain = [Block.initial_block()]
        self.mutex = Lock()

    def last_block(self):
        return self.chain[-1]

    def create_and_add_block(self, message):
        last_block: Block = self.last_block()
        new_block = Block(
            previous_block_hash=last_block.hash,
            message=message,
            difficulty=last_block.difficulty,
        )
        new_block.mine(self)
        with self.mutex:
            if not new_block.validate_block(self):
                return False
            self.chain.append(new_block)
            return True

    def replace_chain(self, new_chain_serialized):
        new_chain = pickle.loads(new_chain_serialized)
        if len(new_chain) <= len(self.chain):
            return False
        for i in range(1, len(new_chain) - 1):
            if new_chain[i].hash != new_chain[i + 1].previous_block_hash:
                return False
        with self.mutex:
            self.chain = new_chain
            return True

    def serialize_chain(self):
        return pickle.dumps(self.chain)

    def show_blockchain(self):
        chain = ""
        for block in self.chain:
            chain += str(block) + '\n'
        print(chain, end="")
