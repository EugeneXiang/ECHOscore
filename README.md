
# 🧠 ECHOscore: Evaluator Cockpit for Human Oversight

**ECHOscore** is an interactive evaluation cockpit for aligning human-centric judgment with LLM-based scoring systems. It enables **multi-dimensional assessment** across compliance, coherence, fluency, logic, and more — through both subjective human input and automated scoring engines.

---

## ✨ Features

- 🧪 **Tri-system scoring**: Human, OVAL, and DeepEval
- 📊 **Radar chart visualization** with Plotly
- 🧠 **Stable score hashing** for consistent outputs
- 🧼 **Network slang annotation** (placeholder-ready)
- 💾 **Export evaluation results** as CSV
- 🧩 **Modular architecture** for easy customization

---

## 📦 Modules Overview

| Module | Description |
|--------|-------------|
| `app.py` | Gradio-based UI interface |
| `eval_core.py` | Main orchestrator: scoring, charting, export |
| `scoring_utils.py` | Stable scoring + explanation generators |
| `radar_chart.py` | Radar chart creation (Plotly) |
| `export_utils.py` | CSV generation |
| `config.py` | Dimensions, system lists, color map |
| `slang_parser.py` | Network slang cleaner (user notes)

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python app.py
```

You can also run `ECHOscore_Intro.ipynb` for a modular walkthrough.

---

## 📋 Scoring Dimensions

- **Compliance**
- **Ethical**
- **Naturalness**
- **Structure**
- **Rationality**
- **Logic**
- **Non-hallucination**
- **Accuracy**
- **Coherence**

---

## 💡 Philosophy

ECHOscore reflects the principle of **human-machine complementarity**. It doesn't replace human judgment but amplifies it — allowing humans and models to evaluate collaboratively with clarity, granularity, and oversight.

---

## 🛡 License

MIT or custom non-commercial license (as defined in LICENSE file).  
For development and commercial usage inquiries, please contact the author.

---

## 🤝 Acknowledgments

Built with ❤️ by a human-AI co-pilot team.

