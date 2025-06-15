
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Mock data - ezt később cseréljük scraper és API adatforrásra
tippmix_data = pd.DataFrame([
    {
        "players": "Carlos Alcaraz - Novak Djokovic",
        "player1_odds": 2.10,
        "player2_odds": 1.75
    }
])

pinnacle_data = pd.DataFrame([
    {
        "players": "Carlos Alcaraz - Novak Djokovic",
        "player1_odds": 1.90,
        "player2_odds": 2.00
    }
])

class ValueBet(BaseModel):
    match: str
    player1_odds_tip: float
    player2_odds_tip: float
    player1_odds_pinnacle: float
    player2_odds_pinnacle: float
    value_player1: float
    value_player2: float

def compute_value_bets(tippmix_df, pinnacle_df):
    results = []
    for _, row in tippmix_df.iterrows():
        match = pinnacle_df[pinnacle_df["players"] == row["players"]]
        if match.empty:
            continue

        p_row = match.iloc[0]
        prob1 = 1 / p_row["player1_odds"]
        prob2 = 1 / p_row["player2_odds"]
        margin = prob1 + prob2

        fair_prob1 = prob1 / margin
        fair_prob2 = prob2 / margin

        value1 = (row["player1_odds"] * fair_prob1) - 1
        value2 = (row["player2_odds"] * fair_prob2) - 1

        results.append(ValueBet(
            match=row["players"],
            player1_odds_tip=row["player1_odds"],
            player2_odds_tip=row["player2_odds"],
            player1_odds_pinnacle=p_row["player1_odds"],
            player2_odds_pinnacle=p_row["player2_odds"],
            value_player1=round(value1 * 100, 2),
            value_player2=round(value2 * 100, 2)
        ))
    return results

@app.get("/value-bets", response_model=list[ValueBet])
def get_value_bets():
    return compute_value_bets(tippmix_data, pinnacle_data) 
