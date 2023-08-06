from NLP.Tokenizer.Tokenizer import Tokenize


def test_tokenizer():
    tokenizer = Tokenize()
    assert ["این", "یک", "تست", "است"] == tokenizer.space_tokenize("این یک تست است")


def test_stanfordTokenize():
    tokenizer = Tokenize(stanford_tokenize=True)
    assert ['این', 'یک', 'تست', 'است'] == tokenizer.stanford_tokenize("این یک تست است")


def test_ngramTokenize():
    tokenizer = Tokenize()
    assert ['این یک', 'یک تست', 'تست است'] == tokenizer.ngramTokenize("این یک تست است", 2)


def test_wordseg():
    tokenizer = Tokenize(word_breaker=True)
    assert ["این", "یک", "تست", "است"] == tokenizer.word_segmentation("اینیکتستاست")


def test_wordcomponent():
    tokenizer = Tokenize(component_words=True)
    assert ["دانش‌آموز"] == tokenizer.component_words("دانش آموز")
