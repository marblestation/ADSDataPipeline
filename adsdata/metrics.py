
import memory_cache

def compute_metrics(bibcode, author_num):
    # hack: eventually need lots of info for bibcode, not just author_num
    cache = memory_cache.get()
    refereed = cache['refereed']
    bibcode_to_references = cache['reference']
    bibcode_to_cites = cache['citation']

    author_num = 20  # hack
    
    total_normalized_citations = 0
    normalized_reference = 0.0
    citations_json_records = []
    citations = bibcode_to_cites[bibcode]
    citation_num = len(citations)
    refereed_citations = []
    reference_num = len(bibcode_to_references[bibcode])
    citations_histogram = defaultdict(float)

    if citations:
        for citation_bibcode in citations:
            citation_refereed = citation_bibcode in refereed
            len_citation_reference = len(bibcode_to_references[citation_bibcode])
            citation_normalized_references = 1.0 / float(max(5, len_citation_reference))
            total_normalized_citations += citation_normalized_references
            normalized_reference += citation_normalized_references
            tmp_json = {"bibcode":  citation_bibcode.encode('utf-8'),
                        "ref_norm": citation_normalized_references,
                        "auth_norm": 1.0 / author_num,
                        "pubyear": int(bibcode[:4]),
                        "cityear": int(citation_bibcode[:4])}
            citations_json_records.append(tmp_json)
            if (citation_refereed):
                refereed_citations.append(citation_bibcode)
            citations_histogram[citation_bibcode[:4]] += total_normalized_citations    

    refereed_citation_num = len(refereed_citations)
    
    # annual citations
    today = datetime.today()
    resource_age = max(1.0, today.year - int(bibcode[:4]) + 1)
    an_citations = float(citation_num) / float(resource_age)
    an_refereed_citations = float(refereed_citation_num) / float(resource_age)

    # normalized info
    rn_citations = normalized_reference 
    rn_citations_hist = dict(citations_histogram)
    logger.info('bibcode: {}, len(citations): {}, citation_normalized_references {}, refereed_citation_num {}, total_normalized_citations {}, citations_histogram {}, an_citations {}, an_refereed_citations {}'.format(bibcode, 
                len(citations), citation_normalized_references, refereed_citation_num, total_normalized_citations,citations_histogram, an_citations, an_refereed_citations))
    logger.info('refereed_citation_num {}, rn_citations {}'.format(refereed_citation_num, rn_citations))

