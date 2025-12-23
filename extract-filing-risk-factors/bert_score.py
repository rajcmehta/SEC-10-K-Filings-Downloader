from store_risk_factors import get_dataframe
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import pandas as pd
import math


df = get_dataframe()

finbert_model = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(finbert_model)
model = AutoModelForSequenceClassification.from_pretrained(finbert_model)
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def chunk_text_tokens(text, max_tokens=500):
    if not isinstance(text, str) or text.strip() == "":
        return []
    tokens = tokenizer.encode(text, truncation=False)
    chunks = [tokens[i:i+max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.decode(chunk, skip_special_tokens=True, clean_up_tokenization_spaces=True) for chunk in chunks]

def get_financial_sentiment(text):
    chunks = chunk_text_tokens(text)
    if not chunks:
        return None, None
    
    label_to_value = {'positive': 1, 'neutral': 0, 'negative': -1}
    
    contributions = []
    label_scores = {'positive': [], 'neutral': [], 'negative': []}
    
    for chunk in chunks:
        result = sentiment_analyzer(chunk)[0]
        label = result['label'].lower()
        score = result['score']
        contributions.append(label_to_value[label] * score)
        label_scores[label].append(score)
    
    continuous_score = sum(contributions) / len(contributions)
    
    avg_scores = {k: sum(v)/len(v) if v else 0 for k,v in label_scores.items()}
    discrete_label = max(avg_scores, key=avg_scores.get)
    
    return discrete_label, continuous_score

df[['sentiment_label', 'continuous_sentiment']] = df['item_1A'].apply(
    lambda x: pd.Series(get_financial_sentiment(x))
)

print(df[['company', 'ticker', 'sentiment_label', 'continuous_sentiment']])