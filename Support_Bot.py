import logging  
import PyPDF2  
import nltk  
from nltk.tokenize import sent_tokenize  
from transformers import T5ForConditionalGeneration, T5Tokenizer  
from sentence_transformers import SentenceTransformer  
import faiss  
import numpy as np  
import torch  

# Download necessary data for sentence tokenization
nltk.download('punkt_tab')

# Set up logging  
logging.basicConfig(filename='support_bot_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  

class DocumentProcessor:  
    def __init__(self):  
        """Initialize the sentence embedding model."""  
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')  

    def load_document(self, path):  
        """Load and preprocess the document (PDF or TXT)."""  
        try:
            if path.endswith('.pdf'):  
                text = self._load_pdf(path)  
            elif path.endswith('.txt'):  
                text = self._load_txt(path)  
            else:  
                raise ValueError("Unsupported file format. Use PDF or TXT.")  

            if not text.strip():
                raise ValueError("Document is empty or unreadable.")

            logging.info(f"Successfully loaded document: {path}")
            return text
        except Exception as e:
            logging.error(f"Error loading document: {e}")
            return ""

    def _load_pdf(self, path):  
        """Extract text from a PDF file."""  
        try:
            with open(path, 'rb') as file:  
                reader = PyPDF2.PdfReader(file)  
                text = "\n".join([page.extract_text() or "" for page in reader.pages])  
            return text.strip()  
        except Exception as e:
            logging.error(f"Error reading PDF: {e}")
            return ""

    def _load_txt(self, path):  
        """Read text from a TXT file."""  
        try:
            with open(path, 'r', encoding='utf-8') as file:  
                return file.read().strip()  
        except Exception as e:
            logging.error(f"Error reading TXT file: {e}")
            return ""

    def split_text(self, text, max_tokens=512):  
        """Split text into sentence-based chunks to improve coherence."""  
        sentences = sent_tokenize(text)  
        chunks = []  
        current_chunk = []  
        current_length = 0  

        for sentence in sentences:  
            sentence_length = len(sentence.split())  
            if current_length + sentence_length > max_tokens:  
                chunks.append(" ".join(current_chunk))  
                current_chunk = []  
                current_length = 0  

            current_chunk.append(sentence)  
            current_length += sentence_length  

        if current_chunk:  
            chunks.append(" ".join(current_chunk))  

        logging.info(f"Split document into {len(chunks)} sections.")
        return chunks  

    def create_embeddings(self, sections):  
        """Create and normalize embeddings for document sections."""  
        try:
            embeddings = self.embedder.encode(sections, convert_to_tensor=True, normalize_embeddings=True)  
            return embeddings  
        except Exception as e:
            logging.error(f"Error generating embeddings: {e}")
            return None

class QueryHandler:  
    def __init__(self, sections, section_embeddings, embedder):  
        """Initialize the query processing pipeline."""  
        self.sections = sections  
        self.section_embeddings = section_embeddings  
        self.embedder = embedder  
        self.qa_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")  
        self.qa_tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")  
        self._create_faiss_index()  

    def _create_faiss_index(self):  
        """Create a FAISS index for fast similarity search."""  
        try:
            self.index = faiss.IndexFlatL2(self.section_embeddings.shape[1])  
            self.index.add(self.section_embeddings.cpu().numpy())  
            logging.info("FAISS index created successfully.")
        except Exception as e:
            logging.error(f"Error creating FAISS index: {e}")

    def find_relevant_section(self, query):  
        """Find the most relevant section using FAISS."""  
        try:
            query_embedding = self.embedder.encode(query, convert_to_tensor=True, normalize_embeddings=True)  
            query_embedding = query_embedding.cpu().numpy().reshape(1, -1)  
            distances, indices = self.index.search(query_embedding, k=1)  

            if indices[0][0] < len(self.sections):
                return self.sections[indices[0][0]]  
            return ""
        except Exception as e:
            logging.error(f"Error finding relevant section: {e}")
            return ""

    def answer_query(self, query):  
        """Generate a response using the T5 model."""  
        context = self.find_relevant_section(query)  
        if not context:  
            return "I don’t have enough information to answer that."  

        input_text = f"question: {query} context: {context}"  
        input_ids = self.qa_tokenizer(input_text, return_tensors="pt").input_ids  

        max_length = min(input_ids.shape[1], self.qa_model.config.n_positions)  
        input_ids = input_ids[:, :max_length]  

        outputs = self.qa_model.generate(input_ids, max_length=1000)  
        return self.qa_tokenizer.decode(outputs[0], skip_special_tokens=True)  

class FeedbackManager:  
    def get_feedback(self, response):  
        """Simulate feedback based on response quality."""  
        if len(response.split()) < 10:  
            return "too vague"  
        elif "don’t have enough information" in response:  
            return "not helpful"  
        else:  
            return "good"  

    def adjust_response(self, query, response, feedback, qa_model, qa_tokenizer):  
        """Refine the response based on feedback using T5 model."""  
        if feedback == "too vague" or feedback == "not helpful":  
            refinement_input = f"Refine: {query} Initial Response: {response}"  
            input_ids = qa_tokenizer(refinement_input, return_tensors="pt").input_ids  
            outputs = qa_model.generate(input_ids, max_length=100)  
            return qa_tokenizer.decode(outputs[0], skip_special_tokens=True)  
        return response  

class SupportBotAgent:  
    def __init__(self, document_path):  
        """Initialize the bot and load the document."""  
        self.document_processor = DocumentProcessor()  
        self.document_text = self.document_processor.load_document(document_path)  
        self.sections = self.document_processor.split_text(self.document_text)  
        self.section_embeddings = self.document_processor.create_embeddings(self.sections)  

        if self.section_embeddings is None:
            logging.error("Failed to generate embeddings. Exiting.")
            exit()

        self.query_handler = QueryHandler(self.sections, self.section_embeddings, self.document_processor.embedder)  
        self.feedback_manager = FeedbackManager()  
        logging.info(f"Loaded document: {document_path}")  

    def run(self):  
        """Run the bot in interactive mode."""  
        print("Welcome to the Customer Support Bot! Type 'exit' to quit.")  
        while True:  
            query = input("\nYou: ")  
            if query.lower() == "exit":  
                print("Bot: Goodbye!")  
                break  

            logging.info(f"Processing query: {query}")  
            response = self.query_handler.answer_query(query)  

            for _ in range(2):  
                feedback = self.feedback_manager.get_feedback(response)  
                if feedback == "good":  
                    break  
                response = self.feedback_manager.adjust_response(query, response, feedback, self.query_handler.qa_model, self.query_handler.qa_tokenizer)  

            print(f"Bot: {response}")  

if __name__ == "__main__":  
    document_path = "PDF or TXT file path"  
    bot = SupportBotAgent(document_path)  
    bot.run()
