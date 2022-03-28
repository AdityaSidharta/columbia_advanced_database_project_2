import entities


def validate_api_key(api_key):
    assert isinstance(api_key, str)


def validate_engine_id(engine_id):
    assert isinstance(engine_id, str)


def validate_relation(relation):
    assert relation in entities.relation_dict


def validate_threshold(threshold):
    assert isinstance(threshold, float)
    assert 0.0 < threshold < 1.0


def validate_query(query):
    assert isinstance(query, str)


def validate_k(k):
    assert isinstance(k, int)
    assert k > 0
