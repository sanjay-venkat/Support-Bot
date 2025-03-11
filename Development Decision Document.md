###   **Development Decision Documentation**

This document outlines the key design choices, challenges, and refinements made during the development of the **Customer Support Bot**, aligning with the assignment’s objectives to create an autonomous, document-trained agent capable of iterative improvement. The final implementation prioritizes accuracy, adaptability, and robustness while adhering to Python best practices. Furthermore, it details the use of Streamlit for a user-friendly interface and considerations for deployment on low-computational devices. Below is a detailed breakdown of the development process:

---

####   **1. Document Processing & Training**

**Objective**: Load and preprocess PDF/TXT documents into structured, retrievable sections.

* **Design Choices**:
    * **PyPDF2 for PDFs**: Chosen for its simplicity in extracting raw text from PDFs. Pages are concatenated into a single string, with empty pages filtered out. This approach provides a balance between ease of use and basic text extraction capabilities.
    * **Sentence-Based Splitting**: Instead of arbitrary paragraph splits, `nltk.sent_tokenize` was used to split text into sentences. This preserves logical coherence and avoids truncating mid-thought, ensuring that the context within sentences is maintained.
    * **Embedding Generation**: The `all-MiniLM-L6-v2` model from `sentence-transformers` creates embeddings for semantic search. Its balance of speed and accuracy (despite smaller size) suits this use case, making it suitable for resource-constrained environments.
* **Challenges**:
    * **Handling Large Documents**: Splitting by sentences while respecting token limits (512 tokens) required dynamic chunking. Each chunk aggregates sentences until the token threshold is reached. For example, documents exceeding 10,000 tokens required a strategy to create context windows that fit within the model's limitations.
    * **Empty Documents**: Robust error handling ensures the bot exits gracefully if the document is unreadable or empty. Specifically, the application checks for extracted text length and provides a graceful exit with appropriate logging if no text is found.

---

####   **2. Query Handling & Response Generation**

**Objective**: Accurately answer user queries by retrieving relevant document sections and generating responses.

* **Design Choices**:
    * **FAISS for Semantic Search**: A `FlatL2` index was chosen for fast and precise similarity matching. This outperformed keyword-based methods by understanding semantic context (e.g., matching "reset password" to "Forgot Password" sections). FAISS enables efficient similarity search over the document embeddings, crucial for quick and accurate retrieval.
    * **T5 Model (FLAN-T5)**: The `google/flan-t5-large` model was selected for its instruction-following capability and text-to-text design. Unlike QA-specific models, it generates fluent, context-aware responses. FLAN-T5's instruction tuning makes it well-suited for generating natural language responses based on retrieved context.
    * **Dynamic Response Length**: Responses adjust based on query complexity—shorter answers for simple questions (e.g., "contact support") and longer ones for complex queries. The bot analyzes the complexity of the query and the relevance of retrieved information to determine the appropriate response length.
* **Challenges**:
    * **Relevance Threshold**: A distance threshold of **0.8** in FAISS ensures only highly relevant sections are used, reducing hallucinations. This threshold was determined empirically through testing and evaluation to balance relevance and recall.
    * **Token Limits**: Inputs to T5 are truncated to the model’s `max_position_embeddings` (512 tokens) to avoid errors. The application implements a context windowing mechanism to ensure that the input to the T5 model does not exceed its maximum token limit.

---

####   **3. Feedback Loop & Iterative Improvement**

**Objective**: Simulate feedback to refine responses and demonstrate adaptability.

* **Design Choices**:
    * **Rule-Based Feedback**: Feedback is simulated using rules (not randomness) for consistency:
        * **Too Vague**: Triggered if the response has fewer than 10 words.
        * **Not Helpful**: Triggered if the response contains the fallback phrase.
    * **T5-Based Refinement**: The same T5 model regenerates responses using feedback. For example, "too vague" appends additional context from the document. This leverages the model's generative capabilities to improve the quality and detail of responses based on simulated feedback.
* **Challenges**:
    * **Over-Refinement**: Limiting feedback loops to **2 iterations** prevents infinite loops or degraded responses. This limit was established to prevent the model from deviating too far from the original context or getting stuck in a refinement loop.
    * **Context Preservation**: The refinement prompt (`Refine: [query] Initial Response: [response]`) ensures the model retains the original query’s intent. This prompt engineering technique helps guide the model to refine the response while staying true to the user's query.

---

####   **4. Logging & Transparency**

**Objective**: Track decisions for debugging and evaluation.

