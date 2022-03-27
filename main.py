import fire
import spacy

import validation
import display
import search
import entities
from spanbert import SpanBERT


def main(api_key, engine_id, relation, threshold, query, k):
    result = []
    seen_sites = set()
    i = 0

    validation.validate_api_key(api_key)
    validation.validate_engine_id(engine_id)
    validation.validate_relation(relation)
    validation.validate_threshold(threshold)
    validation.validate_query(query)
    validation.validate_k(k)

    display.display_parameters(api_key, engine_id, relation, threshold, query, k)
    nlp = spacy.load("en_core_web_lg")
    spanbert = SpanBERT("../pretrained_spanbert")

    while len(result) <= k:
        #TODO: Get best next query, stop otherwise.
        search.get_query()
        display.display_iteration(i, query)
        proposed_sites = search.query(api_key, engine_id, query)
        for proposed_site in proposed_sites:
            if proposed_site not in seen_sites:
                text_site = search.scrape(proposed_site)
                if text_site is None:
                    # TODO: Alerting here
                    continue
                trim_site = search.trim(text_site)
                entities_site = entities.process(trim_site, nlp)
                # TODO: Must remove duplicates too
                entities.add_entities(entities_site, result)
                seen_sites.add(proposed_site)
        display.display_result(result)
    display.display_final_iteration(i)


if __name__ == "__main__":
    fire.Fire(main)
