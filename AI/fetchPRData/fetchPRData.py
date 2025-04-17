import requests
import base64
from difflib import unified_diff

# === CONFIGURATION ===
REPO = "Aurory-Game/ocil"
COMMIT_SHA = "91217b35cd3005a2a7ef056cd3a1bddf4b7a3e67"
OUTPUT_FILE = "pr_diff_output.txt"  # Output file for storing the result

# === HEADERS (OPTIONAL: Use a GitHub token to avoid rate limits) ===
HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}

def get_commit_data(repo, sha):
    """Fetch commit data from GitHub API."""
    url = f"https://api.github.com/repos/{repo}/commits/{sha}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_file_content(repo, ref, path):
    """Retrieve file content for a specific commit (before or after)."""
    url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={ref}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    content_json = response.json()
    return base64.b64decode(content_json['content']).decode('utf-8')

def process_files(repo, commit_data, output_file):
    """Process the changed files in the commit and write output to a file."""
    parent_sha = commit_data["parents"][0]["sha"]
    
    with open(output_file, 'w') as output_file_handle:
        for changed_file in commit_data["files"]:
            file_path = changed_file["filename"]
            output_file_handle.write(f"Processing {file_path}...\n")

            # Get before (parent) and after (current) file contents
            before_code = get_file_content(repo, parent_sha, file_path)
            after_code = get_file_content(repo, commit_data["sha"], file_path)

            # Write before and after code to the output file
            output_file_handle.write(f"\n--- BEFORE CODE (from parent commit) ---\n")
            output_file_handle.write(before_code + "\n")

            output_file_handle.write(f"\n--- AFTER CODE (from current commit) ---\n")
            output_file_handle.write(after_code + "\n")

            output_file_handle.write(f"\n--- UNIFIED DIFF for {file_path} ---\n")
            diff = unified_diff(
                before_code.splitlines(),
                after_code.splitlines(),
                fromfile=f"before_{file_path}",
                tofile=f"after_{file_path}",
                lineterm=""
            )
            output_file_handle.write("\n".join(diff) + "\n")
            output_file_handle.write("=" * 80 + "\n")

def main():
    print("Fetching commit data...")
    commit_data = get_commit_data(REPO, COMMIT_SHA)
    
    print(f"Writing output to {OUTPUT_FILE}...")
    process_files(REPO, commit_data, OUTPUT_FILE)

if __name__ == "__main__":
    main()
