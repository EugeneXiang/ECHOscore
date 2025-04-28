# config.py

# 新的 12 维度顺序（5 主观 + 5 OVAL + 5 DeepEval，总共 5+5+5）
DIMS = [
    # Prompt 主观（前 5）
    "Clarity",
    "Scope Definition",
    "Intent Alignment",
    "Bias / Induction",
    "Efficiency",

    # OVAL 自动（接下来的 5）
    "Structural Clarity",
    "Reasoning Quality",
    "Factuality",
    "Depth of Analysis",
    "Topic Coverage",

    # DeepEval 自动（最后 5）
    "Fluency",
    "Prompt Relevance",
    "Conciseness",
    "Readability",
    "Engagement",
]

CSS = """
#submit-btn {
  background-color: orange !important;
  color: white !important;
  border: none !important;
}
#submit-btn:hover {
  background-color: darkorange !important;
}
"""