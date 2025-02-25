import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS for black background
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: black;
        color: white;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: white;
    }
    .stTextInput, .stFileUploader {
        color: white;
    }
    div.stButton > button {
        background-color: #333333; /* Dark grey */
        color: white;
        border: 1px solid white;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #555555; /* Lighter grey on hover */
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Main Title
st.title("📈 Data Sweeper Integrator By Umer Iqbal")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization, for quarter 3.")

# File uploader
uploaded_files = st.file_uploader("📤 Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Read file into dataframe
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue
        
        st.subheader("👀 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Section
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"✅ Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🚫 Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates Removed ✅")
            
            with col2:
                if st.button(f"📊 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values filled ✅")
                    
            # Column Selection
            st.subheader("📑 Select Columns")
            columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]
            
            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"📈 Show Visualization for {file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
                
            # Conversion Options
            st.subheader("🔄 Conversion Options")
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            
            if st.button(f"⬇️ Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                buffer.seek(0)
                
                st.download_button(
                    label=f"📥 Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
                  
        st.success("✅ All files processed successfully!")
