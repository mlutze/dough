import yake

MAX_NGRAM_SIZE = 1

def get_keywords(text, num) -> list[str]:

    # extract extra in case we filter stuff out
    extractor = yake.KeywordExtractor(n = MAX_NGRAM_SIZE, top = num * 2)

    keywords_scores = extractor.extract_keywords(text)

    keywords = [word for word, score in keywords_scores]

    # filter out invalid words
    keywords = [word for word in keywords if is_valid(word)]

    # cut down to the requested number
    keywords = keywords[0:num]

    return keywords

def is_valid(word: str) -> bool:
    return word.isalpha()
