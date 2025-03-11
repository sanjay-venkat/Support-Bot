# Support-Bot

This project implements a customer support bot that can answer questions based on the content of a given document.

## 📌 Description

The Support-Bot is designed to provide users with accurate responses extracted from a document. It leverages Large Language Models (FLAN-T5), embeddings (SentenceTransformers), and FAISS similarity search to process user queries efficiently.

The bot can be run in:

* Interactive Terminal Mode (CLI-based chat).
* Streamlit Web Interface (with chat history, feedback, and document upload).

## 🛠️ Setup

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/sanjay-venkat/Support-Bot](https://github.com/sanjay-venkat/Support-Bot)
    cd Support-Bot
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Download & Setup Models**

    The bot requires FLAN-T5, SentenceTransformer, and FAISS models.

    **Windows Users**

    Run the `setup.bat` script to automatically download the models:

    ```bash
    setup.bat
    ```

    **Linux/macOS Users**

    Run the `setup.sh` script:

    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

    ### ⚡ Optimized Model Loading

    Setup scripts will reuse existing models instead of downloading them repeatedly.

    This reduces setup time and ensures efficient model management.

---

## 🚀 Usage

1.  **Prepare your Document**

    Place the PDF or TXT file in the project directory.

    * For Terminal Mode: Name it `sample.pdf` or modify `document_path` in the script.
    * For Streamlit UI: Upload the document via the web interface.

2.  **Run the Bot**

    **A) Interactive Mode (Terminal)**

    ```bash
    python Support_Bot.py
    ```

    * The bot starts in an interactive CLI mode.
    * Type queries, and it will respond based on the document.
    * Type `exit` to quit.

    **B) Web Interface (Streamlit)**

    ```bash
    streamlit run app.py
    ```

    * Launches a chat-based UI with a typing box at the bottom.
    * Users can upload documents, send queries, and receive AI-generated responses.
    * Feedback system included: Users must rate responses before asking the next question.

---

## 📝 Example Interactions

**Interactive Mode (Terminal)**

Welcome to the Support Bot! Type 'exit' to quit.
You: What is the purpose of this document?
Bot: This document provides guidelines on information security policies.


**Streamlit Web Interface**

### 📌 Features:

* ✅ Bottom-centered chat input
* ✅ Chat messages appear above the input box
* ✅ Like/Dislike feedback system (only one feedback per bot response)

<img width="920" alt="image" src="https://github.com/user-attachments/assets/663ac492-b671-4c3b-9044-e8b1dc12e329" />


---

## 🔍 Features & Improvements

1.  **Hybrid Retrieval Mechanism**

    * FAISS + Keyword Matching: Enhances recall by combining vector similarity search with keyword-based retrieval.
    * Ensures highly relevant responses even for paraphrased queries.

2.  **Real User Feedback Integration**

    * Users must provide feedback (👍/👎) before asking a new question.
    * Feedback is logged for improving future responses.

3.  **Optimized Performance**

    * Supports CPU execution with fast inference times.
    * Uses efficient model loading to prevent redundant downloads.

4.  **Robust Query Handling**

    * Graceful error handling for unsupported or irrelevant queries.
    * Clear logging for debugging and improvement.

---

## 📁 Files & Structure

support-bot/

├── Support_Bot.py  # Main Python script containing the bot's logic

├── setup.sh      # Bash script to download necessary models (Linux/macOS)

├── setup.bat     # Batch script to download necessary models (Windows)

├── requirements.txt # List of Python dependencies

├── sample.pdf    # Sample PDF document for testing the bot

├── support_bot_log.txt # Log file recording bot's activity 

└── app.py        # Streamlit application script for the chat interface 

---

## 📌 Next Steps & Enhancements

* \[ \] Improve UI with response highlighting for better readability.
* \[ \] Enhance model fine-tuning based on collected user feedback.
* \[ \] Support multiple document uploads for expanded knowledge retrieval.

---

## 💡 Conclusion

The Support-Bot is a powerful AI-driven assistant designed for fast, accurate, and user-friendly document-based Q&A. 🚀

## 🔗 GitHub Repository:

[Support-Bot](https://github.com/sanjay-venkat/Support-Bot)
