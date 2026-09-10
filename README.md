# 📄 Document-to-Ledger Parser

**AI-powered tool that standardizes messy client invoices and bank statements for QuickBooks/Xero import.**

---

## 🎯 The Problem

Every client sends data in different formats:
- Dates as `DD/MM/YYYY` or `Jan 15 2025` or `01-15-2025`
- Debits and credits in separate columns
- Different column names for the same data

Accountants waste hours manually reformatting before importing into QuickBooks or Xero.

---

## 💡 The Solution

This Python tool:
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

---

## 🚀 How to Run

```bash
python parser.py


Scroll down → Commit message: `Updated README with project details` → Click **"Commit changes"**

---

## ✅ You're Done!

**Your 3 portfolios:**
1. [AAPL Financial Analysis](https://github.com/kalitabimanfin-arch/AAPL-Financial-Analysis-Portfolio)
2. [Accounting Automation](https://github.com/kalitabimanfin-arch/Accounting-Automation-Portfolio)
3. [Document-to-Ledger Parser](https://github.com/kalitabimanfin-arch/Document-to-Ledger-Parser)

---

## 🗣️ Interview Line (If They Ask About Project #3)

> *"I identified a real pain point: accountants waste hours reformatting client data for QuickBooks. I built a Python parser that reads messy CSVs, normalizes the dates and amounts, and exports clean import-ready files. It's a prototype, but it proves the concept. I plan to add PDF parsing using AI vision models next."*

---

**Now go run the script and upload. You have time. Let's go!** 🚀
