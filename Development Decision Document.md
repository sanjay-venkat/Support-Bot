---

## Development Decision Documentation

This document outlines the key design choices, challenges, and refinements made during the development of the Customer Support Bot. The final implementation prioritizes accuracy, adaptability, and robustness while adhering to Python best practices. It also considers performance optimization for resource-constrained environments.

---

## 1. Document Processing & Training

**Objective:** Efficiently load, preprocess, and convert PDF/TXT documents into structured, retrievable sections.

### Design Choices

* **PyPDF2 for PDFs:** Extracts raw text from PDFs efficiently, filtering empty pages.
* **Sentence-Based Splitting:** Uses `nltk.sent_tokenize` to split text into coherent segments, preserving context.
* **Optimized Token Limit Handling:** Sections are dynamically chunked to fit within a 512-token limit, ensuring compatibility with retrieval models.
* **SentenceTransformer Embeddings:** `all-MiniLM-L6-v2` was chosen for its balance between accuracy and speed.

### Challenges & Solutions

* **Handling Large Documents:** A dynamic chunking strategy ensures that sections remain coherent while respecting model token limits.
* **Empty Documents:** Implemented strict validation to prevent processing unreadable or empty files, ensuring early failure detection.

---

## 2. Query Handling & Response Generation

**Objective:** Accurately retrieve and answer user queries using document-trained context.

### Design Choices

* **Hybrid Retrieval (FAISS + TF-IDF)**
    * **FAISS (Semantic Search):** Uses L2 similarity search over sentence embeddings.
    * **TF-IDF (Keyword Matching):** Ensures recall of contextually relevant sections.
    * **Hybrid Selection:** FAISS is prioritized, with TF-IDF used as a fallback when the cosine similarity is below 0.5.
* **FLAN-T5 for Answer Generation**
    * The `google/flan-t5-large` model generates responses with strong contextual understanding.
    * Queries and contexts are formatted as: `question: <query> context: <retrieved_section>`
    * **Dynamic Response Length:** Adjusts based on query complexity.

### Challenges & Solutions

* **Hallucinations & Irrelevant Responses:** Implemented a similarity threshold (0.5) for FAISS to filter out less relevant sections.
* **Token Limits:** The T5 model input is truncated to 512 tokens to prevent overflow errors.

---

## 3. Logging & Transparency

**Objective:** Provide clear and structured logs for debugging and evaluation.

### Design Choices

* **Comprehensive Logging:** Key events (document loading, query handling, errors) are logged.
* **Structured Format:** Logs include timestamps, log levels, and execution details.
* **Noise Reduction:** Suppressed unnecessary logs (e.g., PyPDF2 warnings).

---

## 4. Robustness & Edge Cases

**Objective:** Ensure the bot handles unexpected inputs gracefully.

### Design Choices

* **Fallback Responses:** If no relevant section is found, return "I don’t have enough information to answer that."
* **Exception Handling:** Uses `try-except` blocks for document processing, embedding creation, and response generation.
* **Hardware Compatibility:** The model runs on CPU using `float32` precision, avoiding unnecessary GPU dependencies.

### Challenges & Solutions

* **FAISS Index Issues:** Implemented an early exit strategy if embeddings fail.
* **Unsupported File Formats:** Returns an error message instead of crashing.

---

## 5. User Interface with Streamlit

**Objective:** Provide a clean, interactive web-based UI.

### Design Choices

* **Streamlit for Web UI:**
    * **File Upload:** Supports PDFs and TXTs.
    * **Query Input & Response Display:** Provides an interactive chat-like experience.
    * **Feedback Buttons:** Users can mark responses as "Helpful" or "Not Helpful," triggering refinements.
    * **Conversation History:** Allows users to view previous interactions.

---

## 6. Performance Optimization for Resource-Constrained Environments

**Objective:** Ensure efficient execution on resource-limited hardware.

### Design Choices

* **Optimized CPU Execution:**
    * `torch.set_num_threads(4)`: Limits CPU thread usage to avoid resource bottlenecks.
* **FAISS for Fast Retrieval:**
    * Provides fast similarity search without requiring a GPU.
* **Efficient Memory Management:**
    * Lazy model loading prevents unnecessary memory consumption.

### Future Enhancements

* Quantization with `bitsandbytes` to reduce model size and improve latency.
* Smaller T5 variants (`flan-t5-small` or `flan-t5-base`) for faster inference.

---

## 7. Future Improvements

1.  **Real User Feedback:** Replace simulated feedback with Streamlit thumbs up/down for real-time response improvement.
2.  **Better Hybrid Retrieval:** Experiment with BM25 and dense vector re-ranking for more accurate section retrieval.
3.  **Multilingual Support:** Enable support for queries in multiple languages using `paraphrase-multilingual-MiniLM-L12-v2`.
4.  **Continuous Learning:** Implement a feedback-driven retraining loop.

---

## 8. Conclusion

The Customer Support Bot is a highly optimized, fast, accurate, and robust system capable of retrieving and answering user queries based on uploaded documents. The hybrid retrieval method, optimized CPU execution, and Streamlit UI integration make it a user-friendly and scalable solution. Future enhancements will focus on real-time learning, multilingual support, and further efficiency optimizations.

---

## 🔗 GitHub Repository:

[Support-Bot](https://github.com/sanjay-venkat/Support-Bot)
