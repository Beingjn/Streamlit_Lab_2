# Lab 2 — Data Connections (Public Google Sheet or CSV Upload)
# Scope: demonstrate two data-connection methods without authentication.
# 1) Public Google Sheet via URL (including a configured, fixed URL)
# 2) One-off CSV upload

import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Lab 2 — Data Connections", page_icon="2️⃣", layout="wide")
st.title("Lab 2 — Data Connections")
st.caption("Connect to a publicly accessible Google Sheet (CSV export) or upload a CSV.")

# Overview — common data connection methods in Streamlit
st.header("1.Overview of data connection methods")
st.markdown(
    """
**Typical options:**  
1. **Public files by URL** (CSV/Parquet) — e.g., Google Sheets (published or link-visible), GitHub raw links.  
2. **File upload** — `st.file_uploader` for ad-hoc, per-session files (no persistence on Community Cloud).  
3. **Databases** — Postgres, Snowflake, BigQuery, etc., with credentials stored in `st.secrets`.  
4. **Object storage** — S3/GCS/Azure Blob (CSV/Parquet) via URLs/SDKs, credentials in `st.secrets`.  
5. **Web APIs** — fetch JSON/CSV with a token in `st.secrets`.  
6. **Local files** — acceptable in local development; on Community Cloud, prefer small committed files or external sources.
"""
)

# Make a Google Sheet publicly accessible
st.header("2.Make a Google Sheet publicly accessible (CSV export)")
st.markdown(
    """
To read a Google Sheet, expose it as a **public CSV**:

**Method A — “Anyone with the link” (Viewer)**
1. In Google Sheets, select **Share** → set **Anyone with the link** to **Viewer**.  
2. Copy the browser URL (format: `https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit#gid=<GID>`).  
3. Create a CSV export URL in this form (replace the IDs):  
   `https://docs.google.com/spreadsheets/d/<SHEET_ID>/export?format=csv&gid=<GID>`

**Method B — Publish to the web (CSV)**
1. File → **Share** → **Publish to web**.  
2. Choose the **specific sheet (tab)** and **CSV** format, then copy the generated URL (often ends with `output=csv`).

> Use the **final CSV URL** in this app.
"""
)

# Configured data source
st.header("3.Configured CSV URL")
st.markdown(
    """
For small reference dashboards, it is acceptable to define a **fixed public CSV URL** in code.
Set the `CSV_URL` variable in the code to your sheet’s CSV export link.
"""
)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSAbs_1_H6dm93hdkIlg-z-Gm89_29Kv9ExaO7p0loMdrehE01-ex0gh5dSLFmeC9OtAANo0nkR243H/pub?gid=247290797&single=true&output=csv"  # Example: "https://docs.google.com/spreadsheets/d/ABC123/export?format=csv&gid=0"

df_csv = pd.read_csv(CSV_URL)
st.dataframe(df_csv.head(20))
st.write(f"Rows: **{len(df_csv):,}**  •  Columns: **{df_csv.shape[1]:,}**")

st.divider()

# Other data sources
st.header("4.Other data sources")
source = st.radio(
    "Select one option",
    ["Enter Google Sheet CSV URL", "Upload CSV"],
    horizontal=True
)

df = None

if source == "Enter Google Sheet CSV URL":
    url = st.text_input(
        "Public Google Sheet CSV URL",
        placeholder="https://docs.google.com/spreadsheets/d/.../export?format=csv&gid=0"
    )
    if url:
        try:
            df = pd.read_csv(url.strip())
            st.success("Loaded data from the provided CSV URL.")
        except Exception as e:
            st.error(f"Unable to read CSV from the provided URL. ({e})")

else:
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            st.success("Loaded data from the uploaded file.")
        except Exception as e:
            st.error(f"Unable to read the uploaded CSV. ({e})")

# Preview for user-selected source
if df is not None:
    st.subheader("Preview")
    st.write(f"Rows: **{len(df):,}**  •  Columns: **{df.shape[1]:,}**")
    st.dataframe(df.head(20), use_container_width=True)