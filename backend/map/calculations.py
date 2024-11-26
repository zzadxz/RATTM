from rapidfuzz import process

# include all calculations necessary for the use case. 

def _get_closest_match(query: str, choices: list, score_cutoff: int = 60) -> str:
    """
    Returns the best match for query in the keys of choices dict if the score 
    is above the score_cutoff.
    """
    match_score = process.extractOne(query, choices)
    match = match_score[0]
    score = match_score[1]
    if score >= score_cutoff:
        return match
    return None

def _company_tier(company_env_score: int) -> int:
    """
    Returns the tier of the company based on its environmental score, 
    worst tier is 4 and best tier is 1.
    """
    if company_env_score > 560:
        return 1
    elif company_env_score > 520:
        return 2
    elif company_env_score > 500:
        return 3
    else:
        return 4
