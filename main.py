import streamlit as st
import pandas as pd
import os
from langchain_community.llms import Cohere
from langchain_experimental.agents import create_pandas_dataframe_agent
import re
from io import BytesIO


# Set Cohere API Key securely
cohere_api_key = st.secrets["COHERE_API_KEY"]
os.environ["COHERE_API_KEY"] = cohere_api_key


# Page configuration
st.set_page_config(
    page_title="Excel Sensei - Your AI Chat Companion for Excel Insights",
    page_icon="📊",
    # layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit UI
st.title("📊 Excel Sensei")
st.write("Ask questions about your Excel data and get instant insights — powered by AI.")

# How-To Guide
with st.expander("📚 How to Use This Tool"):
    st.markdown("""
    ### Getting Started with Your Data Analysis

    **Step 1: Upload Your Data**
    - Click the 'Browse files' button below
    - Select any Excel file (.xlsx or .xls)
    - Wait for the file to upload and process

    **Step 2: Explore Your Data**
    - Review the preview table to confirm your data loaded correctly
    - Check any warnings about missing values or duplicates

    **Step 3: Ask Questions About Your Data**
    - Type natural language questions in the chat box at the bottom
    - Be specific and refer to column names as they appear in your data
    - Wait for the AI to analyze and respond

    **Example Questions:**
    ```
    • What's the average value in [column]?
    • Which [category column] has the highest average [value column]?
    • Summarize this dataset in 5 bullet points
    • What are the top 3 values in [column]?
    ```

    **Step 4: Save Your Results**
    - Download the cleaned data for further analysis
    - Copy important insights from the chat

    **Troubleshooting Tips:**
    - If you get unexpected results, try rephrasing your question and start afresh.
    - For complex analyses, break down into simpler questions.
    - Make sure your Excel file doesn't contain merged cells or formatting issues.
    """)

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])


# Helper method for Cleaning text cols
def clean_dataframe_text(dataframe):
    """Cleans text columns in a DataFrame by stripping spaces and removing non-alphanumeric characters."""
    text_cols = dataframe.select_dtypes(include='object').columns
    for col in text_cols:
        dataframe[col] = dataframe[col].str.strip()  # Remove extra spaces
        dataframe[col] = dataframe[col].apply(
            lambda text: re.sub(r'[^\w\s.@%?$/-]', '', str(text)))  # Remove special characters
    return dataframe


# Cache data loading and cleaning
@st.cache_data
def load_and_clean_data(file):
    # Read the Excel file
    df = pd.read_excel(file)

    # Data Validation with improved error messages
    # 1. Check for Empty DataFrame
    if df.empty:
        st.error(
            "📛 The uploaded file doesn't contain any data. Please check that your Excel file has populated sheets.")
        return None

    numeric_cols = df.select_dtypes(include='number').columns
    print(f" Numeric Columns : {numeric_cols}")
    text_cols = df.select_dtypes(include='object').columns
    print(f" Text Columns : {text_cols}")

    # 2. Check for Missing Values
    missing_columns = df.columns[df.isnull().any()]
    if not missing_columns.empty:
        st.warning(
            f"⚠️ Missing values detected in columns: {', '.join(missing_columns)}. Cleaning the data by removing incomplete rows."
        )
        df.dropna(inplace=True)

    # 3. Check for Duplicate Rows
    if df.duplicated().any():
        duplicate_count = df.duplicated().sum()
        duplicate_percentage = (duplicate_count / len(df) * 100).round(1)
        st.warning(
            f"⚠️ Found {duplicate_count} duplicate rows ({duplicate_percentage}% of data). These will be dropped to prevent skewed analysis.")
        df.drop_duplicates(inplace=True)

    # Clean text columns
    # df = clean_dataframe_text(df)
    df.to_excel('cleaned_df.xlsx')  # Save cleaned data for review or download
    return df


# Initialize session state for chat history and Excel data
if "excel_data" not in st.session_state:
    st.session_state.excel_data = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Process uploaded file
if uploaded_file:
    # Load and clean the data
    df = load_and_clean_data(uploaded_file)

    # If data is invalid or incomplete after validation, return early
    if df is None:
        st.warning("Please resolve the issues in the dataset and upload again.")
    else:
        # Store Excel data in session state
        st.session_state.excel_data = df

        llm = Cohere(model="command-r-plus")

        agent = create_pandas_dataframe_agent(
            llm=llm,
            df=df,
            verbose=True,
            allow_dangerous_code=True,
            # handle_parsing_error=True,
            # handle_parsing_error= "No Answer",
            max_iterations=10
        )

        # Display cleaned data preview
        st.subheader("📋 DataFrame Preview")
        st.write(df.head())

        # Add download button for the cleaned data
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            st.session_state.excel_data.to_excel(writer, sheet_name='Cleaned_Data', index=False)

        st.download_button(
            label="📥 Download Cleaned Dataset Excel",
            data=buffer.getvalue(),
            file_name="cleaned_data.xlsx",
            mime="application/vnd.ms-excel"
        )

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Handle user query and agent response
        if prompt := st.chat_input("Ask about the Excel data..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("Analyzing..."):
                try:
                    # Query the agent for the response
                    response = agent.invoke(prompt)
                    # Extract only the output from the response dictionary
                    response_output = response.get('output',
                                                   response)  # If 'output' is present, use it, else display the full response
                except Exception as e:
                    if "OUTPUT_PARSING_FAILURE" in str(e):
                        response_output = "No Answer, Query not related to dataframe.. Pls try again."  # Instead of error, return this message in chat
                    else:
                        response_output = f"⚠️ Error: {str(e)}"

            with st.chat_message("assistant"):
                st.markdown(response_output)

            # Store the assistant's response
            st.session_state.messages.append({"role": "assistant", "content": response_output})

else:
    st.warning("Please upload an Excel file to proceed.")
