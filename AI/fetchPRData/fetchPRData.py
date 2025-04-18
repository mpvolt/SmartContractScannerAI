import requests
import base64
import json

# --- CONFIGURATION ---
REPO = "Aurory-Game/ocil"
COMMIT_SHA = "91217b35cd3005a2a7ef056cd3a1bddf4b7a3e67"
OUTPUT_FILE = "llm_training_data.jsonl"
VULN_ID = "CVE-EXAMPLE-123"
DESCRIPTION_OF_ISSUE = "Example: Missing input sanitization in critical function."
DESCRIPTION_OF_FIX = "Add input checks to ensure safe behavior."
SEVERITY = "critical"

HEADERS = {"Accept": "application/vnd.github.v3+json"}

def get_commit_data(repo, sha):
    url = f"https://api.github.com/repos/{repo}/commits/{sha}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_file_content(repo, ref, path):
    url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={ref}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    content_json = response.json()
    return base64.b64decode(content_json['content']).decode('utf-8')

def filter_file(filename):
    return filename.endswith(".rs") or filename.endswith(".sol") or filename.endswith(".ts")

def main():
    print("Fetching commit data...")
    commit_data = get_commit_data(REPO, COMMIT_SHA)
    parent_sha = commit_data["parents"][0]["sha"]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for changed_file in commit_data["files"]:
            file_path = changed_file["filename"]
            # if not filter_file(file_path):
            #     continue

            try:
                before_code = get_file_content(REPO, parent_sha, file_path)
            except Exception:
                before_code = ""
            try:
                after_code = get_file_content(REPO, COMMIT_SHA, file_path)
            except Exception:
                after_code = ""

            input_block = (
                f"# Vulnerability ID: {VULN_ID}\n"
                f"# Description of issue: {DESCRIPTION_OF_ISSUE}\n"
                f"# Description of fix: {DESCRIPTION_OF_FIX}\n"
                f"# Severity: {SEVERITY}\n"
                f"# File: {file_path}\n"
                f"--- BEFORE CODE (from parent commit) ---\n"
                f"{before_code.strip()}\n"
                f"--- END BEFORE ---\n"
            )

            output_block = after_code.strip()

            # Write as a single JSONL entry
            f.write(json.dumps({"input": input_block, "output": output_block}, ensure_ascii=False) + "\n")

    print(f"Entries written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()