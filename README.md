#   Support-Bot

This project implements a support bot that can answer questions based on the content of a given document.

##   Description

The Support-Bot is designed to provide users with information extracted from a document. It utilizes natural language processing (NLP) techniques to understand user queries and provide relevant answers. The bot can be run in an interactive terminal mode or through a Streamlit web interface for a more user-friendly experience.

##   Setup

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/sanjay-venkat/Support-Bot](https://github.com/sanjay-venkat/Support-Bot)
    cd Support-Bot
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Download models:**

    **Windows**

    Run the `setup.bat` file to download the necessary models.

    ```bash
    setup.bat
    ```

    **Linux/macOS**

    Run the `setup.sh` file to download the necessary models.

    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

    This will download the following models:

    * FLAN-T5 Large model
    * FLAN-T5 Large tokenizer
    * SentenceTransformer model (all-MiniLM-L6-v2)

##   Usage

1.  **Prepare your document:**

    Place the document you want the bot to use in the same directory as the script. The document can be a PDF or TXT file.

    * For the terminal application (`Support_Bot.py`), you can either name your document `sample.pdf` or modify the `document_path` variable in the script to point to your document.
    * For the Streamlit application (`app.py`), you can upload your document through the interface.

2.  **Run the bot:**

    You can run the bot in two ways:

    **a) Interactive Mode (Terminal):**

    ```bash
    python Support_Bot.py
    ```

    The bot will start in interactive mode. You can type your questions, and the bot will provide answers based on the content of the loaded document. Type `exit` to quit the bot.

    **b) Streamlit Interface:**

    ```bash
    streamlit run app.py
    ```

    This will launch a web interface in your browser. You can interact with the bot through the chat interface.

##   Example

**Interactive Mode (Terminal):**

Welcome to the Customer Support Bot! Type 'exit' to quit.

You: What is the purpose of this document?
Bot: This document provides information about information security risks.

**Streamlit Interface:**

*(A screenshot of the Streamlit interface would be very helpful here in your README!)*

##   Files

* `Support_Bot.py`: The main Python script containing the bot's logic for processing documents, handling queries, and generating responses in the terminal.
* `app.py`: The Streamlit application script for creating the interactive chat interface in a web browser, allowing users to upload documents and interact with the bot.
* `setup.bat`: A batch script for Windows to automate the download of necessary models.
* `setup.sh`: A shell script for Linux/macOS to automate the download of necessary models.
* `requirements.txt`: A list of Python dependencies required to run the project.
* `sample.pdf`: A sample PDF document provided for testing the bot's functionality.
* `support_bot_log.txt`: A log file that records the bot's activity, including document loading, query processing, and errors.
* `Development Decision Document.md`: This document outlines the key design choices, challenges, and refinements made during the development of the Support-Bot.
* `README.md`: The main file providing information and instructions about the Support-Bot project.
* `Sample_Queries.txt`: A text file containing sample queries that can be used to test the bot.
