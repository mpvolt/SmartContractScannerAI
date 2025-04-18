import fitz  # PyMuPDF
import re
import json
import sys

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_vulnerabilities_from_text(text):
    # Find the 'Vulnerabilities' section
    pattern_vuln_section = re.compile(r'(Vulnerabilities.*?)(?:\n[A-Z][^\n]*Section|\Z)', re.DOTALL | re.IGNORECASE)
    section_match = pattern_vuln_section.search(text)
    if not section_match:
        print("No 'Vulnerabilities' section found.")
        return []
    vuln_section = section_match.group(1)

    # Regex for individual vulnerabilities
    pattern = re.compile(
        r"(?P<header>OS-SSP-[A-Z\-]+-\d{2} \[[^\]]+\] \[[^\]]+\] \| [^\n]+)\n"
        r"Description\n(?P<description>.*?)(?=\n(?:Remediation\n|Patch\n|OS-SSP|$))"
        r"(?:\nRemediation\n(?P<remediation>.*?)(?=\n(?:Patch\n|OS-SSP|$)))?"
        r"(?:\nPatch\n(?P<patch>.*?)(?=\nOS-SSP|$))?",
        re.DOTALL
    )

    vulnerabilities = []
    for match in pattern.finditer(vuln_section):
        id_line = match.group('header').strip()
        description = match.group('description').strip() if match.group('description') else None
        remediation = match.group('remediation').strip() if match.group('remediation') else None
        patch = match.group('patch').strip() if match.group('patch') else None

        # Parse the header line
        id_status_pattern = re.compile(r"^(OS-SSP-[A-Z\-]+-\d{2}) \[([^\]]+)\] \[([^\]]+)\] \| (.+)$")
        match_id = id_status_pattern.match(id_line)
        if not match_id:
            continue
        issue_id, severity, status, title = match_id.groups()

        vulnerabilities.append({
            "id": issue_id,
            "severity": severity,
            "status": status,
            "title": title,
            "description": description,
            "remediation": remediation,
            "patch": patch,
        })
    return vulnerabilities

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_vulnerabilities_from_pdf.py <audit.pdf>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    text = extract_text_from_pdf(pdf_path)
    vulns = extract_vulnerabilities_from_text(text)
    print(json.dumps(vulns, indent=2))