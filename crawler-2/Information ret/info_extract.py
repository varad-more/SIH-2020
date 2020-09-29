import PyPDF2
import spacy 


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

file_obj = open ('2.pdf', 'rb')
pdfreader = PyPDF2.PdfFileReader(file_obj)

print(pdfreader.documentInfo)
print (pdfreader.numPages)
page_matter = pdfreader.getPage(0)

page_context = page_matter.extractText()
print (page_context)

nlp = spacy.load('en_core_web_lg')
doc = nlp(page_context)

print ("########")
for names in doc.ents:
    print (names.text,names.label_)
print ("########")

relations = extract_currency_relations(doc)
for r1, r2 in relations:
    print("{:<10}\t{}\t{}".format(r1.text, r2.ent_type_, r2.text))



