from flask import Flask, jsonify, request
from blockchain import Blockchain
import dataclasses
import requests

app = Flask(__name__)
# Give yourself a name
address = ""
# Make this unique for each node you are running on your computer
port_num = 5000
difficulty_number = 2
mining_reward = 10
local_blockchain = Blockchain(address, difficulty_number, mining_reward)


@app.route("/chain", methods=["GET", "POST"])
def chain():
    if request.method == "GET":
        response = {
            "chain": [dataclasses.asdict(block) for block in local_blockchain.chain],
            "length": len(local_blockchain.chain),
        }
        return jsonify(response), 200
    else:
        new_chain = request.get_json()
        replaced = local_blockchain.receive_chain(new_chain)
        if replaced:
            response = {
                "message": "The chain was replaced",
                "chain": local_blockchain.chain,
            }
        else:
            response = {
                "message": "No changes to the chain",
                "chain": local_blockchain.chain,
            }

        return jsonify(response), 200


@app.route("/mine", methods=["GET"])
def mine():
    local_blockchain.mine()

    response = {
        "status": "Success",
        "index": local_blockchain.current_block().index,
        "transactions": [
            dataclasses.asdict(t) for t in local_blockchain.current_block().transactions
        ],
        "proof": local_blockchain.current_block().proof,
    }

    return jsonify(response), 200


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()
    required = ["sender", "recipient", "amount"]
    if not values or not all(k in values for k in required):
        return "Missing values", 400

    local_blockchain.add_transaction(
        values["sender"], values["recipient"], values["amount"]
    )

    response = {
        "message": f"Transaction will be added to block {local_blockchain.next_index()}"
    }
    return jsonify(response), 201


@app.route("/network", methods=["GET", "POST"])
def network():
    if request.method == "GET":
        response = {"nodes": list(local_blockchain.players)}
        return jsonify(response), 200
    else:
        value = request.get_json()
        if not value or not ("address" in value):
            return "Missing values", 400

        local_blockchain.add_player(value["address"])

        response = {"message": f"Added player address {value['address']}"}
        return jsonify(response), 200


@app.route("/broadcast", methods=["GET"])
def broadcast():
    successful_broadcasts = []
    for a in local_blockchain.players:
        try:
            r = requests.post(
                a + "/chain",
                json=[dataclasses.asdict(block) for block in local_blockchain.chain],
            )
            successful_broadcasts.append(a)
        except Exception as e:
            print("Failed to send to ", a)
            print(e)
    response = {"message": "Chain broadcasted", "recipients": successful_broadcasts}
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(port=port_num)
