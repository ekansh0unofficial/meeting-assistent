import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter, defaultdict

nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def summarize_text(text: str, sentence_count: int = 3) -> str:
    sentences = sent_tokenize(text)

    if len(sentences) <= sentence_count:
        return "\n".join(sentences)

    word_freq = Counter()
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word.isalpha() and word not in stop_words:
                word_freq[word] += 1

    sentence_scores = defaultdict(int)
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                sentence_scores[i] += word_freq[word]

    top = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:sentence_count]
    top.sort()
    return "\n".join([sentences[i] for i in top])
