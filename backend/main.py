
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd

app = FastAPI(
    title="Sales Forecasting & Business Intelligence API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_csv(filename):
    path = DATA_DIR / filename

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Missing data file: {filename}"
        )

    return pd.read_csv(path)


@app.get("/")
def home():
    return {"message": "Sales Forecasting API is running!"}


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.get("/api/overview")
def overview():
    df = load_csv("overview.csv")
    return df.iloc[0].to_dict()


@app.get("/api/monthly-sales")
def monthly_sales():
    return load_csv("monthly_sales.csv").to_dict(orient="records")


@app.get("/api/top-products")
def top_products():
    return load_csv("top_products.csv").to_dict(orient="records")


@app.get("/api/top-countries")
def top_countries():
    return load_csv("top_countries.csv").to_dict(orient="records")


@app.get("/api/forecast")
def forecast():
    return load_csv("30_day_forecast.csv").to_dict(orient="records")
