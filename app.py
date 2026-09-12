import streamlit as st
import pandas as pd
import re
from datetime import datetime

# =============================================
# PAGE CONFIGURATION
# =============================================
st.set_page_config(page_title="Document-to-Ledger Parser", page_icon="📄")

st.title("📄 Document-to-Ledger Parser")
st.write("Upload a messy CSV file. The app auto-detects the structure and exports clean files for QuickBooks or Xero.")

st.markdown("---")

# =============================================
# SMART DETECTION FUNCTIONS
# =============================================

def detect_date_column(df):
    date_keywords = ['date', 'txn', 'transaction', 'posted', 'invoice', 'created']
    best_score = 0
    best_col = None

    for col in df.columns:
        score = 0
        col_lower = str(col).lower()
        for keyword in date_keywords:
            if keyword in col_lower:
                score += 5

        sample = df[col].dropna().head(10).astype(str)
        date_patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
            r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
            r'[A-Za-z]{3,}\s+\d{1,2}\s+\d{2,4}',
            r'\d{1,2}\s+[A-Za-z]{3,}\s+\d{2,4}',
        ]
        for val in sample:
            for pattern in date_patterns:
                if re.search(pattern, str(val)):
                    score += 3
                    break

        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def detect_amount_columns(df, exclude_cols):
    numeric_cols = []

    for col in df.columns:
        if col in exclude_cols:
            continue
        try:
            converted = pd.to_numeric(
                df[col].astype(str).str.replace(r'[,$()\s+]', '', regex=True),
                errors='coerce'
            )
            if converted.notna().sum() > len(df) * 0.5:
                numeric_cols.append(col)
        except:
            pass

    debit_col = None
    credit_col = None
    single_amount = None

    for col in numeric_cols:
        col_lower = str(col).lower()
        if 'debit' in col_lower or 'withdrawal' in col_lower or 'out' in col_lower:
            debit_col = col
        elif 'credit' in col_lower or 'deposit' in col_lower or 'in' in col_lower:
            credit_col = col
        elif 'amount' in col_lower or 'total' in col_lower or 'value' in col_lower:
            single_amount = col

    if not single_amount and not (debit_col and credit_col) and numeric_cols:
        single_amount = numeric_cols[0]

    return debit_col, credit_col, single_amount


def detect_description_column(df, exclude_cols):
    desc_keywords = ['description', 'details', 'narrative', 'vendor', 'payee', 'memo', 'particulars']
    best_col = None

    for col in df.columns:
        if col in exclude_cols:
            continue
        col_lower = str(col).lower()
        for keyword in desc_keywords:
            if keyword in col_lower:
                return col
        if best_col is None:
            if df[col].dtype == 'object' and df[col].nunique() > 3:
                best_col = col

    return best_col


def parse_any_date(value):
    if pd.isna(value):
        return None
    val = str(value).strip()

    formats = [
        '%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y',
        '%b %d %Y', '%d %b %Y', '%B %d %Y', '%d %B %Y',
        '%Y/%m/%d', '%d.%m.%Y', '%m-%d-%Y', '%Y.%m.%d',
        '%d/%m/%y', '%d-%m-%y', '%m/%d/%y', '%m-%d-%y',
        '%d %b %y', '%d %B %y', '%b %d %y', '%B %d %y'
    ]

    for fmt in formats:
        try:
            return datetime.strptime(val, fmt).strftime('%Y-%m-%d')
        except:
            pass
    return None


