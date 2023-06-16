from hashlib import sha256
import json


class Block:
    def __init__(self, index, timestamp, previous_block_hash, message_list):
        self.index = index
        self.timestamp = timestamp
        self.previous_block_hash = previous_block_hash
        self.message_list = message_list

    def compute_hash(self):
        block_data = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_data.encode()).hexdigest()

    def show_block(self):
        print(self.__dict__)
