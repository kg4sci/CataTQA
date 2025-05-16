import spacy
from typing import Dict, List

nlp = spacy.load("en_core_web_sm")

def extract_conditions(question: str) -> Dict[str, List[str]]:
    doc = nlp(question)

    conditions = {
        'temporal': [],
        'numeric': [],
        'conditional': [],
    }
    for ent in doc.ents:
        conditions['entities'].append({
            'text': ent.text,
            'label': ent.label_,
            'start': ent.start_char,
            'end': ent.end_char
        })

        if ent.label_ in ["DATE", "TIME"]:
            conditions['temporal'].append(ent.text)

        if ent.label_ in ["CARDINAL", "MONEY", "PERCENT", "QUANTITY"]:
            conditions['numeric'].append(ent.text)

    for token in doc:
        if token.text.lower() in ["if", "when", "provided", "assuming"]:
            start = token.i
            subtree = list(token.subtree)
            end = subtree[-1].i + 1 if subtree else len(doc)
            condition_clause = doc[start:end].text
            conditions['conditional'].append(condition_clause)

    condition_keywords = ["must", "require", "need", "should", "only"]
    for token in doc:
        if token.text.lower() in condition_keywords:
            conditions['other'].append(token.text)

    return conditions