# =============================================
# FILE UPLOADER
# =============================================
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    messy = pd.read_csv(uploaded_file)

    st.subheader("📋 Your Messy Data")
    st.dataframe(messy.head(20))
    st.caption(f"Showing 20 of {len(messy)} rows")

    st.markdown("---")

    # =============================================
    # AUTO-DETECT COLUMNS
    # =============================================
    st.subheader("🤖 Auto-Detected Structure")

    date_col = detect_date_column(messy)
    debit_col, credit_col, amount_col = detect_amount_columns(
        messy, [date_col] if date_col else []
    )
    desc_col = detect_description_column(
        messy, [date_col, debit_col, credit_col, amount_col]
    )

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**📅 Date Column:** `{date_col}`" if date_col else "**📅 Date Column:** ❌ Not found")
        st.write(f"**📝 Description Column:** `{desc_col}`" if desc_col else "**📝 Description Column:** ❌ Not found")
    with col2:
        if debit_col and credit_col:
            st.write(f"**💰 Debit Column:** `{debit_col}`")
            st.write(f"**💰 Credit Column:** `{credit_col}`")
        elif amount_col:
            st.write(f"**💰 Amount Column:** `{amount_col}`")
        else:
            st.write("**💰 Amount Column:** ❌ Not found")

    st.markdown("---")

    # =============================================
    # CLEAN BUTTON
    # =============================================
    if st.button("🧹 Clean My Data"):

        if not date_col:
            st.error("❌ Could not find a date column. Please check your CSV.")
            st.stop()

        # --- Parse Dates ---
        messy['_clean_date'] = messy[date_col].apply(parse_any_date)

        # --- Calculate Amount ---
        if debit_col and credit_col:
            debit_vals = pd.to_numeric(
                messy[debit_col].astype(str).str.replace(r'[,$()\s+]', '', regex=True),
                errors='coerce'
            ).fillna(0)
            credit_vals = pd.to_numeric(
                messy[credit_col].astype(str).str.replace(r'[,$()\s+]', '', regex=True),
                errors='coerce'
            ).fillna(0)
            messy['_clean_amount'] = credit_vals - debit_vals
        elif amount_col:
            messy['_clean_amount'] = pd.to_numeric(
                messy[amount_col].astype(str).str.replace(r'[,$()\s+]', '', regex=True),
                errors='coerce'
            ).fillna(0)
        else:
            st.error("❌ Could not find an amount column.")
            st.stop()

        # --- Description ---
        if desc_col:
            messy['_clean_desc'] = messy[desc_col].astype(str)
        else:
            messy['_clean_desc'] = "N/A"

        # =============================================
        # BUILD CLEAN DATAFRAME (Preserve ALL original columns)
        # =============================================
        used_cols = [date_col, desc_col, debit_col, credit_col, amount_col]
        used_cols = [c for c in used_cols if c is not None]

        extra_cols = [c for c in messy.columns if c not in used_cols and not c.startswith('_clean_')]

        clean = pd.DataFrame({
            'Date': messy['_clean_date'],
            'Description': messy['_clean_desc'],
            'Amount': messy['_clean_amount']
        })

        for col in extra_cols:
            clean[col] = messy[col].values

        # Drop rows where date parsing failed
        clean = clean.dropna(subset=['Date'])

        # Auto-sort by date (oldest to newest)
        clean = clean.sort_values('Date').reset_index(drop=True)

        st.subheader("✅ Your Clean Data")
        st.dataframe(clean)
        st.caption(f"Total rows cleaned: {len(clean)}")

        st.markdown("---")
        st.subheader("📥 Download Your Files")

        # Safe date conversion for QuickBooks
        clean['_qb_date'] = pd.to_datetime(clean['Date'], errors='coerce')
        qb = clean.dropna(subset=['_qb_date']).copy()
        qb['Date'] = qb['_qb_date'].dt.strftime('%m/%d/%Y')
        qb = qb.drop(columns=['_qb_date'])

        # Safe date conversion for Xero
        clean['_xero_date'] = pd.to_datetime(clean['Date'], errors='coerce')
        xero = clean.dropna(subset=['_xero_date']).copy()
        xero['Date'] = xero['_xero_date'].dt.strftime('%d/%m/%Y')
        xero = xero.rename(columns={'Description': 'Payee'})
        xero = xero.drop(columns=['_xero_date'])

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="📥 Download for QuickBooks",
                data=qb.to_csv(index=False),
                file_name="quickbooks_ready.csv",
                mime="text/csv"
            )

        with col2:
            st.download_button(
                label="📥 Download for Xero",
                data=xero.to_csv(index=False),
                file_name="xero_ready.csv",
                mime="text/csv"
            )

        st.success("🎉 Done! Your files are ready to import.")

st.markdown("---")
st.caption("Built by Biman Kalita | Accounting Automation Portfolio")
