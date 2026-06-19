from flask import Flask, request, jsonify
from utils.predict import safe_predict

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    result = safe_predict(data)

    return jsonify(result)

@app.route("/audit", methods=["GET"])
def audit():
    import os
    import json
    from blockchain.config import AUDIT_TRAIL_PATH, BLOCKCHAIN_SIMULATION_MODE, PROVIDER_URL, CONTRACT_ADDRESS
    
    if not os.path.exists(AUDIT_TRAIL_PATH):
        return jsonify([])
        
    try:
        with open(AUDIT_TRAIL_PATH, "r") as f:
            records = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Failed to read audit trail: {str(e)}"}), 500
        
    # If blockchain mode is active (not simulation), verify each round dynamically on-chain
    if not BLOCKCHAIN_SIMULATION_MODE:
        try:
            from web3 import Web3
            w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
            if w3.is_connected() and CONTRACT_ADDRESS:
                abi_path = os.path.join(os.path.dirname(__file__), "blockchain", "abi", "MediBellRegistry.json")
                with open(abi_path, "r") as f:
                    abi = json.load(f)
                contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
                
                verified_records = []
                for record in records:
                    r_num = record["round"]
                    # Call contract getRound
                    try:
                        on_chain_data = contract.functions.getRound(r_num).call()
                        # on_chain_data = [round, cid, accuracy, timestamp]
                        if on_chain_data[0] == r_num:
                            record["on_chain_verified"] = True
                            record["on_chain_accuracy"] = on_chain_data[2] / 100.0
                            record["on_chain_timestamp"] = on_chain_data[3]
                        else:
                            record["on_chain_verified"] = False
                    except Exception:
                        record["on_chain_verified"] = False
                    verified_records.append(record)
                return jsonify(verified_records)
        except Exception:
            pass
            
    return jsonify(records)

if __name__ == "__main__":
    app.run(debug=True)