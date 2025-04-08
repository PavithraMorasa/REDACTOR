# 🔏 Redactor: A Python-Based Text Redaction Tool

A Python-based command-line utility to automatically redact sensitive information (like names, genders, dates, phone numbers, and addresses) from text files using Natural Language Processing (NLP) and regex. Useful for anonymizing documents before sharing or analysis.
Redacted content is saved in new `.redacted` files, and detailed statistics are logged.


## ⚙️ Features:

* Redacts names using SpaCy's NLP entity recognition (excluding emails)
* Redacts genders (e.g., "he", "she", "actor", etc.)
* Redacts dates in multiple formats
* Redacts phone numbers in various patterns
* Redacts addresses including ZIP codes and US states
* Supports batch processing for multiple files
* Generates a redaction stats report

## 🚀 Installation:

🔹 Requires Python 3.7+

🔹 SpaCy English model `(en_core_web_sm)` required

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/redactor-tool.git
cd redactor-tool
```
### 2. Install dependencies

```bash
pip install spacy pyap
python -m spacy download en_core_web_sm
```

## Usage:

Redact Single or Multiple Files:

```bash
python redactor.py \
  --input "data/*.txt" \
  --output "redacted/" \
  --stats "redacted/stats.txt" \
  --names --dates --phones --genders --address
```

### Flags
