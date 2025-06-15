from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Value bet API működik 🚀"}

@app.get("/value-bets")
def get_value_bets():
    # Példa értékek, itt majd jöhet a valódi scraper logika
    bets = [
        {"match": "Alcaraz vs Djokovic", "pinnacle_odds": 2.10, "tippmix_odds": 2.50, "value_percent": 19.0},
        {"match": "Swiatek vs Gauff", "pinnacle_odds": 1.70, "tippmix_odds": 1.90, "value_percent": 11.8},
    ]
    return JSONResponse(content={"value_bets": bets})
