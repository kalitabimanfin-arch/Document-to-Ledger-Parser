import pandas as pd
from datetime import datetime

# =============================================
# DOCUMENT-TO-LEDGER PARSER
# Standardizes messy client data for QuickBooks/Xero
# =============================================

print("=" * 60)
print("DOCUMENT-TO-LEDGER PARSER")
print("Standardizing messy client data...")
print("=" * 60)

# ---------------------------------------------
# PART 1: PARSE MESSY BANK STATEMENT
# ---------------------------------------------
print("\n📄 Processing: messy_bank_statement.csv")

bank = pd.read_csv('messy_bank_statement.csv')

# Standardize date format (DD/MM/YYYY → YYYY-MM-DD)
bank['Txn Date'] = pd.to_datetime(bank['Txn Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

# Combine Debit and Credit into a single Amount column
# Debits = negative, Credits = positive
bank['Amount'] = bank['Credit'].fillna(0) - bank['Debit'].fillna(0)

# Create standardized output
standardized_bank = pd.DataFrame({
    'Date': bank['Txn Date'],
    'Description': bank['Details'],
    'Amount': bank['Amount']
})

print(f"✅ Extracted {len(standardized_bank)} transactions")
print(f"✅ Dates normalized to YYYY-MM-DD")
print(f"✅ Debit/Credit merged into single Amount column")

# ---------------------------------------------
# PART 2: PARSE MESSY INVOICE
# ---------------------------------------------
print("\n📄 Processing: messy_invoice.csv")

invoice = pd.read_csv('messy_invoice.csv')

# Standardize date format (Jan 15 2025 → 2025-01-15)
invoice['Invoice Date'] = pd.to_datetime(invoice['Invoice Date'], format='%b %d %Y').dt.strftime('%Y-%m-%d')

# Rename columns to standard format
standardized_invoice = pd.DataFrame({
    'Invoice_Number': invoice['Invoice No'],
    'Date': invoice['Invoice Date'],
    'Vendor': invoice['Vendor'],
    'Amount': invoice['Total'],
    'Currency': invoice['Currency']
})

print(f"✅ Extracted {len(standardized_invoice)} invoices")
print(f"✅ Dates normalized to YYYY-MM-DD")

# ---------------------------------------------
# PART 3: EXPORT FOR QUICKBOOKS
# ---------------------------------------------
print("\n📤 Exporting for QuickBooks...")

# QuickBooks expects: Date, Description, Amount
qb_export = standardized_bank.copy()
qb_export['Date'] = pd.to_datetime(qb_export['Date']).dt.strftime('%m/%d/%Y')
qb_export.to_csv('quickbooks_ready.csv', index=False)

print("✅ Saved: quickbooks_ready.csv")

# ---------------------------------------------
# PART 4: EXPORT FOR XERO
# ---------------------------------------------
print("\n📤 Exporting for Xero...")

# Xero expects: Date, Payee, Amount
xero_export = standardized_bank.copy()
xero_export['Date'] = pd.to_datetime(xero_export['Date']).dt.strftime('%d/%m/%Y')
xero_export = xero_export.rename(columns={'Description': 'Payee'})
xero_export.to_csv('xero_ready.csv', index=False)

print("✅ Saved: xero_ready.csv")

# ---------------------------------------------
# SUMMARY
# ---------------------------------------------
print("\n" + "=" * 60)
print("✅ PARSING COMPLETE!")
print("=" * 60)
print(f"📊 Bank transactions processed: {len(standardized_bank)}")
print(f"📊 Invoices processed: {len(standardized_invoice)}")
print(f"📁 Output files created: quickbooks_ready.csv, xero_ready.csv")
print("\n💡 Time saved: ~20 minutes of manual reformatting → 2 seconds")
print("=" * 60)

# Show preview
print("\n📋 PREVIEW: QuickBooks-Ready Output")
print(standardized_bank.to_string(index=False))