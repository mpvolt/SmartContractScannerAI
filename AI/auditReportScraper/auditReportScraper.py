import fitz  # PyMuPDF

def extract_findings_from_pdf(pdf_path):
    findings_sections = []
    keywords = ['findings', 'vulnerabilities']
    capture = False

    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page_text = doc[page_num].get_text()
            lines = page_text.split('\n')

            for line in lines:
                lower_line = line.lower().strip()

                # Check if we’re entering a findings/vulnerabilities section
                if any(kw in lower_line for kw in keywords):
                    capture = True

                # Heuristic to detect leaving the section (new major section or summary)
                elif capture and (
                    lower_line.startswith('conclusion') or 
                    lower_line.startswith('recommendations') or
                    lower_line.startswith('appendix') or 
                    lower_line.strip() == ''
                ):
                    capture = False

                if capture:
                    findings_sections.append(line)

    return '\n'.join(findings_sections)

# Usage
pdf_file = "Yieldly_Finance_Bridge_Algorand_Smart_Contract_Security_Audit_Halborn_v_1_1.pdf"
findings_text = extract_findings_from_pdf(pdf_file)

# Save output or print
with open("findings_output.txt", "w") as f:
    f.write(findings_text)

print("Findings extracted successfully.")
