import numpy as np
import spacy

import entities
from entities import relation_dict


def display_parameters(api_key, engine_id, relation, threshold, query, k):
    print("____")
    print("Parameters:")
    print("Client key	= {}".format(api_key))
    print("Engine key	= {}".format(engine_id))
    print("Relation	= {}".format(entities.relation_dict[relation]))
    print("Threshold	= {}".format(threshold))
    print("Query		= {}".format(query))
    print("# of Tuples	= {}".format(k))
    print("Loading necessary libraries; This should take a minute or so ...)")


def display_iteration(i, query):
    print("=========== Iteration: {} - Query: {} ===========".format(i, query))


def error_parsing(proposed_site):
    print("")
    print("")
    print("ERROR : Unable to parse {}".format(proposed_site))


def display_final_iteration(i):
    print("Total # of iterations = {}".format(i))


def display_result(result, relation):
    subjects = []
    objects = []
    confidences = []
    print(
        "================== ALL RELATIONS for {} ( {} ) =================".format(relation_dict[relation], len(result))
    )
    if len(result):
        for key, value in result.items():
            subjects.append(key[0])
            objects.append(key[1])
            confidences.append(value)
        idxs = np.argsort(confidences)[::-1]
        for idx in idxs:
            print("Confidence: {} 		| Subject: {} 		| Object: {}".format(confidences[idx], subjects[idx], objects[idx]))
