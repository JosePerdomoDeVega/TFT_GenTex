from typing import List
from bert_score import scorer
from domain.models import ConclusionResponse



def bertscore_report(report: ConclusionResponse, reference_texts: List[str]):
    scorer_bert = scorer.BERTScorer(lang="es")

    generated_texts = report

    P, R, F1 = scorer_bert.score(generated_texts, reference_texts)

    return P.mean().item(), R.mean().item(), F1.mean().item()
