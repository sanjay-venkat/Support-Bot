import logging
import os
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
from transformers import T5ForConditionalGeneration, T5Tokenizer
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Optimize CPU execution
torch.set_num_threads(4)  # Adjust as needed

# Download necessary data for sentence tokenization
if not nltk.data.find('tokenizers/punkt_tab'):
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

        # Hybrid retrieval: FAISS + TF-IDF
        self._create_faiss_index()
        self.tfidf_vectorizer = TfidfVectorizer().fit(sections)
        self.tfidf_matrix = self.tfidf_vectorizer.transform(sections)

    def _create_faiss_index(self):
        """Create a FAISS index for fast similarity search."""
        try:
            self.index = faiss.IndexFlatL2(self.section_embeddings.shape[1])
            self.index.add(self.section_embeddings.cpu().numpy())
            logging.info("FAISS index created successfully.")
        except Exception as e:
            logging.error(f"Error creating FAISS index: {e}")

    def find_relevant_section(self, query):
        """Find the most relevant section using FAISS and keyword matching."""
        query_embedding = self.embedder.encode(query, convert_to_tensor=True, normalize_embeddings=True).cpu().numpy()
        _, faiss_indices = self.index.search(query_embedding.reshape(1, -1), k=1)

        # TF-IDF keyword matching
        query_tfidf = self.tfidf_vectorizer.transform([query])
        cosine_similarities = cosine_similarity(query_tfidf, self.tfidf_matrix).flatten()
        tfidf_index = np.argmax(cosine_similarities)

        # Hybrid selection: prioritize FAISS but use TF-IDF as fallback
        faiss_section = self.sections[faiss_indices[0][0]]
        tfidf_section = self.sections[tfidf_index]

        return faiss_section if cosine_similarities[tfidf_index] < 0.5 else tfidf_section

    def answer_query(self, query):
        """Generate a response using the T5 model."""
        context = self.find_relevant_section(query)
        if not context:
            return "I don’t have enough information to answer that."

        input_text = f"question: {query} context: {context}"
        input_ids = self.qa_tokenizer(input_text, return_tensors="pt").input_ids[:, :512]  # Limit token length

        outputs = self.qa_model.generate(input_ids, max_length=150)
        return self.qa_tokenizer.decode(outputs[0], skip_special_tokens=True)


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
        logging.info(f"Loaded document: {document_path}")

if __name__ == "__main__":
    import sys

    # Check if a document path is provided
    document_path = "sample.pdf"  # Replace with an actual document path
    if not os.path.exists(document_path):
        print(f"Error: Document '{document_path}' not found.")
        sys.exit(1)

    # Initialize the bot
    bot = SupportBotAgent(document_path)

    print("\nCustomer Support Bot (Type 'exit' to quit)")
    while True:
        user_query = input("\nYou: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = bot.query_handler.answer_query(user_query)
        print(f"Bot: {response}")
