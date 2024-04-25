import hashlib
import time
from dataclasses import dataclass
import copy
from dacite import from_dict

@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float


@dataclass
class Block:
    index: int
    transactions: list[Transaction]
    proof: int
    previous_hash: str
    timestamp: float # add timestamp field


class Blockchain:
    def __init__(self, address, difficulty_number, mining_reward):
        self.address = address
        self.difficulty_number = difficulty_number
        self.mining_reward = mining_reward
        self.chain = []
        self.current_transactions = []
        self.users = ['http://127.0.0.1:5000']

        block = self.create_block(1, [], 0, 0)
        while not self.check_proof(block):
              block.proof += 1
        self.add_block(block)

    def create_block(self, index, transactions, proof, previous_hash):
        timestamp = time.time() # current timestamp
        return Block(index, copy.copy(transactions), proof, previous_hash, timestamp)
    
    def add_player(self, player):
        self.users.append(player)

    def create_transaction(self, sender, recipient, amount):
        if self.users[sender] >= amount:
            self.users[sender] -= amount
            self.users[recipient] += amount
        return Transaction(sender, recipient, amount)

    def get_transactions(self):
        return self.current_transactions

    def current_block(self):
        return self.chain[len(self.chain) - 1]

    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append(Transaction(sender, recipient, amount))

    def next_index(self):
        return len(self.chain) + 1

    def get_length(self):
        return len(self.chain)

    def add_block(self, block):
        if self.check_proof(block):
            self.chain.append(block)

    def hash_block(self, block):
        return hashlib.sha256(str(block).encode()).hexdigest()

    def check_proof(self, block):
        # Check that the hash of the block ends in difficulty_number many zeros
        m = self.hash_block(block)
        last_difficulty_characters = m[0:self.difficulty_number]
        for c in last_difficulty_characters:
            if not c == '0':
                return False
        return True


    def mine(self):
        # Give yourself a reward at the beginning of the transactions
        self.add_transaction("network", self.address, self.mining_reward)

        # Find the right value for proof
        block = self.create_block(self.next_index(), self.get_transactions(), 0, self.hash_block(self.current_block()))
        while not self.check_proof(block):
              block.proof += 1

        # Add the block to the chain
        self.add_block(block)

        # Clear your current transactions
        self.current_transactions.clear()
        pass

    def validate_chain(self, chain):
        if not self.check_proof(chain[0]):
            return False
        for i in range(1, len(chain)):
            b = chain[i]
            if not b.previous_hash == self.hash_block(chain[i - 1]):
                return False
            if not self.check_proof(chain[i]):
                return False
        return True

    def receive_chain(self, chain_raw_json):
        chain = [from_dict(Block, b) for b in chain_raw_json]
        if self.validate_chain(chain) and len(chain) > self.get_length():
            self.chain = chain
            return True
        return False
