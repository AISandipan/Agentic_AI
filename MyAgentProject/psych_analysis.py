#INSIGHTIFY!!
from transformers import pipeline
import re
from collections import Counter
import nltk

nltk.download('punkt')
'''This tokenizer in NLTK divides a text into a list of sentences by using an unsupervised algorithm to build
a model for abbreviation words, collocations, and words that start sentences.
It must be trained on a large collection of plaintext in the target language before it can be used.'''

# Sentiment model
sentiment_analyzer = pipeline("sentiment-analysis")

# -------- MAIN FUNCTION --------
def analyze_psychology(text):

    #SENTIMENT --------
    sentiment = sentiment_analyzer(text[:512])[0]

    #CLEAN TEXT --------
    words = re.findall(r'\b\w+\b', text.lower())

    stopwords = ["the","is","and","in","to","of","a","i","it","that"]
    words = [w for w in words if w not in stopwords]

    # KEY THEMES --------
    freq = Counter(words)
    keywords = freq.most_common(8)

    #PSYCHOLOGICAL PATTERNS --------
    patterns = []

    if any(word in words for word in ["sad","empty","lonely","tired"]):
        patterns.append("Possible low mood / emotional distress")

    if any(word in words for word in ["anxious","worried","overthinking","stress"]):
        patterns.append("Signs of anxiety or overthinking")

    if any(word in words for word in ["alone","isolated","nobody","no one"]):
        patterns.append("Indicators of social isolation")

    if any(word in words for word in ["angry","hate","frustrated"]):
        patterns.append("Emotional frustration detected")

    #OUTPUT --------
    result = "\n🧠 Psychological Analysis\n"
    result += f"\n💬 Sentiment: {sentiment['label']} ({round(sentiment['score']*100,2)}%)\n"

    result += "\n📌 Key Themes:\n"
    for word, count in keywords:
        result += f"- {word} ({count})\n"

    result += "\n🔍 Behavioral Insights:\n"
    if patterns:
        for p in patterns:
            result += f"- {p}\n"
    else:
        result += "- No strong psychological patterns detected!, need more info to give analysis.\n"

    return result


'''RESEARCH:

Uses the Hugging Face Transformers pipeline to analyze sentiment of input text
Downloads and prepares sentence tokenization from NLTK
Limits input to first 512 characters for sentiment analysis (model constraint)

***
Cleans the text using regex (removes punctuation, converts to lowercase)
Removes basic stopwords like “the”, “is”, “and”
Counts word frequency using Counter to extract top keywords

Detects simple psychological patterns based on keyword matching:
these are the main categories that the model checks out for
sadness
anxiety
isolation
anger

Generates a structured output with:
sentiment score
key themes (top words)
behavioral insights



 Pros (of the code)
Simple and readable structure (easy to debug and expand)
Combines NLP + psychology concept (good interdisciplinary idea)
Uses pretrained model → no need to train from scratch
Fast execution (lightweight logic after sentiment step)
Clear output formatting (user-friendly)
Good starting point for a real NLP app feature'''




