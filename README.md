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
