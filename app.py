import streamlit as st
import pandas as pd
import altair as alt

st.title("Hello, Streamlit!")
st.write("これは最小構成の Streamlitアプリです。")

# 数値入力
number_1 = st.number_input(
    "1つ目の数字を入力してください。",
    min_value=0,
    max_value=100,
    value=0,
    step=1
)

number_2 = st.number_input(
    "2つ目の数字を入力してください。",
    min_value=0,
    max_value=100,
    value=0,
    step=1
)

# 合計
number = number_1 + number_2
st.write(f"入力された数値は {number} です。")

# データ準備
data = pd.DataFrame({
    "項目": ["1つ目", "2つ目", "合計"],
    "値": [number_1, number_2, number]
})

# グラフの種類を選択
chart_type = st.radio("グラフの種類を選んでください", ["棒グラフ", "折れ線", "円グラフ"])

if chart_type == "棒グラフ":
    chart = alt.Chart(data).mark_bar(color="skyblue").encode(
        x="項目",
        y="値"
    )
elif chart_type == "折れ線":
    chart = alt.Chart(data).mark_line(point=True).encode(
        x="項目",
        y="値"
    )
else:
    chart = alt.Chart(data).mark_arc().encode(
        theta="値",
        color="項目"
    )

# グラフ表示
st.altair_chart(chart, use_container_width=True)

