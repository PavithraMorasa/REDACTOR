import glob
import spacy
import re
import sys
import pyap
import os
nlp = spacy.load('en_core_web_sm')

def redact_names(text):
    email_regex = r'\b(?<![\w.-])\w+@\w+\.\w+(?![\w.-])\b'
    emails = re.findall(email_regex, text)

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            if ent.text not in emails: # exclude names that are part of email addresses
                text = text.replace(ent.text, '█' * len(ent.text))
    for email in emails:
        text = text.replace(email, email)
    stats("names", str(len(emails)))
    return text

def redact_genders(text):
    # Identify gender-related terms using regex with word boundary anchors
    gender_regex = r'\b(he|him|his|she|her|hers|father|mother|brother|sister|son|daughter|uncle|aunt|nephew|niece|male|female|actor|actress|boy|girl|man|woman|Mr.|Ms.)\b'
    genders = re.findall(gender_regex, text, flags=re.IGNORECASE)

    # Redact gender-related terms
    for gender in genders:
        text = re.sub(r'\b{}\b'.format(gender), '█'* len(gender), text, flags=re.IGNORECASE)
    stats("gender", str(len(genders)))
    return text
def redact_dates(text):
    # Match various date formats using regular expressions
    date_regexes = [
        r'\d{1,2}/\d{1,2}/\d{2,4}',  # MM/DD/YYYY or M/D/YYYY
        r'\d{1,2}-\d{1,2}-\d{2,4}',  # MM-DD-YYYY or M-D-YYYY
        r'\d{1,2}\.\d{1,2}\.\d{2,4}',  # MM.DD.YYYY or M.D.YYYY
        r'\d{2,4}/\d{1,2}/\d{1,2}',  # YYYY/MM/DD or YYYY/M/D
        r'\d{2,4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD or YYYY-M-D
        r'\d{2,4}\.\d{1,2}\.\d{1,2}',  # YYYY.MM.DD or YYYY.M.D
        r'\d{1,2} [A-Za-z]{3} \d{2,4}',  # DD MMM YYYY or D MMM YYYY
        r'[A-Za-z]{3,9} \d{1,2},? \d{2,4}',  # MMMM DD, YYYY or MMMM D, YYYY
        r'[A-Za-z]{3,9} \d{2,4}',  # MMMM YYYY
        r'[A-Za-z]{3,9} \d{1,2}(st|nd|rd|th), \d{2,4}',  # MMMM DDth, YYYY
    ]
    for regex in date_regexes:
        text = re.sub(regex, '█'* len(regex), text)
    stats("dates", str(len(date_regexes)))
    return text

def redact_phone_numbers(text):
    # Match various phone number formats using regular expressions
    phone_regexes = [
        r'\d{3}-\d{3}-\d{4}', # XXX-XXX-XXXX
        r'\(\d{3}\) \d{3}-\d{4}', # (XXX) XXX-XXXX
        r'\d{3} \d{3} \d{4}', # XXX XXX XXXX
        r'\+\d{1,2} \d{10}', # +XX XXXXXXXXXX
        r'\b\d{10}\b', # XXXXXXXXXX (whole word match)
        r'^\d{3}[-.\s]?\d{3}[-.\s]?\d{4}$',
        r'\d{3}/\d{3}-\d{4}',
        r'\d{3}/\d{3}-\d{4}', # XXX/XXX-XXXX
    ]
    
    # Find all message IDs
    message_id_regex = r'Message-ID: <.*?>'
    message_ids = re.findall(message_id_regex, text)
    
    # Replace each matched phone number with █ unless it is part of a message ID
    for regex in phone_regexes:
        text = re.sub(regex, lambda match: match.group() if any(message_id in match.group() for message_id in message_ids) else '█'* len(regex), text)
    stats("phone", str(len(phone_regexes)))
    return text


def redact_address(text):
    # Use regex to find the address in the text
    address_pattern = r'\b\d{1,5}\s+([a-zA-Z]+(\.| ))*[a-zA-Z]+\b,\s*([A-Z]{2}|\b(?:Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming)\s*){1},?\s+\d{5}(?:-\d{4})?\b'
    matches = re.findall(address_pattern, text)
    
    # Loop through the matches and redact the address and city name using spaCy NER
    for match in matches:
        doc = nlp(match[0])
        for ent in doc.ents:
            if ent.label_ in ['GPE', 'LOC']:
                match[0] = match[0].replace(ent.text, '█'* len(ent.text))
        text = text.replace(match[0], '█')
    
    # Use regex to find the zip code in the text and redact it
    text = re.sub(r'\b\d{5}(?:-\d{4})?\b', lambda match: '█' * len(match.group(0)), text)
    stats("address", str(len(matches)))
    return text

def redact_files_in_directory(directory_path):
    for file in glob.glob(f"{directory_path}/{'*'}"):
        print(file)
        with open(file, 'r') as f:
            file_content = f.read()
            redacted_content = redact_dates(redact_genders(redact_names(redact_phone_numbers(redact_address(file_content)))))
            print(redacted_content)
            new_file_name = os.path.splitext(file)[0] + '.redacted'
            with open(new_file_name, 'w', encoding='utf-8') as fw:
                fw.write(redacted_content)
                fw.close()
def stats(name,writtendata):
    statsfile = open(stats_path,"a")
    statsfile.write("\n"+ writtendata +" " + name + "'s are " + "Redacted" )
    statsfile.close()

a = []
a = sys.argv
in_path = a.index('--input')+1
out_path = a.index('--output')+1
stat_path = a.index('--stats')+1
files= glob.glob(a[in_path])


stats_path=a[stat_path]

if os.path.exists(stats_path):
    os.remove(stats_path)

for f in files:

    text=open(f,'r', encoding='utf').read()
    if len(text) == 0:
        print("File can't read") 
    elif len(text) != 0:
        print("File Readacted Successfully")
        statsfile = open(stats_path,"a")
        statsfile.write("\n"+str(f))
        statsfile.close()
        if '--names' in a:
            text = redact_names(text)
        if '--dates' in a:
            text = redact_dates(text)
        if '--phones' in a:
            text= redact_phone_numbers(text)
        if '--address' in a:
            text =redact_address(text)
        if '--genders' in a:
            text =redact_genders(text)
        statsfile = open(stats_path,"r")
        filecont=statsfile.read()
        # path=os.path.splitext(str(f))[0]

        # redaction file code    
        redacted_path= a[out_path]+str(f)+".redacted"
        if os.path.exists(redacted_path):
            os.remove(redacted_path)
        redacted=open(redacted_path,"w")
        redacted.write(text)
        redacted.close()
