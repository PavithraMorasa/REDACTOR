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

--input : Path to input file(s)

--output : Path to output directory

--stats	: File to log redaction statistics

--names	: Redact person names

--dates : Redact all types of dates

--phones : Redact phone numbers

--genders : Redact gendered terms

--address : Redact street address and ZIP code

### Running Tests:

To run the provided unit tests:

```bash
pytest test_redact.py
```

Tests include:

* Name redaction
* Gender term masking
* Date pattern replacement
* Phone/address sanitization
* Directory-based file redaction

## Sample Redaction Example:

Input:

`John Doe (male) called 555-1234 on 01/01/2022 from 123 Main St, Houston, TX 77001.`

Output:

`████████ (████) called ███████████████ on ███████████████ from █████████████████████████`

## 📊 Redaction Stats

A stats report will be generated (e.g., stats.txt) showing what categories were redacted and how many occurrences were found.

```bash
samples/text1.txt
3 names's are Redacted
2 gender's are Redacted
4 dates's are Redacted
1 phone's are Redacted
```

## 📌 Notes:

* The tool keeps email addresses intact even if they contain names.
* Message IDs (like Message-ID: <...>) are preserved to avoid breaking email headers.
* For performance, batch operations are supported using glob patterns like *.txt.







