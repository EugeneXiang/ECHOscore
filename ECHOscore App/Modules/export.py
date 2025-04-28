
import pandas as pd
import tempfile
from config import DIMS

def export_csv(subj: list, oval: list, deep: list) -> str:
    """Build DataFrame and save to temp CSV, return file path"""
    df = pd.DataFrame({
        "Dimension": DIMS,
        "Subjective": subj,
        "OVAL": oval,
        "DeepEval": deep
    })
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(tmp.name, index=False)
    return tmp.name
