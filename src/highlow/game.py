from dataclasses import dataclass
from typing import List
import random

@dataclass
class RoundResult:
    player_card: int
    secret_card: int
    outcome: str
    chips_after: int
    used_cards: List[int]
    remaining_deck: List[int]

def judge(player_card: int, secret_card: int, choice: str) -> str:
    if choice == "High" and secret_card > player_card:
        return "win"
    elif choice == "Low" and secret_card < player_card:
        return "win"
    return "lose"

def play_round(player_card: int, choice: str, bet: int, deck: List[int], chips: int) -> RoundResult:
    secret_card = random.choice(deck)
    outcome = judge(player_card, secret_card, choice)
    chips_after = chips + bet if outcome == "win" else chips - bet
    used = [player_card, secret_card]
    remaining = [card for card in deck if card not in used]
    return RoundResult(player_card, secret_card, outcome, chips_after, used, remaining)

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
