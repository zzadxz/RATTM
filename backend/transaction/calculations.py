from rapidfuzz import process

class Calculations:
    def _get_closest_match(self, query: str, choices: dict, score_cutoff: int = 75) -> str:
        """
        Returns the best match for query in the keys of choices dict if the score 
        is above the score_cutoff
        """
        match, score, _ = process.extractOne(query, choices.keys())
        if score >= score_cutoff:
            return match
        return None
    
    def get_company_env_score(self, transaction: dict, ESG_scores: dict[str, dict]):
        """
        Returns environmental score for a transaction's company IF the company is in the ESG_scores dict.
        Otherwise, return 0.
        """
        company_name = self._get_closest_match(transaction['merchant_name'], ESG_scores)
        if company_name is not None:
            score = ESG_scores[company_name]['environment_score']
            return score
        else:
            return 0
