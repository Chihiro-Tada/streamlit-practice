import json
from pathlib import Path
import streamlit as st

# ----Pathを指定して JSONファイルを読み込み ----
json_path = Path(__file__).parent.parent / "sample_data" / "highlow_round3.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

st.session_state.deck = data["deck"]