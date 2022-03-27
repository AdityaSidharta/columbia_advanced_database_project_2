import spacy


def display_parameters(api_key, engine_id, relation, threshold, query, k):
    print("____")
    print("Parameters:")
    print("Client key	= {}".format(api_key))
    print('Engine key	= {}'.format(engine_id))
    print("Relation	= {}".format(spacy.relation_dict[relation]))
    print("Threshold	= {}".format(threshold))
    print("Query		= {}".format(query))
    print("# of Tuples	= {}".format(k))
    print("Loading necessary libraries; This should take a minute or so ...)")

def display_iteration(i, query):
    print("=========== Iteration: {} - Query: {} ===========".format(i, query))
