import fire
import spacy

import display
import entities
import search
import validation
from spanbert import SpanBERT


def main(api_key, engine_id, relation, threshold, query, k):
    result = dict()
    seen_sites = set()
    previous_queries = set()
    i = 1

    validation.validate_api_key(api_key)
    validation.validate_engine_id(engine_id)
    validation.validate_relation(relation)
    validation.validate_threshold(threshold)
    validation.validate_query(query)
    validation.validate_k(k)

    display.display_parameters(api_key, engine_id, relation, threshold, query, k)
    nlp = spacy.load("en_core_web_lg")
    spanbert = SpanBERT("pretrained_spanbert")

    while len(result) < k:
        current_query = search.get_query(query, result, previous_queries)
        if current_query is None:
            display.error_query()
            return result
        display.display_iteration(i, current_query)
        proposed_sites = search.query(api_key, engine_id, current_query)
        for idx_site, proposed_site in enumerate(proposed_sites):
            if proposed_site not in seen_sites:
                text_site = search.scrape(idx_site, proposed_site)
                if text_site is None:
                    display.error_parsing(proposed_site)
                    continue
                trim_site = search.trim(text_site)
                proposed_entities = entities.process(trim_site, nlp, spanbert, relation, threshold)
                entities.add_entities(proposed_entities, result)
                seen_sites.add(proposed_site)
                previous_queries.add(current_query)
        display.display_result(result, relation)
        if len(result) == 0:
            return None
    display.display_final_iteration(i)

    return result


if __name__ == "__main__":
    fire.Fire(main)
