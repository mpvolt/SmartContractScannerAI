import subprocess
import argparse
import openai

# OpenAI API Key
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

def main():
    parser = argparse.ArgumentParser(description="Smart Contract Security Scanner with AI")
    parser.add_argument("contract", help="Path to Solidity contract")
    args = parser.parse_args()

    print("\n🔍 Running Solidity Security Scan...")
    vulnerabilities = run_slither(args.contract)

    print("\n===== SECURITY REPORT =====")
    print(vulnerabilities)

    print("\n===== AI-Powered Explanations =====")
    print(explain_with_ai(vulnerabilities))

if __name__ == "__main__":
    main()
