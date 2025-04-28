import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import hashlib, tempfile
from config import CSS, DIMS
from OVAL import oval_scores
from DeepEval import deepeval_scores

def make_explanation(system: str, dimension: str, score: float) -> str:
    templates = {
        # OVAL 拓展 5 维
        "Structural Clarity":  f"{system} scored Structural Clarity at {score}: The text structure may be unclear; consider adding headings or breaking into paragraphs.",
        "Reasoning Quality":   f"{system} scored Reasoning Quality at {score}: Argument support is weak; consider adding logical reasoning or evidence.",
        "Factuality":          f"{system} scored Factuality at {score}: Information may be inaccurate; please fact-check the facts.",
        "Depth of Analysis":   f"{system} scored Depth of Analysis at {score}: Analysis seems shallow; add more insights or examples.",
        "Topic Coverage":      f"{system} scored Topic Coverage at {score}: Key aspects may be missing; ensure you cover the full scope.",
        # DeepEval 拓展 5 维
        "Fluency":             f"{system} scored Fluency at {score}: Expression may be disfluent; consider smoothing sentence transitions.",
        "Prompt Relevance":    f"{system} scored Prompt Relevance at {score}: The response may stray from the prompt; ensure alignment.",
        "Conciseness":         f"{system} scored Conciseness at {score}: The response may be verbose; consider trimming redundant parts.",
        "Readability":         f"{system} scored Readability at {score}: The text is hard to read; consider simpler wording or shorter sentences.",
        "Engagement":          f"{system} scored Engagement at {score}: The response lacks engagement; add examples or a conversational tone.",
    }
    return templates.get(dimension, f"{system} scored {dimension} at {score}: Low score detected; please review this aspect.")

def evaluate(
    prompt_text: str,
    output_text: str,
    # Prompt 主观 5 维度
    s1: float, s2: float, s3: float, s4: float, s5: float,
    # Prompt 主观解释
    e1: str, e2: str, e3: str, e4: str, e5: str,
    # Judge 模块
    judge_llm: str,
    ja1: float, ja2: float, ja3: float, ja4: float, ja5: float,
    judge_remark: str,
    # 额外备注
    remark: str
):
    # 1) 验证 Prompt 主观低分必须解释
    for score, exp, label in [
        (s1, e1, "Clarity"),
        (s2, e2, "Scope Definition"),
        (s3, e3, "Intent Alignment"),
        (s4, e4, "Bias / Induction"),
        (s5, e5, "Efficiency"),
    ]:
        if score < 3 and not exp.strip():
            raise gr.Error(f"{label} score < 3: please provide an explanation.")

    # 2) 构造三组分数
    subj = [s1, s2, s3, s4, s5] + [None]*10
    oval = oval_scores(output_text)                   # 15-length list
    deep = deepeval_scores(prompt_text, output_text)  # 15-length list

    # 3) 自动低分解释
    auto_expls = []
    for system, scores, idxs in [
        ("OVAL",     oval, range(5,10)),
        ("DeepEval", deep, range(10,15))
    ]:
        for i in idxs:
            sc = scores[i]
            if sc is not None and sc < 3:
                auto_expls.append(make_explanation(system, DIMS[i], sc))
    auto_text = "\n".join(auto_expls) or "All automated scores ≥ 3; no issues detected."

    # 4) 构建 DataFrame 并导出 CSV（包含 Judge 信息列）
    full_df = pd.DataFrame({
        "Dimension":                   DIMS,
        "Subjective (Prompt)":         subj,
        "OVAL (Output)":               oval,
        "DeepEval (Output)":           deep,
        "Judge LLM":                   [judge_llm] * len(DIMS),
        "Sensory Accuracy":            [ja1] * len(DIMS),
        "Emotional Engagement":        [ja2] * len(DIMS),
        "Flow & Naturalness":          [ja3] * len(DIMS),
        "Imagery Completeness":        [ja4] * len(DIMS),
        "Simplicity & Accessibility":  [ja5] * len(DIMS),
        "Judge Remarks":               [judge_remark] * len(DIMS),
        "Notes (Slang/Tech Terms)":    [remark] * len(DIMS),
    })
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    full_df.to_csv(tmp.name, index=False)

    # 5) 提取子表
    subj_df = full_df.iloc[0:5][["Dimension","Subjective (Prompt)"]]
    oval_df = full_df.iloc[5:10][["Dimension","OVAL (Output)"]]
    deep_df = full_df.iloc[10:15][["Dimension","DeepEval (Output)"]]

    # 6) 构造雷达图（取三类分数最大值）
    max_scores = [
        max([v for v in vals if v is not None]) if any(v is not None for v in vals) else 0
        for vals in zip(subj, oval, deep)
    ]
    closed_dims = DIMS + [DIMS[0]]
    r = max_scores + [max_scores[0]]
    fig = go.Figure(go.Scatterpolar(r=r, theta=closed_dims, fill='toself'))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,5])),
        showlegend=False,
        title="Final (Max) Scores Radar"
    )

    return (
        subj_df,
        oval_df,
        deep_df,
        fig,
        tmp.name,
        remark,
        # prompt 低分解释
        e1, e2, e3, e4, e5,
        # 自动解释
        auto_text,
        # Judge 输出
        judge_llm,
        ja1, ja2, ja3, ja4, ja5,
        judge_remark
    )

