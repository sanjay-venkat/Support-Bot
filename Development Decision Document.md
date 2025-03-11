---

#   Development Decision Documentation

This document outlines the key design choices, challenges, and refinements made during the development of the Customer Support Bot. The final implementation prioritizes accuracy, adaptability, and robustness while adhering to Python best practices. It also considers performance optimization for low-computation devices.

---

##   1. Document Processing & Training

**Objective:** Efficiently load, preprocess, and convert PDF/TXT documents into structured, retrievable sections.

###   Design Choices

* **PyPDF2 for PDFs:** Extracts raw text from PDFs efficiently, filtering empty pages.
* **Sentence-Based Splitting:** Uses `nltk.sent_tokenize` to split text into coherent segments, preserving context.
* **Optimized Token Limit Handling:** Sections are dynamically chunked to fit 512 tokens, ensuring compatibility with retrieval models.
* **SentenceTransformer Embeddings:** `all-MiniLM-L6-v2` was chosen for its balance between accuracy and speed.

###   Challenges & Solutions

* **Handling Large Documents:** A dynamic chunking strategy ensures that sections remain coherent while respecting model token limits.
* **Empty Documents:** Implemented strict validation to prevent processing unreadable or empty files, ensuring early failure detection.

---

##   2. Query Handling & Response Generation

**Objective:** Accurately retrieve and answer user queries using document-trained context.

###   Design Choices

* **Hybrid Retrieval (FAISS + TF-IDF)**
    * **FAISS (Semantic Search):** Uses L2 similarity search over sentence embeddings.
    * **TF-IDF (Keyword Matching):** Ensures recall of contextually relevant sections.
    * **Hybrid Selection:** FAISS is prioritized.

* **FLAN-T5 for Answer Generation**
    * The `google/flan-t5-large` model generates responses with strong contextual understanding.
    * Queries and contexts are formatted as: `question: <query> context: <retrieved_section>`
    * Dynamic Response Length: Adjusts based on query complexity.

###   Challenges & Solutions

* **Hallucinations & Irrelevant Responses:** Implemented a similarity threshold for FAISS to filter out irrelevant sections.
* **Token Limits:** The T5 model input is truncated to 512 tokens to prevent overflow errors.

---

##   3. Logging & Transparency

**Objective:** Provide clear and structured logs for debugging and evaluation.

###   Design Choices

* **Comprehensive Logging:** Key events (document loading, query handling, errors) are logged.
* **Structured Format:** Logs include timestamps, log levels, and execution details.
* **Noise Reduction:** Suppressed unnecessary logs (e.g., PyPDF2 warnings).

---

##   4. Robustness & Edge Cases

**Objective:** Ensure the bot handles unexpected inputs gracefully.

###   Design Choices

* **Fallback Responses:** If no relevant section is found, return "I don’t have enough information to answer that."
* **Exception Handling:** Uses `try-except` blocks for document processing, embedding creation, and response generation.
* **Hardware Compatibility:** The model runs on CPU, avoiding unnecessary GPU dependencies.

###   Challenges & Solutions

* **Index Corruption in FAISS:** Implemented an early exit strategy if embeddings fail.
* **Unsupported File Formats:** Returns an error message instead of crashing.

---

##   5. User Interface with Streamlit

**Objective:** Provide a clean, interactive web-based UI.

###   Design Choices

* **Streamlit for Web UI:**
    * File Upload: Supports PDFs and TXTs.
    * Query Input & Response Display: Provides an interactive chat-like experience.
    * **Feedback Buttons:** Users can mark responses as Helpful or Not Helpful, triggering refinements.
    * Conversation History: Allows users to view previous interactions.
    * **Input Handling:** Uses `st.form` with `clear_on_submit` to manage input and clear the text box after sending.

---

##   6. Performance Optimization for Low-Computational Devices

**Objective:** Ensure efficient execution on resource-limited hardware.

###   Design Choices

* **Optimized CPU Execution:**
    * `torch.set_num_threads(4)`: Limits CPU thread usage to avoid resource bottlenecks.
* **FAISS for Fast Retrieval:**
    * Provides fast similarity search without requiring a GPU.
* **Efficient Memory Management:**
    * Lazy model loading prevents unnecessary memory consumption.

###   Future Enhancements

* Quantization with `bitsandbytes` to reduce model size and improve latency.
* Smaller T5 variants (flan-t5-small or flan-t5-base) for faster inference.

---

##   7. Feedback Mechanism

**Objective:** Integrate user feedback to assess and potentially improve bot responses.

###   Design Choices

* **Streamlit Buttons:** 👍 (Thumbs Up) and 👎 (Thumbs Down) buttons are displayed after each bot response.
* **Session State Tracking:** `st.session_state.feedback` dictionary stores feedback for each message.
* **One Feedback Per Response:** The UI ensures that users can provide feedback only once for each bot response.
* **Logging:** User feedback (positive or negative) is logged with the corresponding message index.
* **UI Update:** `st.rerun()` is used to refresh the UI and reflect the feedback.

---

##   8. Future Improvements

1.  **Better Hybrid Retrieval:** Experiment with BM25 and dense vector re-ranking for more accurate section retrieval.
2.  **Multilingual Support:** Enable support for queries in multiple languages using `paraphrase-multilingual-MiniLM-L12-v2`.
3.  **Continuous Learning:** Implement a feedback-driven retraining loop.

---

##   9. Conclusion

The Customer Support Bot is a highly optimized, fast, accurate, and robust system capable of retrieving and answering user queries based on uploaded documents. The hybrid retrieval method, optimized CPU execution, and Streamlit UI integration with a feedback mechanism make it a user-friendly and scalable solution. Future enhancements will focus on real-time learning, multilingual support, and further efficiency optimizations.

---

##   10. GitHub Repository:

[Support-Bot](https://github.com/sanjay-venkat/Support-Bot)
