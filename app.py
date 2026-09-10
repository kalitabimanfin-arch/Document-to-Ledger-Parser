import streamlit as st
import pandas as pd

# =============================================
# PAGE CONFIGURATION
# =============================================
st.set_page_config(page_title="Document-to-Ledger Parser", page_icon="📄")

st.title("📄 Document-to-Ledger Parser")
st.write("Upload a messy CSV file. Get clean files ready for QuickBooks or Xero.")

st.markdown("---")

# =============================================
# FILE UPLOADER
# =============================================
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the file
    messy = pd.read_csv(uploaded_file)

    st.subheader("📋 Your Messy Data")
    st.dataframe(messy)

    st.markdown("---")

    # Detect file type
    if 'Txn Date' in messy.columns:
        file_type = 'bank_statement'
        st.info("📊 Detected: Bank Statement")
    elif 'Invoice Date' in messy.columns:
        file_type = 'invoice'
        st.info("🧾 Detected: Invoice")
    else:
        st.error("❌ Unknown file format. Please upload a bank statement or invoice CSV.")
        st.stop()

    # Clean button
    if st.button("🧹 Clean My Data"):

        if file_type == 'bank_statement':
            # Normalize dates
            messy['Txn Date'] = pd.to_datetime(messy['Txn Date'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')

            # Merge Debit/Credit into single Amount
            messy['Amount'] = messy['Credit'].fillna(0) - messy['Debit'].fillna(0)

            clean = pd.DataFrame({
                'Date': messy['Txn Date'],
                'Description': messy['Details'],
                'Amount': messy['Amount']
            })

        elif file_type == 'invoice':
            # Normalize dates
            messy['Invoice Date'] = pd.to_datetime(messy['Invoice Date'], format='%b %d %Y').dt.strftime('%Y-%m-%d')

            clean = pd.DataFrame({
                'Invoice_Number': messy['Invoice No'],
                'Date': messy['Invoice Date'],
                'Vendor': messy['Vendor'],
                'Amount': messy['Total'],
                'Currency': messy['Currency']
            })

        st.subheader("✅ Your Clean Data")
        st.dataframe(clean)

        st.markdown("---")
        st.subheader("📥 Download Your Files")

        # QuickBooks format
        qb = clean.copy()
        if 'Date' in qb.columns:
            qb['Date'] = pd.to_datetime(qb['Date']).dt.strftime('%m/%d/%Y')

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="📥 Download for QuickBooks",
                data=qb.to_csv(index=False),
                file_name="quickbooks_ready.csv",
                mime="text/csv"
            )

        # Xero format
        xero = clean.copy()
        if 'Date' in xero.columns:
            xero['Date'] = pd.to_datetime(xero['Date']).dt.strftime('%d/%m/%Y')
        if 'Description' in xero.columns:
            xero = xero.rename(columns={'Description': 'Payee'})

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