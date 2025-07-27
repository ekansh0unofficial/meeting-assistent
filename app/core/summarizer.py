from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
from typing import List

_stop_words = set(stopwords.words('english'))

def summarize_text(text: str, sentence_count: int = 3) -> str:
    sentences: List[str] = sent_tokenize(text)

    if len(sentences) <= sentence_count:
        return "\n".join(sentences)

    word_freq = Counter(
        word.lower()
        for sentence in sentences
        for word in word_tokenize(sentence)
        if word.isalpha() and word.lower() not in _stop_words
    )

    sentence_scores = {
        idx: sum(word_freq[word.lower()] for word in word_tokenize(sentence) if word.lower() in word_freq)
        for idx, sentence in enumerate(sentences)
    }

    top_sentence_ids = sorted(sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:sentence_count])
    return "\n".join(sentences[i] for i in top_sentence_ids)
