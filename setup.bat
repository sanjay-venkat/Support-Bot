@echo off
setlocal

if not exist "models" mkdir models

if not exist "models\flan-t5-large" (
    echo Downloading FLAN-T5 model...
    python -c "from transformers import T5ForConditionalGeneration, T5Tokenizer; model = T5ForConditionalGeneration.from_pretrained('google/flan-t5-large'); tokenizer = T5Tokenizer.from_pretrained('google/flan-t5-large'); model.save_pretrained('models/flan-t5-large');tokenizer.save_pretrained('models/flan-t5-large')"
    echo FLAN-T5 model downloaded successfully.
) else (
    echo FLAN-T5 model already exists.
)

if not exist "models\all-MiniLM-L6-v2" (
    echo Downloading Sentence Transformer model...
    python -c "from sentence_transformers import SentenceTransformer;model = SentenceTransformer('all-MiniLM-L6-v2'); model.save('models/all-MiniLM-L6-v2')"
    echo Sentence Transformer model downloaded successfully.
) else (
    echo Sentence Transformer model already exists.
)

if not exist "tokenizers/punkt_tab" (
    echo download punkt....
    python -c "import nltk; nltk.download('punkt_tab')"
    echo punkt downloaded successfully.
) else (
    echo punkt already exists.
)

echo Setup completed successfully.
pause
