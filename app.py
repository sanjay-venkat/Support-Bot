from flask import Flask, render_template, request, jsonify
from Support_Bot import SupportBotAgent
import logging

app = Flask(__name__)
bot = None  # Initialize bot outside of route

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global bot
    if bot is None:  # Initialize bot on first request
        try:
            document_path = "sample.pdf"  # Or you can make this configurable
            bot = SupportBotAgent(document_path)
            logging.info("Support bot initialized.")
        except Exception as e:
            logging.error(f"Error initializing bot: {e}")
            return jsonify({"response": "Error initializing bot. Please try again later."}), 500

    query = request.form['query']
    logging.info(f"Received query: {query}")
    try:
        response = bot.query_handler.answer_query(query)
        logging.info(f"Bot's response: {response}")
        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"Error processing query: {e}")
        return jsonify({"response": "Error processing query. Please try again."}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Basic logging
    app.run(debug=True)
