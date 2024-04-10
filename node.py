from flask import Flask, jsonify, request
from blockchain import Blockchain
import dataclasses

app = Flask(__name__)
# Give yourself an address
address = ""
difficulty_number = 2
mining_reward = 10
local_blockchain = Blockchain(address, difficulty_number, mining_reward)


@app.route("/chain", methods=["GET"])
def get_chain():
    response = {
        "chain": [dataclasses.asdict(block) for block in local_blockchain.chain],
        "length": len(local_blockchain.chain),
    }
    return jsonify(response), 200


@app.route("/mine", methods=["GET"])
def mine():
    local_blockchain.mine()

    response = {
        "status": "Success",
        "index": local_blockchain.current_block().index,
        "transactions": [dataclasses.asdict(t) for t in local_blockchain.current_block().transactions],
        "proof": local_blockchain.current_block().proof,
    }

    return jsonify(response), 200


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()
    required = ["sender", "recipient", "amount"]
    if not values or not all(k in values for k in required):
        return "Missing values", 400

    local_blockchain.add_transaction(values["sender"], values["recipient"], values["amount"])

    response = {
        "message": f"Transaction will be added to block {local_blockchain.next_index()}"
    }
    return jsonify(response), 201


if __name__ == "__main__":
    app.run()
