import time
from block import Block


class Blockchain:
    def __init__(self, difficulty=2):
        self.unconfirmed_messages = []
        self.chain = []
        self.create_initial_block()

    def create_initial_block(self):
        initial_block = Block(0, time.time(), "0", [])
        self.chain.append(initial_block)

    def last_block(self):
        return self.chain[-1]

    def add_block(self, block: Block):
        last_block: Block = self.last_block()
        previous_hash = last_block.compute_hash()
        if previous_hash != block.previous_block_hash:
            return False
        self.chain.append(block)
        return True

    def add_new_message(self, message):
        self.unconfirmed_messages.append(message)

    def create_and_add_block(self):
        if not self.unconfirmed_messages:
            return False

        last_block: Block = self.last_block()

        new_block = Block(
            index=last_block.index + 1,
            timestamp=time.time(),
            previous_block_hash=last_block.compute_hash(),
            message_list=self.unconfirmed_messages,
        )

        self.add_block(new_block)
        self.unconfirmed_messages = []
        return new_block.index

    def validate_blockchain(self):
        for i in range(len(self.chain) - 1):
            if self.chain[i].compute_hash() != self.chain[i + 1].previous_block_hash:
                return False
        return True

    def show_blockchain(self):
        for block in self.chain:
            block.show_block()
            print()
