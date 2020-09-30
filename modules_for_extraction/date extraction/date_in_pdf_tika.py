import datefinder
import spacy
from tika import parser
import time

def read_pdf():
    raw = parser.from_file('1.pdf')
    print(raw['content'])
    file1 = open("output_of_pdf_read.txt","w+")
    file1.write(raw['content'])
    file1.close()

def read_file():
    file1 = open("output_of_pdf_read.txt","r")
    text_file = file1.read()
    return text_file

def filter_spans(spans):
    # Filter a sequence of spans so they don't contain overlaps
    # For spaCy 2.1.4+: this function is available as spacy.util.filter_spans()
    get_sort_key = lambda span: (span.end - span.start, -span.start)
    sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
    result = []
    seen_tokens = set()
    for span in sorted_spans:
        # Check for end - 1 here because boundaries are inclusive
        if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
            result.append(span)
        seen_tokens.update(range(span.start, span.end))
    result = sorted(result, key=lambda span: span.start)
    return result

def extract_currency_relations(doc):
    # Merge entities and noun chunks into one token
    spans = list(doc.ents) + list(doc.noun_chunks)
    spans = filter_spans(spans)
    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(span)
    relations = []
    for money in doc:
        if money.dep_ in ("attr", "dobj"):
            subject = [w for w in money.head.lefts if w.dep_ == "nsubj"]
            if subject:
                subject = subject[0]
                relations.append((subject, money))
        elif money.dep_ == "pobj" and money.head.dep_ == "prep":
            relations.append((money.head.head, money))
    return relations



if __name__ == "__main__":
    start_time= time.time()
    read_pdf()
    text_string = read_file()

    print("\n\n  TYPE  ***", type(text_string))
    

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text_string)
    print(type(doc))

    print("\n*** CURRENCY ***\n")
    relations = extract_currency_relations(doc)
    for r1, r2 in relations:
        print("{:<10}\t{}\t{}".format(r1.text, r2.ent_type_, r2.text))

    try:

        matches = datefinder.find_dates(text_string)
        for match in matches:
            print(match)
    except TypeError:
        print("\nTypeError")
    except:
        print("\nAn exception occurred")

    print("time = ", time.time()-start_time)