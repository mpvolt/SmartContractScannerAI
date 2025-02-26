from flask import Flask, request, jsonify
import subprocess
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/analyze": {"origins": "http://localhost:3000"}})

# Set your OpenAI API key
client = openai.OpenAI(api_key="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")
SLITHER_PATH = "/Users/matt/Documents/SmartContractScannerAI/backend/venv/bin/slither"  # Change this to your Slither path

def run_slither(contract_path):
    """Runs Slither on a Solidity contract and returns vulnerabilities."""
    try:
        result = subprocess.run([SLITHER_PATH, contract_path], capture_output=True, text=True)
        
        print("\n🔍 Slither Output (stdout):")
        print(result.stdout)

        print("\n⚠️ Slither Errors (stderr):")
        print(result.stderr)

        if not result.stdout and result.stderr:
            return f"Slither failed: {result.stderr}"

        return result.stdout
    except Exception as e:
        return f"Error running Slither: {e}"

def explain_with_ai(vulnerability_text):
    """Uses AI to explain a vulnerability and suggest fixes."""
    try:
        print(vulnerability_text)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert Solidity security auditor."},
                {"role": "user", "content": f"Explain the following Solidity vulnerability and suggest a fix:\n\n{vulnerability_text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error fetching AI explanation: {e}"

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handles file uploads or pasted Solidity code, runs Slither, and returns results."""
    print("📩 Incoming Request!")  # ✅ Log request arrival
    print("🔍 Request Headers:", request.headers)  # ✅ Log request headers

    contract_code = request.form.get("code")
    file = request.files.get("file")

    if file:
        print(f"📂 Received File: {file.filename}, Size: {file.content_length} bytes")  # ✅ Log file details
        contract_path = f"temp/{file.filename}"
        file.save(contract_path)
    elif contract_code:
        print("📝 Received Solidity Code")  # ✅ Log received Solidity code
        contract_path = "temp/temp.sol"
        with open(contract_path, "w") as f:
            f.write(contract_code)
    else:
        print("❌ No contract provided!")
        return jsonify({"error": "No contract provided."}), 400

    # ✅ Run Slither and get output
    vulnerabilities = run_slither(contract_path)

    print("\n===== SECURITY REPORT =====")
    print(vulnerabilities)

    print("\n===== AI-Powered Explanations =====")
    print(explain_with_ai(vulnerabilities))

    # ✅ Delete temp file after processing
    os.remove(contract_path)

    return jsonify({"analysis": explain_with_ai(vulnerabilities)})

if __name__ == '__main__':
    os.makedirs("temp", exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5001)  # ✅ Allow external connections
