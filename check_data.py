import streamlit as st
import pandas as pd

st.title("Data Column Checker")

# File Uploader

uploaded_file = st.file_uploader("Upload your TTC CSV", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.success(f"Loaded {len(df):,} rows")
    
    st.subheader("Columns Found:")
    col_list = df.columns.tolist()
    for col in col_list:
        st.write(f"- **{col}** (type: {df[col].dtype})")
    
    st.subheader("First 10 Rows:")
    st.dataframe(df.head(10))
    
    st.subheader("Sample Values from Key Columns:")
    
    # Check for columns you mentioned
    if 'delay_bin' in df.columns:
        st.write("**delay_bin unique values:**")
        st.write(df['delay_bin'].value_counts())
    
    if 'hour' in df.columns:
        st.write("**hour range:**", df['hour'].min(), "to", df['hour'].max())
    
    if 'weekday' in df.columns:
        st.write("**weekday unique values:**")
        st.write(df['weekday'].value_counts())
    
    if 'route' in df.columns:
        st.write("**route unique values (sample):**")
        st.write(df['route'].value_counts().head(10))
        
else:
    st.info("Upload your feature_engineered CSV file above")