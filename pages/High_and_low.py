import streamlit as st
import random

st.title("🎲 High and Low Game 🎲")

cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

# --- 初期化 ---
if "current_card" not in st.session_state:
    st.session_state.current_card = random.randint(1, 13)

st.write(f"現在のカード: {cards[st.session_state.current_card - 1]}")

# --- 次のカード ---
next_card = random.randint(1, 13)

# --- High ボタン ---
if st.button("High"):
    st.write(f"次のカード: {cards[next_card - 1]}")
    if next_card > st.session_state.current_card:
        st.success("You Win! 🎉")
    elif next_card < st.session_state.current_card:
        st.error("You Lose 💔")
    elif next_card == st.session_state.current_card:
        st.info("Draw 🤝")
    else:
        st.warning("This is a warning ⚠️")
    st.session_state.current_card = next_card

# --- Low ボタン ---
if st.button("Low"):
    st.write(f"次のカード: {cards[next_card - 1]}")
    if next_card < st.session_state.current_card:
        st.success("You Win! 🎉")
    elif next_card > st.session_state.current_card:
        st.error("You Lose 💔")
    elif next_card == st.session_state.current_card:
        st.info("Draw 🤝")
    else:
        st.warning("This is a warning ⚠️")
    st.session_state.current_card = next_card

# --- リセットボタン ---
if st.button("リセット"):
    st.session_state.current_card = random.randint(1, 13)
    st.warning("ゲームをリセットしました！ ⚠️")