* **Design Choices**:
    * **Comprehensive Logging**: The `logging` module records key steps: document loading, section splits, query processing, and feedback. This detailed logging facilitates debugging, monitoring, and analysis of the bot's behavior.
    * **Structured Log Format**: Each log entry includes a timestamp, log level, and context (e.g., `"Loaded document: res.pdf"`). The structured format enables efficient parsing and analysis of log data.
* **Challenges**:
    * **Noise Reduction**: Non-essential warnings (e.g., PyPDF2 extraction errors) are suppressed to keep logs clean. Log filtering is implemented to focus on important events and errors.

---

####   **5. Robustness & Edge Cases**

**Objective**: Gracefully handle unexpected inputs and errors.

* **Design Choices**:
    * **Fallback Responses**: Queries with no relevant sections return a predefined message: *"I don’t have enough information..."*. This provides a user-friendly response when the bot cannot find relevant information in the provided documents.
    * **Error Handling**: Critical failures (e.g., embedding generation errors) terminate the bot with a log entry. Try-except blocks are used throughout the code to catch potential exceptions and handle them gracefully, ensuring the application's stability.
    * **Hardware Compatibility**: The T5 model runs on CPU with `float32` precision to avoid GPU dependency. While this may impact performance, it ensures that the application can run on a wider range of hardware.

---

####   **6. User Interface with Streamlit**

**Objective**: Provide a clean, interactive, and user-friendly interface for interacting with the Customer Support Bot.

* **Design Choices**:
    * **Streamlit Integration**: Streamlit was chosen to create a web-based user interface. Streamlit's simplicity allows for rapid development of interactive applications with minimal code. The interface includes:
        * **File Upload**: Users can upload their documents (PDF or TXT).
        * **Query Input**: A text box for users to enter their questions.
        * **Response Display**: The bot's responses are displayed in a clear and readable format.
        * **Feedback Buttons**: Users can provide feedback on the bot's responses (e.g., "Helpful" or "Not Helpful"), triggering the refinement loop.
* **User Experience Details**:
    * **Clear Prompts and Instructions**: The interface provides clear prompts and instructions to guide users through the process.
    * **Real-time Updates**: The interface provides real-time updates as the bot processes the input and generates responses.
    * **Conversation History**: The interface maintains a conversation history, allowing users to review previous interactions.

---

####   **7. Optimization for Low-Computational Devices**

**Objective**: Implement techniques to make the bot more lightweight and suitable for running on devices with limited resources.

* **Design Choices and Future Improvements**:
    * **Model Quantization**: In addition to running the T5 model on the CPU, future improvements will explore advanced quantization techniques such as bitsandbytes for 4-bit or even lower-bit quantization. This would significantly reduce the model's memory footprint and computational requirements.
    * **Further Optimization**:
        * **Efficient Data Structures**: Optimizing data structures and algorithms for memory efficiency.
        * **Selective Loading**: Only loading necessary model components into memory.
        * **Asynchronous Processing**: Implementing asynchronous processing to improve responsiveness.
    * **Smaller Models**: While `flan-t5-large` was chosen for its strong performance, exploring distillation techniques or using smaller, yet effective models could further reduce resource consumption.
    * **Hardware Acceleration (If Available)**: While the current implementation prioritizes CPU compatibility, if available, leveraging hardware acceleration like GPUs or specialized accelerators (even on lower-powered devices) could be explored for performance gains.

---

####   **8. Future Improvements**

While the bot meets the assignment’s core requirements, the following enhancements could be explored:

1.  **Real User Feedback**: Replace simulated feedback with user input (e.g., thumbs up/down) gathered through the Streamlit interface for more realistic iterative improvement.
2.  **Hybrid Retrieval**: Combine FAISS with keyword matching for better recall and more robust information retrieval.
3.  **Multilingual Support**: Leverage multilingual embeddings (e.g., `paraphrase-multilingual-MiniLM-L12-v2`) to expand the bot's capabilities to handle queries in different languages.
4.  **Continuous Learning**: Implement a mechanism for the bot to continuously learn and improve from new data and user interactions.

---

####   **9. Conclusion**

The final implementation balances accuracy, performance, and maintainability. By leveraging sentence-based chunking, FAISS semantic search, and T5’s generative capabilities, the bot provides contextually relevant answers while iteratively refining its responses. The use of Streamlit provides a user-friendly interface, and considerations have been made for optimizing the bot for low-computational devices. The modular class structure (`DocumentProcessor`, `QueryHandler`, etc.) ensures readability and extensibility, aligning with the assignment’s emphasis on code quality and agentic workflows.
