# link
[link](https://practice-tada.streamlit.app/High_and_low)

# 🎴 High or Low カードゲーム

[▶ デモを開く](https://practice-tada.streamlit.app/High_and_low)

このサイトは、Streamlit で作成した **High or Low（ハイ＆ロー）** カードゲームのドキュメントです。  
ロジック部分と UI 部分を分離し、再利用性とテスト容易性を高めています。

---

## 🎮 ゲーム概要

プレイヤーはカードを1枚選び、相手が引くカードが「自分のカードより高い (High)」か「低い (Low)」かを予想します。  
当たればベット額分のチップを獲得し、外れれば減少します。

- 使用カード：1〜13  
- 初期チップ：100枚  
- 最大3ラウンド制  

---

## 💾 ゲーム履歴データ (JSON構造例)

このプロジェクトでは、各ラウンド結果を JSON 形式で保存できます。  
以下は実際の 3 ラウンド分のプレイ履歴例です。

```json
{
  "initial_chips": 100,
  "rounds": [
    {
      "round": 1,
      "base_card": 5,
      "player_choice": "High",
      "result_card": 9,
      "bet": 10,
      "outcome": "win",
      "chips_after": 110
    },
    {
      "round": 2,
      "base_card": 12,
      "player_choice": "Low",
      "result_card": 13,
      "bet": 20,
      "outcome": "lose",
      "chips_after": 90
    },
    {
      "round": 3,
      "base_card": 2,
      "player_choice": "Low",
      "result_card": 1,
      "bet": 30,
      "outcome": "win",
      "chips_after": 120
    }
  ],
  "game_end": "3 rounds finished"
}
