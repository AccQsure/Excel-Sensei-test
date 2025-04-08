
## 📊 Excel Sensei – Your LLM Agent for Spreadsheet Insights!!

Say hello to **Excel Sensei**... your new AI-powered companion that turns complex data into clear, actionable answers!

I've built a GenAI LLM app leveraging AI Agents that lets you simply upload your Excel file and ask questions in plain English. Excel Sensei uses advanced AI to analyze your data and provide instant insights.

🔗 **App URL**: [https://excel-sensei.streamlit.app](https://excel-sensei.streamlit.app)  
📺 **App Video Demo**: [Watch on YouTube](https://youtu.be/cxOOpmPXXyE?si=XKOtgLGr98XDAgAq)

---

### 💡 Why it Helps

Data analysis in Excel can be overwhelming — especially for non-technical users. With Excel Sensei, anyone can:

- ✅ Get quick insights from raw data  
- 🚫 Skip writing complex formulas or scripts  
- 🧹 Automatically clean datasets  
- 💬 Chat directly with their data using natural language

---

### 🛠️ Tech Stack

- **LangChain + Cohere LLM** – powers the pandas DataFrame AI Agent  
- **Streamlit** – for the interactive UI  
- **Pandas** – for DataFrame operations and cleaning  
- **Regex + validation checks** – ensures clean and usable input data

---

### 🔧 Code Structure & Workflow
```
Excel-Sensei/
│
├── main.py              # Main Streamlit app logic
├── requirements.txt     # Dependencies for the app
├── README.md            # Project documentation
└── .streamlit/
    └── secrets.toml     # Securely stores API keys
```

### 🧠 Workflow Overview

#### 1. Setup & Initialization
- Loads API keys and sets Streamlit page configuration  
- Initializes session state for chat and data tracking  

#### 2. Excel Upload & Cleaning
- Reads Excel file using `pandas.read_excel()`  
- Validates and cleans data (missing values, duplicates, etc.)  
- Stores cleaned dataset for chat-based exploration  

#### 3. AI Agent Creation
- Uses `create_pandas_dataframe_agent()` with **Cohere’s `command-r-plus`**  
- Powers natural language queries on uploaded Excel data  

#### 4. Interactive UI & Chat
- Chat interface to ask questions about the data  
- Agent responses appear in a conversational thread  
- Cleaned data preview and Excel download also available  

---

I'm excited to hear how **Excel Sensei** streamlines your data analysis workflows!  
💬 Share your experiences and questions in the comments.

---

**#LLM #GenAI #AIAgent #ExcelSensei #LangChain #DataAnalysis #AIinAction**
