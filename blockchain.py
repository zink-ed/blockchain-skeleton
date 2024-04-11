import hashlib
import time
from dataclasses import dataclass

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
        self.users = {'Cathleen': 100}

    def create_block(self, index, transactions, proof, previous_hash):
        timestamp = time.time() # current timestamp
        return Block(index, transactions, proof, previous_hash)

    def create_transaction(self, sender, recipient, amount):
        if self.users[sender] >= amount:
            self.users[sender] -= amount
            self.users[recipient] += amount
        return Transaction(sender, recipient, amount)

    def get_transactions(self):
        return self.current_transactions

    def current_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append(Transaction(sender, recipient, amount))

    def next_index(self):
        return len(self.chain) + 1

    def get_length(self):
        return len(self.chain)

    def add_block(self, block):
        if self.check_proof(block):
            self.chain.append(block)

    def hash(self, block):
        return hashlib.sha256(str(block).encode()).hexdigest()

    def check_proof(self, block):
        # Check that the hash of the block ends in difficulty_number many zeros

        return False

    def mine(self):
        # Give yourself a reward at the beginning of the transactions
        self.add_transaction("network", self.address, self.mining_reward)
        # Find the right value for proof
        # Add the block to the chain
        # Clear your current transactions
        pass
