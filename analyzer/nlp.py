import es_dep_news_trf
from spacy.matcher import Matcher

nlp = es_dep_news_trf.load()

def build_lemma_matcher(replacements):
    matcher = Matcher(nlp.vocab)
    for key in replacements.keys():
        lemma_pattern = [{"LEMMA": lemma} for lemma in key.split()]
        matcher.add(key, [lemma_pattern])
    return matcher

def replace_lemmas_with_matcher(text, replacements):
    doc = nlp(text)
    matcher = build_lemma_matcher(replacements)

    matches = matcher(doc)
    matches = sorted(matches, key=lambda x: x[1])
    replaced = []
    last_end = 0

    for _, start, end in matches:
        replaced.extend([t.text for t in doc[last_end:start]])
        span_key = doc[start:end].text.lower()
        span_lemmas = " ".join([t.lemma_ for t in doc[start:end]])
        replacement = replacements.get(span_lemmas, span_key)
        replaced.append(replacement)
        last_end = end

    replaced.extend([t.text for t in doc[last_end:]])

    return " ".join(replaced)

def lemmatize_episodes(text: str, project=None):
    episodes = text.strip().splitlines()
    analyzed = []

    replacements = {}
    if project:
        for term in project.dictionary_terms.all():
            replacements[term.meaning.lower()] = term.meaning.lower()
            for synonym in term.synonyms.split(','):
                synonym = synonym.strip().lower()
                if synonym:
                    replacements[synonym] = term.meaning.lower()

    for episode in episodes:
        doc = nlp(episode)
        lemmatized_tokens = [token.lemma_ for token in doc if not token.is_punct]
        lemmatized_text = " ".join(lemmatized_tokens)

        replaced_text = replace_lemmas_with_matcher(lemmatized_text, replacements)
        analyzed.append(replaced_text)

    return analyzed
