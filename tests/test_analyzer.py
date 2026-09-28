from caesar_breaker.analyzer import rank_candidates
from caesar_breaker.breaker import generate_candidates


def test_rank_candidates_sorts_by_score_descending():
    candidates = generate_candidates("KHOOR ZRUOG")
    ranked = rank_candidates(candidates)
    scores = [c.score for c in ranked]
    assert scores == sorted(scores, reverse=True)


def test_rank_candidates_preserves_all_26():
    candidates = generate_candidates("KHOOR ZRUOG")
    ranked = rank_candidates(candidates)
    assert len(ranked) == 26
    assert {c.key for c in ranked} == set(range(26))
