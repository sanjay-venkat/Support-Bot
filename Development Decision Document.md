---

##   Development Decision Documentation

This document details the critical design choices, challenges, and refinements made during the development of the Customer Support Bot, ensuring an autonomous, document-trained agent capable of iterative improvement. The final implementation prioritizes accuracy, adaptability, and robustness while adhering to Python best practices. Additionally, the bot is designed to be efficient for low-computational environments and provides a user-friendly interface using Streamlit.

---

##   1. Document Processing & Training

###   Objective

Load and preprocess PDF/TXT documents into structured, retrievable sections.

###   Design Choices

* **PyPDF2 for PDFs:** Extracts raw text efficiently, handling multi-page documents while filtering out empty pages.
* **Sentence-Based Splitting (nltk.sent_tokenize):** Maintains logical coherence by splitting text at sentence boundaries rather than arbitrary chunks.
* **Embedding Generation (all-MiniLM-L6-v2):** A fast, lightweight model chosen for efficient sentence embeddings, ensuring low latency retrieval and compatibility with resource-constrained devices.

###   Challenges & Solutions

* **Handling Large Documents**

    * **Dynamic Chunking:** Sentences are aggregated into chunks, ensuring each remains under 512 tokens (T5’s input limit). If a single sentence exceeds the token limit, it is split into smaller chunks.
    * **Memory Optimization:** Processing occurs in batches to avoid high RAM usage.
* **Empty Document Handling**

    * **Graceful Exit:** If no readable text is extracted, the bot logs an error and informs the user.

---

##   2. Query Handling & Response Generation

###   Objective

Accurately answer user queries by retrieving the most relevant document sections and generating context-aware responses.

###   Design Choices

* **FAISS for Semantic Search (IndexFlatL2)**

    * Faster and more accurate than keyword search, enabling efficient document retrieval.
    * Normalized embeddings improve retrieval accuracy by ensuring cosine similarity is correctly measured.
* **FLAN-T5 (Large)**

    * Strong instruction-following capabilities make it better suited for answering user queries contextually.
    * Text-to-Text Framework allows better adaptability in generating responses.
* **Dynamic Response Length**

    * Short Responses for Simple Queries (e.g., "contact support").
    * Longer Responses for Complex Queries, ensuring that the bot does not over-explain straightforward questions.

###   Challenges & Solutions

* **Relevance Threshold**

    * A 0.8 similarity threshold (determined through experimentation) ensures only highly relevant document sections are used, preventing hallucinations.
* **Token Limits & Truncation**

    * Input to FLAN-T5 is truncated to 512 tokens for efficiency while ensuring sufficient context is included.

---

##   3. Feedback Loop & Iterative Refinement

###   Objective

Improve responses using a structured feedback system.

###   Design Choices

* **Real User Feedback via Streamlit**

    * Users provide thumbs up/down, triggering real-time refinement instead of simulated feedback.
    * Feedback is stored to a log file for potential future analysis and model improvement.
* **Feedback-Based Refinement with FLAN-T5**

    * If feedback is "too vague" or "not helpful", the bot generates a refined response by appending additional context.

###   Challenges & Solutions

* **Preventing Over-Refinement**

    * Refinement is limited to 2 iterations to prevent infinite loops or excessive verbosity.
* **Context Preservation**

    * The prompt format ensures the model retains original query intent:

        * `Refine: [query] Initial Response: [response]`

---

##   4. Logging & Transparency

###   Objective

Ensure clear debugging and evaluation of the bot’s decision-making process.

###   Design Choices

* **Comprehensive Logging (logging module)**

    * Logs key steps like document loading, section splits, query processing, and feedback application.
* **Structured Log Format**

    * Includes timestamp, log level, and message context (e.g., "Loaded document: res.pdf").
* **Noise Reduction**

    * Suppresses irrelevant warnings (e.g., PyPDF2 extraction errors), keeping logs clean.

---

##   5. Robustness & Edge Case Handling

###   Objective

Ensure stability and reliability when handling unexpected inputs.

###   Design Choices

* **Fallback Responses for Unanswerable Queries**

    * Returns "I don’t have enough information to answer that." when no relevant section is found.
* **Error Handling for Critical Failures**

    * Try-except blocks catch and log embedding generation errors, document parsing failures, and model loading issues.
    * Example: If the document fails to load, the user sees an error message: "Document could not be loaded."
* **Hardware Compatibility Enhancements**

    * The T5 model runs on CPU with float32 precision, ensuring the bot can run on standard hardware without requiring specialized GPUs, increasing accessibility.

---

##   6. User Interface with Streamlit

###   Objective

Provide an interactive and user-friendly web-based interface.

###   Design Choices

* **Streamlit-Based Interface**

    * **File Upload:** Allows users to upload PDF or TXT documents.
    * **Query Input:** A simple text box for user queries.
    * **Response Display:** Bot responses are formatted clearly.
    * **Feedback Buttons:** Users can provide feedback (Helpful/Not Helpful), triggering real-time refinement.
    * **Conversation History:** Allows users to review past queries and responses.

###   Challenges & Solutions

* **Ensuring Clear User Guidance**

    * The UI provides step-by-step instructions to guide users on uploading files and querying.
* **Real-Time Updates**

    * The UI updates in real time as the bot generates responses.

---

##   7. Optimization for Low-Computational Devices

###   Objective

Optimize the bot for fast performance on CPUs and reduce memory footprint.

###   Design Choices & Future Enhancements

* **Model Quantization (Planned)**

    * Use bitsandbytes for 4-bit quantization, reducing memory footprint without sacrificing accuracy.
* **Efficient Data Structures**

    * Optimize embeddings storage and document indexing for speed.
* **Selective Model Loading**

    * Modify setup.bat to reuse downloaded models instead of redownloading on every run.
* **Asynchronous Processing (Planned)**

    * Implement async operations for faster response times.

---

##   8. Future Enhancements

While the bot meets core assignment requirements, several enhancements are planned:

1.  **Hybrid Retrieval:**

    * Combine FAISS with keyword-based matching to improve recall.

2.  **Multilingual Support:**

    * Use paraphrase-multilingual-MiniLM-L12-v2 to handle queries in different languages.

3.  **Adaptive Learning Mechanism:**

    * Implement continuous learning from user feedback to improve responses over time.

4.  **Performance Profiling & Speed Optimization:**

    * Profile execution times and optimize query retrieval speed further.

---

##   9. Conclusion

The Customer Support Bot successfully balances accuracy, efficiency, and usability by leveraging:

* Sentence-based chunking for logical text segmentation.
* FAISS similarity search for fast and precise document retrieval.
* FLAN-T5’s generative capabilities for coherent and context-aware responses.
* Streamlit for an intuitive user interface.
* Optimizations for CPU execution to ensure wider accessibility.

The modular class structure (DocumentProcessor, QueryHandler, FeedbackManager) enhances maintainability and extensibility, making the bot adaptable for real-world deployment.
