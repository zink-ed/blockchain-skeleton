import os
import sys
import requests
import json


os.environ["NO_PROXY"] = "127.0.0.1"
address = "http://127.0.0.1:5000"

if __name__ == "__main__":
    print("Input 1 to see the blockchain on the server.")
    print("Input 2 to make the server mine a block.")
    print("Input 3 to add a transaction to the server.")
    print("Input q to quit.")
    while True:
        choice = input("> ")
        if choice == "1":
            r = requests.get(address + "/chain")
            json.dump(r.json(), sys.stdout, indent=2)
            print()
            print(r.status_code)
        elif choice == "2":
            r = requests.get(address + "/mine")
            json.dump(r.json(), sys.stdout, indent=2)
            print()
            print(r.status_code)
        elif choice == "3":
            sender = input("Input the sender: ")
            recipient = input("Input the recipient: ")
            amount = input("Input an amount: ")
            try:
                amount = float(amount)
                payload = {"sender": sender, "recipient": recipient, "amount": amount}
                r = requests.post(address + "/transactions/new", json=payload)
                json.dump(r.json(), sys.stdout, indent=2)
                print()
                print(r.status_code)
            except:
                print("Invalid amount. Please input a float.")

        elif choice == "q":
            print("Goodbye.")
            exit()
