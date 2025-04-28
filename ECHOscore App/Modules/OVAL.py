# OVAL.py
from score import stable_score
from config import DIMS

def oval_scores(text: str) -> list[float | None]:
    """
    Compute OVAL automated scores for these 5 dimensions:
      - Structural Clarity
      - Reasoning Quality
      - Factuality
      - Depth of Analysis
      - Topic Coverage
    """
    # OVAL 只打后 5 项中的前 5(即索引 5–9)
    vals = [stable_score("OVAL", text, d) for d in DIMS[5:10]]
    # 前 5 维度（Prompt 主观）留 None，后面 DeepEval 维度也留 None
    return [None]*5 + vals + [None]*5