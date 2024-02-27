import os
import fitz  # PyMuPDF
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    """Extracts text from a single PDF file."""
    text = ''
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Failed to extract text from {pdf_path}: {e}")
    return text

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def parse_transaction_details(text):
    """Parses the transaction details from the given text and filters out non-numerical values."""
    transactions = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line:  # If the line is not empty
            date = line.split()[0]
            description = ""
            amount = ""
            # Accumulate multi-line descriptions
            while i + 1 < len(lines) and lines[i + 1] and not lines[i + 1][0].isdigit():
                i += 1
                description += lines[i] + " "
            # Check for an amount on the next line and ensure it's a float
            if i + 1 < len(lines) and is_float(lines[i + 1].replace(',', '').strip()):
                i += 1
                amount = float(lines[i].replace(',', ''))
            if amount:  # Only add transactions with a valid amount
                transactions.append({'date': date, 'description': description.strip(), 'amount': amount})
        i += 1
    return transactions

def analyze_transactions(transactions):
    """Analyze transactions for total income, expenses, and subscriptions."""
    total_income = sum(t['amount'] for t in transactions if t['amount'] > 0)
    total_expenses = sum(t['amount'] for t in transactions if t['amount'] < 0)
    # Assuming subscription transactions contain keywords like 'Subscripti'
    subscriptions = sum(t['amount'] for t in transactions if 'Subscripti' in t['description'])
    # Print highlights
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expenses}")
    print(f"Total Subscriptions: {subscriptions}")
    print(f"Income after Subscriptions: {total_income - subscriptions}")
    print(f"Income after Subscriptions and Expenses: {total_income - subscriptions + total_expenses}")

def output_to_file(transactions, highlights):
    """Outputs transactions to a file with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"transactions_summary_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write(highlights + "\n")
        print(f"Summary has been written to {filename}")

def read_pdfs_in_folder(folder_path):
    """Reads all PDFs in the specified folder, parses, analyzes, and outputs transactions."""
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            print(f"Processing {file_name}...")
            text = extract_text_from_pdf(pdf_path)
            transactions = parse_transaction_details(text)
            analyze_transactions(transactions)
            highlights = f"Processed {file_name}: Total Transactions: {len(transactions)}"
            output_to_file(transactions, highlights)

if __name__ == "__main__":
    folder_path = 'pdfs'  # Assuming the PDFs are in a folder named 'pdfs' in the current directory
    read_pdfs_in_folder(folder_path)
