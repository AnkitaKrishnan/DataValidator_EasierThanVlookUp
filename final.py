import streamlit as st
import pandas as pd

def main():
    st.title("Excel File Validator")

    uploaded_file = st.file_uploader("Upload Excel file", type="xlsx")

    if uploaded_file is not None:
        sheets = pd.ExcelFile(uploaded_file).sheet_names
        snv_sheet = st.selectbox("Select SNV table:", options=sheets, key="snv_sheet")
        other_sheet = st.selectbox("Select other table:", options=sheets, key="other_sheet")

        df_snv = pd.read_excel(uploaded_file, sheet_name=snv_sheet)
        df_other = pd.read_excel(uploaded_file, sheet_name=other_sheet)

        # st.subheader(f"Columns in {snv_sheet}:")
        # st.write(list(df_snv.columns))

        # st.subheader(f"Columns in {other_sheet}:")
        # st.write(list(df_other.columns))

        col1 = st.selectbox(f"Select column from {snv_sheet}:", options=list(df_snv.columns), key="col1")
        col2 = st.selectbox(f"Select column from {other_sheet}:", options=list(df_other.columns), key="col2")

        validate_data(df_snv[col1], df_other[col2], (snv_sheet, other_sheet))

def validate_data(col1, col2, selected_sheets):
    missing_entries_sheet1 = col2[~col2.isin(col1)]
    missing_entries_sheet2 = col1[~col1.isin(col2)]

    if len(missing_entries_sheet1) > 0:
        st.subheader("Missing entries:")
        st.write(f"Entries in {selected_sheets[0]} missing in {selected_sheets[1]}:")
        st.write(missing_entries_sheet1)
    elif len(missing_entries_sheet2) > 0:
        st.subheader("Missing entries:")
        st.write(f"Entries in {selected_sheets[1]} missing in {selected_sheets[0]}:")
        st.write(missing_entries_sheet2)
    else:
        st.subheader("No missing entries found!")
        st.write("😊")

if __name__ == "__main__":
    main()
