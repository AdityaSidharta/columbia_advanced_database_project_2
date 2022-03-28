relation_dict = {
    1: "per:schools_attended",
    2: "per:employee_of",
    3: "per:cities_of_residence",
    4: "org:top_members/employees",
}

relation_entity_dict = {
    1: (["PERSON"], ["ORGANIZATION"]),
    2: (["PERSON"], ["ORGANIZATION"]),
    3: (["PERSON"], ["LOCATION", "CITY", "COUNTRY", "STATE_OR_PROVINCE"]),
    4: (["ORGANIZATION", ["PERSON"]]),
}

spacy2bert = {
    "ORG": "ORGANIZATION",
    "PERSON": "PERSON",
    "GPE": "LOCATION",
    "LOC": "LOCATION",
}

bert2spacy = {
    "ORGANIZATION": "ORG",
    "PERSON": "PERSON",
    "LOCATION": "LOC",
    "CITY": "GPE",
    "COUNTRY": "GPE",
    "STATE_OR_PROVINCE": "GPE",
}

entities_of_interest = ["ORGANIZATION", "PERSON", "LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]


def get_entities(sentence):
    return [(e.text, spacy2bert[e.label_]) for e in sentence.ents if e.label_ in spacy2bert]


def create_entity_pairs(sents_doc, entities_of_interest, window_size=40):
    """
    Input: a spaCy Sentence object and a list of entities of interest
    Output: list of extracted entity pairs: (text, entity1, entity2)
    """
    entities_of_interest = {bert2spacy[b] for b in entities_of_interest}
    ents = sents_doc.ents  # get entities for given sentence

    length_doc = len(sents_doc)
    entity_pairs = []
    for i in range(len(ents)):
        e1 = ents[i]
        if e1.label_ not in entities_of_interest:
            continue

        for j in range(1, len(ents) - i):
            e2 = ents[i + j]
            if e2.label_ not in entities_of_interest:
                continue
            if e1.text.lower() == e2.text.lower():  # make sure e1 != e2
                continue

            if 1 <= (e2.start - e1.end) <= window_size:

                punc_token = False
                start = e1.start - 1 - sents_doc.start
                if start > 0:
                    while not punc_token:
                        punc_token = sents_doc[start].is_punct
                        start -= 1
                        if start < 0:
                            break
                    left_r = start + 2 if start > 0 else 0
                else:
                    left_r = 0

                # Find end of sentence
                punc_token = False
                start = e2.end - sents_doc.start
                if start < length_doc:
                    while not punc_token:
                        punc_token = sents_doc[start].is_punct
                        start += 1
                        if start == length_doc:
                            break
                    right_r = start if start < length_doc else length_doc
                else:
                    right_r = length_doc

                if (right_r - left_r) > window_size:  # sentence should not be longer than window_size
                    continue

                x = [token.text for token in sents_doc[left_r:right_r]]
                gap = sents_doc.start + left_r
                e1_info = (e1.text, spacy2bert[e1.label_], (e1.start - gap, e1.end - gap - 1))
                e2_info = (e2.text, spacy2bert[e2.label_], (e2.start - gap, e2.end - gap - 1))
                if e1.start == e1.end:
                    assert x[e1.start - gap] == e1.text, "{}, {}".format(e1_info, x)
                if e2.start == e2.end:
                    assert x[e2.start - gap] == e2.text, "{}, {}".format(e2_info, x)
                entity_pairs.append((x, e1_info, e2_info))
    return entity_pairs


def process(trim_site, nlp, spanbert, relation, threshold):
    useful_sentence_idx = []
    n_extracted = 0
    print("Webpage length (num characters): {}".format(len(trim_site)))
    doc_site = nlp(trim_site)
    print("Annotating the webpage using spacy...")
    proposed_entities = {}
    n_sents = len(doc_site.sents)
    print(
        "Extracted {} sentences. Processing each sentence one by one to check for presence of right pair of named entity types; if so, will run the second pipeline ...".format(
            n_sents
        )
    )
    for idx_sent, sentence in enumerate(doc_site.sents):
        if idx_sent % 5 == 0:
            print("Processed {} / {} sentences".format(idx_sent, n_sents))
        # print("\n\nProcessing entence: {}".format(sentence))
        # print("Tokenized sentence: {}".format([token.text for token in sentence]))
        # ents = get_entities(sentence)
        # print("spaCy extracted entities: {}".format(ents))

        # create entity pairs
        candidate_pairs = []
        sentence_entity_pairs = create_entity_pairs(sentence, entities_of_interest)
        for ep in sentence_entity_pairs:
            token = ep[0]
            subject = ep[1]
            object = ep[2]
            allowed_subjects = relation_entity_dict[relation][0]
            allowed_objects = relation_entity_dict[relation][1]
            if (subject in allowed_subjects) and (object in allowed_objects):
                candidate_pairs.append({"tokens": token, "subj": subject, "obj": object})

        # print("Candidate entity pairs:")
        # for p in candidate_pairs:
        #     print("Subject: {}\tObject: {}".format(p["subj"][0:2], p["obj"][0:2]))
        # print("Applying SpanBERT for each of the {} candidate pairs. This should take some time...".format(len(candidate_pairs)))

        if len(candidate_pairs) == 0:
            return proposed_entities

        relation_preds = spanbert.predict(candidate_pairs)  # get predictions: list of (relation, confidence) pairs
        for candidate_pair, relation_pred in list(zip(candidate_pairs, relation_preds)):
            tokens = candidate_pair["tokens"]
            subject = candidate_pair["subj"][0]
            object = candidate_pair["obj"][0]
            relation = relation_pred[0]
            confidence = relation_pred[1]
            if (relation == relation_dict[relation]) and (confidence >= threshold):
                proposed_entities[(subject, object)] = confidence
                print("")
                print("=== Extracted Relation ===")
                print("Input tokens: {}".format(tokens))
                print("Output Confidence: {} ; Subject: {} ; Object: {} ;".format(confidence, subject, object))
                print("Adding to set of extracted relations")
                print("==========")
                n_extracted = n_extracted + 1
                useful_sentence_idx.append(idx_sent)
        print(
            "Extracted annotations for  {}  out of total  {}  sentences".format(len(set(useful_sentence_idx)), n_sents)
        )
        return proposed_entities


def add_entities(proposed_entities, result):
    print("Relations extracted from this website: {} (Overall: {})".format(len(proposed_entities), len(result)))
    for proposed_entity, confidence in proposed_entities.items():
        if proposed_entity in result:
            prev_confidence = result[proposed_entity]
            result[proposed_entity] = max(confidence, prev_confidence)
        else:
            result[proposed_entity] = confidence
    return result
