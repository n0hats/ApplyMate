from transformers import BertTokenizer, BertModel
import torch

# Load pre-trained BERT model and tokenizer
model = BertModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize and generate embeddings for the resume
inputs = tokenizer("Joshua Smith: Skills: Vulnerability Identification, Vulnerability Analysis, Detection Engineering",
                   return_tensors='pt', truncation=True)
with torch.no_grad():
    resume_embeddings = model(**inputs).last_hidden_state.mean(dim=1)
