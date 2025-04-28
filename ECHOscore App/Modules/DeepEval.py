# DeepEval.py
from score import stable_score
from config import DIMS

def deepeval_scores(prompt: str, output: str) -> list[float | None]:
    """
    Compute DeepEval automated scores for:
      - Fluency
      - Prompt Relevance (uses prompt+output)
      - Conciseness
      - Readability
      - Engagement
    Returns a 15-length list with:
      [None]*10 + [fluency, relevance, conciseness, readability, engagement]
    """
    # 输出流畅度
    fluency     = stable_score("DeepEval", output, DIMS[10])
    # 与 Prompt 相关性：拼接 prompt||output
    relevance   = stable_score("DeepEval", prompt + "||" + output, DIMS[11])
    # 输出简洁度
    conciseness = stable_score("DeepEval", output, DIMS[12])
    # 可读性
    readability  = stable_score("DeepEval", output, DIMS[13])
    # 吸引度／参与度
    engagement  = stable_score("DeepEval", output, DIMS[14])

    # 前 10 维度留空，后 5 维度返回自动分
    return [None]*10 + [
        fluency,
        relevance,
        conciseness,
        readability,
        engagement
    ]