# Text Analysis Toolkit

A production-ready Python package for tokenization, word frequency analysis, sentiment scoring, and report generation — built entirely on Python's standard library with **zero external dependencies**.

<p align="center">
  <a href="https://github.com/abhinay03/text-analysis-toolkit"><strong>GitHub</strong></a> ·
  <a href="#quick-start"><strong>Quick Start</strong></a> ·
  <a href="#features"><strong>Features</strong></a> ·
  <a href="#usage"><strong>Usage</strong></a>
</p>

## Features

- **Tokenization** — word/sentence splitting, punctuation removal, stopword filtering, n-gram generation
- **Frequency Analysis** — word counts, top-N, term frequency (TF), relative frequencies, threshold filtering
- **Sentiment Scoring** — lexicon-based scoring (-1 to +1) with 100+ built-in positive/negative words, custom lexicon support
- **Report Generation** — plain text and JSON report output with formatted tables
- **CLI** — command-line interface for analyzing text files or inline text
- **Web Interface** — interactive demo with FastAPI (optional)

## Authors

- Manikanta Engalligi
- Abhinay Sambherao
- Sandeep Hidellarachchi
- Kevin Luke Prashanth

---

## Quick Start

### Installation (Core — No Dependencies)

```bash
cd text-analysis-toolkit
pip install -e .
```

### Installation (Web Interface)

```bash
pip install -r requirements.txt
uvicorn webapp.main:app --reload
# Open http://localhost:8000
```

---

## Usage

### Web Interface

Visit the interactive demo at **http://localhost:8000/demo** after starting the web server.

### Command Line

```bash
# Analyze a text file
python -m text_analysis_toolkit.cli samples/positive_review.txt

# JSON output
python -m text_analysis_toolkit.cli samples/mixed_article.txt -f json

# Remove stopwords
python -m text_analysis_toolkit.cli samples/negative_review.txt --no-stopwords

# Output to file
python -m text_analysis_toolkit.cli samples/article.txt -o report.txt

# Analyze inline text
python -m text_analysis_toolkit.cli -t "I love this amazing product!"

# Help
python -m text_analysis_toolkit.cli --help
```

### Python API

```python
from text_analysis_toolkit import Tokenizer, FrequencyAnalyzer, SentimentAnalyzer, TextAnalyzer

# --- Tokenizer ---
tk = Tokenizer(lower=True, remove_punct=True, remove_stopwords=False)
tokens = tk.tokenize("Hello, World! How are you?")
# Result: ['hello', 'world', 'how', 'are', 'you']

sentences = tk.sentence_split("Hello world. How are you?")
# Result: ['Hello world.', 'How are you?']

bigrams = tk.ngrams(tokens, 2)
# Result: ['hello world', 'world how', 'how are', 'are you']

# With stopword removal
tk_sw = Tokenizer(remove_stopwords=True)
tk_sw.tokenize("the quick brown fox jumps")
# Result: ['quick', 'brown', 'fox', 'jumps']

# Custom stopwords
tk_custom = Tokenizer(remove_stopwords=True, stopwords=["hello", "world"])
tk_custom.tokenize("Hello World foo bar")
# Result: ['foo', 'bar']

# --- FrequencyAnalyzer ---
fa = FrequencyAnalyzer(tokens)
fa.total_words     # 5
fa.unique_words    # 5
fa.top_words(3)    # [('hello', 1), ('world', 1), ('how', 1)]
fa.term_frequency("hello")  # 0.2
fa.word_counts()   # {'hello': 1, 'world': 1, 'how': 1, 'are': 1, 'you': 1}
fa.relative_frequencies()   # {'hello': 0.2, ...}
fa.words_above_threshold(0)  # all words with count > 0

# --- SentimentAnalyzer ---
sa = SentimentAnalyzer()
sa.score(["good", "great", "bad"])        # 0.33 (positive)
sa.score(["bad", "terrible", "good"])     # -0.33 (negative)

sa.detailed_score(["happy", "sad", "angry", "nice"])
# Returns dict with: positive_count, negative_count, sentiment_score, sentiment_label

sa.positive_matches(["good", "bad", "great"])   # ['good', 'great']
sa.negative_matches(["good", "bad", "great"])   # ['bad']

# Custom lexicon
sa.load_custom_lexicon("my_positive_words.txt", "positive")
sa.load_custom_lexicon("my_negative_words.txt", "negative")

# Alternative: construct with custom sets
sa2 = SentimentAnalyzer(positive_words={"foo"}, negative_words={"bar"})

# --- TextAnalyzer (all-in-one facade) ---
ta = TextAnalyzer(remove_stopwords=False)
result = ta.analyze("I love this amazing product! It is fantastic and wonderful.")
result["statistics"]
# {'total_words': 10, 'unique_words': 10, 'sentences': 2, 'avg_word_length': 4.8}

result["sentiment"]
# {'positive_count': 4, 'negative_count': 0, 'sentiment_score': 1.0, 'sentiment_label': 'positive', ...}

result["frequencies"]["top_words"]  # top 20 words with counts
result["ngrams"]["2"]               # bigrams with counts
result["ngrams"]["3"]               # trigrams with counts

# Reports
print(ta.report_text(result))       # formatted text report
print(ta.report_json(result))       # JSON report

# File analysis
result = ta.analyze_file("samples/positive_review.txt")
```

### Options Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `lower` | `True` | Convert text to lowercase |
| `remove_punct` | `True` | Strip punctuation |
| `remove_stopwords` | `False` | Filter out common English stopwords |
| `stopwords` | `None` | Custom stopword list (uses defaults if None) |
| `n` (ngrams) | `2` | N-gram size |
| `threshold` | `1` | Minimum count for `words_above_threshold` |

## Running Tests

```bash
python -m unittest discover -s text_analysis_toolkit/tests -v
```

## Project Structure

```
text-analysis-toolkit/
├── text_analysis_toolkit/
│   ├── __init__.py          # Package exports
│   ├── tokenizer.py         # Tokenizer class
│   ├── frequency.py         # FrequencyAnalyzer class
│   ├── sentiment.py         # SentimentAnalyzer class
│   ├── reporter.py          # ReportGenerator class
│   ├── analyzer.py          # TextAnalyzer facade
│   ├── cli.py               # Command-line interface
│   └── tests/               # Comprehensive test suite (46+ tests)
│       ├── test_tokenizer.py
│       ├── test_frequency.py
│       ├── test_sentiment.py
│       ├── test_reporter.py
│       └── test_analyzer.py
├── webapp/
│   ├── main.py              # FastAPI web application
│   ├── run.py               # Entry point for development server
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html       # Landing page
│   │   ├── documentation.html
│   │   ├── demo.html        # Interactive demo
│   │   └── about.html
│   └── static/
│       ├── css/style.css
│       └── js/main.js
├── samples/
│   ├── positive_review.txt
│   ├── negative_review.txt
│   └── mixed_article.txt
├── pyproject.toml
├── requirements.txt
└── README.md
```
