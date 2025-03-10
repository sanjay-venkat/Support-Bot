# Support-Bot

This project implements a support bot that can answer questions based on the content of a given document.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/sanjay-venkat/Support-Bot
    cd Support-Bot
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Download models:**
    **WINDOWS**
    Run the `setup.bat` file to download the necessary models .

    ```bash
    setup.bat
    ```
    **LINUX**
    Run the `setup.sh` file to download the necessary models .
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```
    
    This will download the following models:

    * FLAN-T5 Large model
    * FLAN-T5 Large tokenizer
    * SentenceTransformer model (all-MiniLM-L6-v2)

## Usage

1.  **Prepare your document:**

    Place the document you want the bot to use in the same directory as the script. The document can be a PDF or TXT file.  Ensure the document is named "sample.pdf" or modify the `document_path` variable in `Support_Bot.py` to point to your document.

2.  **Run the bot:**

    ```bash
    python Support_Bot.py
    ```

3.  **Interact with the bot:**

    The bot will start in interactive mode. You can type your questions, and the bot will provide answers based on the content of the loaded document. Type `exit` to quit the bot.

## Example

Welcome to the Customer Support Bot! Type 'exit' to quit.

You: What is the purpose of this document?
Bot: This document provides information about information security risks.

## Logging

The bot's activity, including loading the document, processing queries, and any errors, will be logged in `support_bot_log.txt`. [cite: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

## Files

* `Support_Bot.py`: The main Python script containing the bot's logic.
* `setup.bat`:  A batch script to download necessary models.
* `requirements.txt`: A list of Python dependencies.
* `sample.pdf`: A sample PDF document for testing the bot.
* `support_bot_log.txt`: A log file记录 bot's activity. [cite: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
