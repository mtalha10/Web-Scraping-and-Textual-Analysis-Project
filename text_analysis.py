import os
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from textblob import TextBlob
from syllapy import count

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')


# Functions for text metrics
def avg_sentence_length(text):
    sentences = sent_tokenize(text)
    total_words = sum(len(word_tokenize(sentence)) for sentence in sentences)
    return total_words / len(sentences) if sentences else 0

def percentage_complex_words(text):
    words = word_tokenize(text)
    tagged_words = nltk.pos_tag(words)
    complex_words = [word for word, tag in tagged_words if tag.startswith("JJ") or tag.startswith("RB")]
    return (len(complex_words) / len(words)) * 100 if words else 0

def fog_index(avg_sent_len, pct_complex_words):
    return 0.4 * (avg_sent_len + pct_complex_words)

def personal_pronouns(text):
    pronouns = ["i", "me", "my", "mine", "myself", "we", "us", "our", "ours", "ourselves", "you", "your", "yours",
                "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
                "itself", "they", "them", "their", "theirs", "themselves"]
    words = word_tokenize(text.lower())
    return sum(1 for word in words if word in pronouns)

def avg_word_length(text):
    words = word_tokenize(text)
    total_chars = sum(len(word) for word in words)
    return total_chars / len(words) if words else 0

# Function to analyze text files
def analyze_text_files(input_dir, output_file):
    output_data = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as file:
                text = file.read()

            # Calculate text metrics
            blob = TextBlob(text)
            positive_score = sum(1 for sentence in blob.sentences if sentence.sentiment.polarity > 0)
            negative_score = sum(1 for sentence in blob.sentences if sentence.sentiment.polarity < 0)
            polarity_score = blob.sentiment.polarity
            subjectivity_score = blob.sentiment.subjectivity
            avg_sent_len = avg_sentence_length(text)
            pct_complex_words = percentage_complex_words(text)
            fog_idx = fog_index(avg_sent_len, pct_complex_words)
            avg_words_per_sent = len(word_tokenize(text)) / len(sent_tokenize(text)) if sent_tokenize(text) else 0
            word_count = len(word_tokenize(text))
            syllables_per_word = sum(count(word) for word in word_tokenize(text)) / word_count if word_count else 0
            pronouns_count = personal_pronouns(text)
            avg_word_len = avg_word_length(text)

            output_data.append({
                "URL_ID": filename.split(".")[0],
                "POSITIVE SCORE": positive_score,
                "NEGATIVE SCORE": negative_score,
                "POLARITY SCORE": polarity_score,
                "SUBJECTIVITY SCORE": subjectivity_score,
                "AVG SENTENCE LENGTH": avg_sent_len,
                "PERCENTAGE OF COMPLEX WORDS": pct_complex_words,
                "FOG INDEX": fog_idx,
                "AVG NUMBER OF WORDS PER SENTENCE": avg_words_per_sent,
                "WORD COUNT": word_count,
                "SYLLABLES PER WORD": syllables_per_word,
                "PERSONAL PRONOUNS": pronouns_count,
                "AVG WORD LENGTH": avg_word_len
            })

    # Save to Excel
    output_df = pd.DataFrame(output_data)
    output_df.to_excel(output_file, index=False)
    print(f"Analysis completed. Results saved to {output_file}.")
