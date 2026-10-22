import os
import re
import json
import pymupdf as fitz

PDF_DIR = "pdfs"

salary_data = []


def extract_amount(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).replace(",", "").strip()
    return None


for pdf_file in os.listdir(PDF_DIR):

    if not pdf_file.lower().endswith(".pdf"):
        continue

    print(f"Processing {pdf_file}")

    pdf_path = os.path.join(PDF_DIR, pdf_file)

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text() + "\n"

    record = {}

    record["source"] = pdf_file

    # MONTH
    month_match = re.search(
        r"Salary\s+Slip\s+for\s+the\s+Month\s+of\s+([A-Za-z]+)\s*-\s*(\d{4})",
        text,
        re.IGNORECASE
    )

    if month_match:
        record["month"] = (
            f"{month_match.group(1)} {month_match.group(2)}"
        )
    else:
        record["month"] = None

    patterns = {
        "basic_pay": r"Basic\s*:?\s*([\d,]+)",
        "provident_fund": r"Provident\s+Fund\s*:?\s*([\d,]+)",
        "hra": r"\bHRA\s*:?\s*([\d,]+)",
        "professional_tax": r"Professional\s+Tax\s*:?\s*([\d,]+)",
        "education_allowance": r"Education\s+Allowance\s*:?\s*([\d,]+)",
        "lta": r"\bLTA\s*:?\s*([\d,]+)",
        "special_allowance": r"Special\s+Allowance\s*:?\s*([\d,]+)",
        "merit_pay": r"Merit\s+Pay\s*:?\s*([\d,]+)",
        "gross_pay": r"Gross\s+Pay\s*\(A\)\s*:?\s*([\d,]+)",
        "gross_deductions": r"Gross\s+Deductions\s*\(B\)\s*:?\s*([\d,]+)",
        "reimbursement": r"Reimbursement\s*\(C\)\s*:?\s*([\d,]+)",
        "net_pay": r"Net\s+Pay\s*\(A-B\)\s*:?\s*([\d,]+)",
        "total_pay": r"Total\s+Pay\s*\(A-B\)\s*\+\s*C\s*:?\s*([\d,]+)",
        "net_taxable_income": r"Net\s+Taxable\s+Income.*?:?\s*([\d,]+)",
        "income_tax_before_rebate": r"Income\s+Tax.*?Before\s+Rebate.*?:?\s*([\d,]+)",
        "rebate_87a": r"Rebate.*?87A.*?:?\s*([\d,]+)",
        "raw_surcharge": r"Raw\s+Surcharge\s*:?\s*([\d,]+)"
    }

    for field, pattern in patterns.items():
        record[field] = extract_amount(pattern, text)

    fy_match = re.search(
        r"FY\s+(\d{4}-\d{2})",
        text,
        re.IGNORECASE
    )

    record["financial_year"] = (
        fy_match.group(1)
        if fy_match
        else None
    )

    regime_match = re.search(
        r"Tax\s+Regime\s*:\s*(New|Old)",
        text,
        re.IGNORECASE
    )

    record["tax_regime"] = (
        regime_match.group(1)
        if regime_match
        else None
    )

    salary_data.append(record)

with open(
    "salary_data.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        salary_data,
        f,
        indent=4
    )

print("salary_data.json created successfully")
