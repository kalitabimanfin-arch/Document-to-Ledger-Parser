# 📄 Document-to-Ledger Parser

**AI-powered tool that standardizes messy client invoices and bank statements for QuickBooks/Xero import.**

---

## 🎯 The Problem

Every client sends data in different formats:
- Dates as `15-01-2025` or `Jan 15 2025`
- Debits and credits in separate columns
- Different column names for the same data

Accountants waste hours manually reformatting before importing into QuickBooks or Xero.

---

## 💡 The Solution

This tool:
1. Reads messy CSV files from any client
2. Normalizes dates, amounts, and column names
3. Exports clean files ready for QuickBooks or Xero import

**Time Saved:** ~20 minutes of manual work → 2 seconds

---

## 🛠️ How It Works

| Step | Action |
| :--- | :--- |
| 1 | Reads `messy_bank_statement.csv` and `messy_invoice.csv` |
| 2 | Normalizes all dates to `YYYY-MM-DD` |
| 3 | Merges Debit/Credit columns into single `Amount` |
| 4 | Exports `quickbooks_ready.csv` and `xero_ready.csv` |

---

## 📁 Files

| File | Purpose |
| :--- | :--- |
| `parser.py` | Main automation script |
| `messy_bank_statement.csv` | Sample client data (input) |
| `messy_invoice.csv` | Sample client invoices (input) |
| `quickbooks_ready.csv` | Output for QuickBooks import |
| `xero_ready.csv` | Output for Xero import |
| `requirements.txt` | Python dependencies |

---

## 🚀 How to Run

**Prerequisites:** Python 3.x installed

1. Clone this repository:
   ```bash
   git clone https://github.com/kalitabimanfin-arch/Document-to-Ledger-Parser.git
   pip install -r requirements.txt
   python parser.py