def toggle_explain(v): 
    return gr.update(visible=(v<3))

css = """
#submit-btn {
  background-color: orange !important;
  color: white !important;
  border: none !important;
}
#submit-btn:hover {
  background-color: darkorange !important;
}
"""

with gr.Blocks(css=css) as iface:
    gr.Markdown("# ECHOscore – Prompt vs Output Evaluation")

    prompt_in = gr.Textbox(lines=2, label="Input (Prompt)")
    output_in = gr.Textbox(lines=4, label="Output (Model Response)")

    with gr.Row():
        s1 = gr.Slider(0,5,0,step=0.1, label="Prompt – Clarity")
        s2 = gr.Slider(0,5,0,step=0.1, label="Prompt – Scope Definition")
        s3 = gr.Slider(0,5,0,step=0.1, label="Prompt – Intent Alignment")
        s4 = gr.Slider(0,5,0,step=0.1, label="Prompt – Bias / Induction")
        s5 = gr.Slider(0,5,0,step=0.1, label="Prompt – Efficiency")

    e1 = gr.Textbox(lines=2, label="Explain Clarity (<3)", visible=False)
    e2 = gr.Textbox(lines=2, label="Explain Scope Definition (<3)", visible=False)
    e3 = gr.Textbox(lines=2, label="Explain Intent Alignment (<3)", visible=False)
    e4 = gr.Textbox(lines=2, label="Explain Bias / Induction (<3)", visible=False)
    e5 = gr.Textbox(lines=2, label="Explain Efficiency (<3)", visible=False)
    
    remark = gr.Textbox(lines=2, label="Internet slang & technical terms notes (optional)")
    
    # LLM-as-a-judge 模块（完全可选）
    judge_llm    = gr.Textbox(lines=1, label="LLM-as-a-Judge (optional-the name of LLM)")
    ja1          = gr.Number(label="Sensory Accuracy",            value=0, precision=1, step=0.1)
    ja2          = gr.Number(label="Emotional Engagement",        value=0, precision=1, step=0.1)
    ja3          = gr.Number(label="Flow & Naturalness",          value=0, precision=1, step=0.1)
    ja4          = gr.Number(label="Imagery Completeness",        value=0, precision=1, step=0.1)
    ja5          = gr.Number(label="Simplicity & Accessibility",  value=0, precision=1, step=0.1)
    judge_remark = gr.Textbox(lines=2, label="Judge Remarks (optional)")


    s1.change(toggle_explain, s1, e1)
    s2.change(toggle_explain, s2, e2)
    s3.change(toggle_explain, s3, e3)
    s4.change(toggle_explain, s4, e4)
    s5.change(toggle_explain, s5, e5)

    submit = gr.Button("Submit", elem_id="submit-btn")
    with gr.Row():
        subj_tbl = gr.Dataframe(label="Prompt Subjective Scores")
        oval_tbl = gr.Dataframe(label="OVAL Automated Scores")
        deep_tbl = gr.Dataframe(label="DeepEval Automated Scores")

    radar          = gr.Plot(label="Final Radar Chart")
    csv_out        = gr.File(label="Export CSV")
    notes_out      = gr.Textbox(label="Notes (Slang/Tech Terms)")
    exp1_out       = gr.Textbox(label="Clarity Explanation")
    exp2_out       = gr.Textbox(label="Scope Definition Explanation")
    exp3_out       = gr.Textbox(label="Intent Alignment Explanation")
    exp4_out       = gr.Textbox(label="Bias/Induction Explanation")
    exp5_out       = gr.Textbox(label="Efficiency Explanation")
    auto_out       = gr.Textbox(label="Automatic Explanation")
    judge_llm_out  = gr.Textbox(label="Judge LLM")
    ja1_out        = gr.Number(label="Sensory Accuracy")
    ja2_out        = gr.Number(label="Emotional Engagement")
    ja3_out        = gr.Number(label="Flow & Naturalness")
    ja4_out        = gr.Number(label="Imagery Completeness")
    ja5_out        = gr.Number(label="Simplicity & Accessibility")
    judge_remarks_out = gr.Textbox(label="Judge Remarks")

    submit.click(
        evaluate,
        [
            prompt_in, output_in,
            s1, s2, s3, s4, s5,
            e1, e2, e3, e4, e5,
            judge_llm, ja1, ja2, ja3, ja4, ja5,
            judge_remark, remark
        ],
        [
            subj_tbl, oval_tbl, deep_tbl,
            radar, csv_out, notes_out,
            exp1_out, exp2_out, exp3_out, exp4_out, exp5_out,
            auto_out,
            judge_llm_out, ja1_out, ja2_out, ja3_out, ja4_out, ja5_out,
            judge_remarks_out
        ]
    )

if __name__ == "__main__":
    iface.launch()