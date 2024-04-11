# blockchain-skeleton
Skeleton code for the Cyber x ICPC blockchain workshop

## Getting Started
First, make a fork of this repository so that you have your own copy. 

There's some code missing in the skeleton, but you should be able to run it even without filling it in.

1. Using a Python package manager, install Flask.
2. Run `node.py`.
3. Make requests to the server! It will be running on localhost, Flask should tell you the port number. For making requests, you can use something like Postman.

In `blockchain.py`, the code for the `check_proof` and `mine` functions is missing. Go ahead and fill those in, and you have yourself a working centralized ledger system!

## Next Steps
The code is pretty bare-bones, so there's a lot you could add.

Easy:
- Timestamps on blocks
- Add known users in the network and give them some starting money
- Check that no one spends more money than they have
- Ensure blocks all have a set number of transactions

Medium:
- Add digital signatures (use another program to generate keys, and hard code in everyone's public keys)
- Check that signatures are valid when checking the validity of a block
