@echo off
echo Downloading models for faster execution...
python -c "from transformers import T5ForConditionalGeneration; T5ForConditionalGeneration.from_pretrained('google/flan-t5-large')"
python -c "from transformers import T5Tokenizer; T5Tokenizer.from_pretrained('google/flan-t5-large')"
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

echo All models downloaded successfully!
pause
