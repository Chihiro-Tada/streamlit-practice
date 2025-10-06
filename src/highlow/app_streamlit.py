import streamlit as st
from highlow.game import GameState

# -------------------------------
# 🌐 ページ設定とタイトル
# -------------------------------
st.set_page_config(page_title="High or Low Game", page_icon="🎴", layout="wide")

st.title("🎴 High or Low カードゲーム")
st.markdown("チップを賭けて、カードの大小を当てよう！")

# -------------------------------
# 🧠 セッション状態の初期化
# -------------------------------
if "game" not in st.session_state:
    st.session_state.game = GameState()

game = st.session_state.game

# -------------------------------
# 🧭 サイドバー：ステータスと操作
# -------------------------------
with st.sidebar:
    st.header("🧭 ゲームステータス")

    # チップ残高
    st.markdown("### 💰 チップ残高")
    st.metric(label="現在のチップ", value=game.chips)

    # ラウンド数
    st.markdown("### 🔁 ラウンド数")
    st.metric(label="現在のラウンド", value=game.round)

    st.divider()

    # 残りのカード
    st.markdown("### 📦 残りのカード")
    st.write(", ".join(map(str, game.deck)))

    # 使用済みカード
    st.markdown("### 🃏 使用済みカード")
    if game.used_cards:
        st.write(", ".join(map(str, game.used_cards)))
    else:
        st.write("（まだ使用されていません）")

    st.divider()

    # リセット操作
    st.markdown("### 🔄 ゲーム操作")
    st.caption("ゲームを最初からやり直したい場合はこちら")
    if st.button("🔁 ゲームをリセット"):
        st.session_state.game = GameState()
        st.rerun()

# -------------------------------
# 🏁 ゲーム終了判定
# -------------------------------
if game.round > 3 or game.chips <= 0 or len(game.deck) < 2:
    st.subheader("🎮 ゲーム終了！")
    st.success(f"最終チップ: {game.chips}")
    st.write(f"使用済みカード: {game.used_cards}")
    st.write(f"残りのカード: {game.deck}")

    # 履歴を一覧表示
    st.markdown("### 📊 勝敗履歴")
    for i, r in enumerate(game.history, 1):
        st.write(
            f"Round {i}: {r.outcome.upper()} | あなた: {r.player_card} | 相手: {r.secret_card} | 残高: {r.chips_after}"
        )

    st.stop()

# -------------------------------
# 🎯 メイン画面：ラウンドプレイ
# -------------------------------
st.subheader(f"🔁 Round {game.round}")

col1, col2 = st.columns(2)

# あなたのカード選択
with col1:
    st.markdown("### 🃏 あなたのカードを選択")
    player_card = st.selectbox("カードを選んでください", game.deck)

# High / Low 選択
with col2:
    st.markdown("### 🎯 勝負の選択")
    choice = st.radio("HighかLowを選んでください", ["High", "Low"])
    bet = st.slider("ベット額を選んでください", min_value=1, max_value=game.chips, value=10)

# 勝負ボタン
if st.button("🔥 勝負する！"):
    result = game.next_round(player_card, choice, bet)

    # 結果表示
    st.markdown("## 🧾 結果")
    st.write(f"あなたのカード: {result.player_card}")
    st.write(f"相手のカード: {result.secret_card}")

    if result.outcome == "win":
        st.success("🎉 勝ちました！")
    else:
        st.error("😢 負けました…")

    # 残高と残りカード表示
    st.metric("💰 チップ残高", result.chips_after)
    st.write(f"📦 残りのカード: {result.remaining_deck}")
