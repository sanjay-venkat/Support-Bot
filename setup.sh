#!/bin/bash
mkdir -p models
if [ ! -d "models/flan-t5-large" ]; then
    echo "Downloading FLAN-T5 model..."
    python3 -c "from transformers import T5ForConditionalGeneration, T5Tokenizer; \
                model = T5ForConditionalGeneration.from_pretrained('google/flan-t5-large'); \
                tokenizer = T5Tokenizer.from_pretrained('google/flan-t5-large'); \
                model.save_pretrained('models/flan-t5-large'); \
                tokenizer.save_pretrained('models/flan-t5-large')"
    echo "FLAN-T5 model downloaded successfully."
else
    echo "FLAN-T5 model already exists."
fi

if [ ! -d "models/all-MiniLM-L6-v2" ]; then
    echo "Downloading Sentence Transformer model..."
    python3 -c "from sentence_transformers import SentenceTransformer; \
                model = SentenceTransformer('all-MiniLM-L6-v2'); \
                model.save('models/all-MiniLM-L6-v2')"
    echo "Sentence Transformer model downloaded successfully."
else
    echo "Sentence Transformer model already exists."
fi

echo "Setup completed successfully."
