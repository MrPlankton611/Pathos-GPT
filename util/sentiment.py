from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

def compute_sentiment(message):
    tokens = tokenizer.encode(message, return_tensors='pt')
    result = model(tokens)
    sentiment_score = int(torch.argmax(result.logits))+1
    return sentiment_score