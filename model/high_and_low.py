import streamlit as st
import random
from dataclasses import dataclass
from typing import List

# -------------------------------
# 🎯 モデル定義（ロジック部分）
# -------------------------------

@dataclass
class RoundResult:
    player_card: int
    secret_card: int
    outcome: str  # "win" or "lose"
    chips_after: int
    used_cards: List[int]
    remaining_deck: List[int]

def judge(player_card: int, secret_card: int, choice: str) -> str:
    if choice == "High" and secret_card > player_card:
        return "win"
    elif choice == "Low" and secret_card < player_card:
        return "win"
    else:
        return "lose"

def play_round(player_card: int, choice: str, bet: int, deck: List[int], chips: int) -> RoundResult:
    secret_card = random.choice(deck)  # ✅ ランダムに選ぶ
    outcome = judge(player_card, secret_card, choice)
    chips_after = chips + bet if outcome == "win" else chips - bet
    used = [player_card, secret_card]
    remaining = [card for card in deck if card not in used]

    return RoundResult(
        player_card=player_card,
        secret_card=secret_card,
        outcome=outcome,
        chips_after=chips_after,
        used_cards=used,
        remaining_deck=remaining
    )

# -------------------------------
# 🧠 ゲーム状態管理クラス
# -------------------------------

class GameState:
    def __init__(self, initial_chips=100, deck=None):
        self.chips = initial_chips
        self.deck = deck if deck else list(range(1, 14))
        self.used_cards = []
        self.round = 1
        self.history = []

    def start_game(self):
        self.chips = 100
        self.deck = list(range(1, 14))
        self.used_cards = []
        self.round = 1
        self.history = []

    def next_round(self, player_card, choice, bet):
        result = play_round(player_card, choice, bet, self.deck, self.chips)
        self.chips = result.chips_after
        self.deck = result.remaining_deck
        self.used_cards.extend(result.used_cards)
        self.round += 1
        self.history.append(result)
        return result

# -------------------------------
# 🌐 Streamlit UI部分（サイドバー改良）
# -------------------------------

st.set_page_config(page_title="High or Low Game", page_icon="🎴", layout="wide")

st.title("🎴 High or Low カードゲーム")
st.markdown("チップを賭けて、カードの大小を当てよう！")

# セッション状態の初期化
if "game" not in st.session_state:
    st.session_state.game = GameState()

game = st.session_state.game

# サイドバー：ゲーム情報と操作（改良版）
with st.sidebar:
    st.header("🧭 ゲームステータス")

    st.markdown("### 💰 チップ残高")
    st.metric(label="現在のチップ", value=game.chips)

    st.markdown("### 🔁 ラウンド数")
    st.metric(label="現在のラウンド", value=game.round)

    st.divider()

    st.markdown("### 📦 残りのカード")
    st.write(", ".join(map(str, game.deck)))

    st.markdown("### 🃏 使用済みカード")
    if game.used_cards:
        st.write(", ".join(map(str, game.used_cards)))
    else:
        st.write("（まだ使用されていません）")

    st.divider()

    st.markdown("### 🔄 ゲーム操作")
    st.caption("ゲームを最初からやり直したい場合はこちら")
    if st.button("🔁 ゲームをリセット"):
        st.session_state.game = GameState()
        st.rerun()

# ゲーム終了判定
if game.round > 3 or game.chips <= 0 or len(game.deck) < 2:
    st.subheader("🎮 ゲーム終了！")
    st.success(f"最終チップ: {game.chips}")
    st.write(f"使用済みカード: {game.used_cards}")
    st.write(f"残りのカード: {game.deck}")

    st.markdown("### 📊 勝敗履歴")
    for i, r in enumerate(game.history, 1):
        st.write(f"Round {i}: {r.outcome.upper()} | あなた: {r.player_card} | 相手: {r.secret_card} | 残高: {r.chips_after}")

    st.stop()

# メイン画面：ラウンドプレイ
st.subheader(f"🔁 Round {game.round}")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🃏 あなたのカードを選択")
    player_card = st.selectbox("カードを選んでください", game.deck)

with col2:
    st.markdown("### 🎯 勝負の選択")
    choice = st.radio("HighかLowを選んでください", ["High", "Low"])
    bet = st.slider("ベット額を選んでください", min_value=1, max_value=game.chips, value=10)

if st.button("🔥 勝負する！"):
    result = game.next_round(player_card, choice, bet)

    st.markdown("## 🧾 結果")
    st.write(f"あなたのカード: {result.player_card}")
    st.write(f"相手のカード: {result.secret_card}")

    if result.outcome == "win":
        st.success("🎉 勝ちました！")
    else:
        st.error("😢 負けました…")

    st.metric("💰 チップ残高", result.chips_after)
    st.write(f"📦 残りのカード: {result.remaining_deck}")