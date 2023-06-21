#pylint: disable=import-error, missing-module-docstring, missing-function-docstring, missing-class-docstring
import os
import random
import threading
import time

import redis

from blockchain import Blockchain

blockchain = Blockchain()
pubsub = redis.StrictRedis(os.getenv('REDIS_URL') or 'localhost', os.getenv('REDIS_PORT') or 6379)

def mine(miner_id):
    message = 0
    time.sleep(3)
    while True:
        if blockchain.create_and_add_block(f'Miner {miner_id} - Block {message}'):
            message += 1
            pubsub.publish('blockchain', blockchain.serialize_chain())

def listen_for_new_chains():
    subscriber = pubsub.pubsub()
    subscriber.subscribe(['blockchain'])
    for message in subscriber.listen():
        if message['type'] == 'message':
            blockchain.replace_chain(message.get('data'))
            with blockchain.mutex:
                blockchain.show_blockchain()

if __name__ == '__main__':
    threading.Thread(target=mine, args=(random.randint(0,1000000),)).start()
    threading.Thread(target=listen_for_new_chains).start()
