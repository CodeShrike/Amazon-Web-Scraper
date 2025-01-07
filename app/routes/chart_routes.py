from flask import Blueprint, render_template
import pandas as pd
from ..services.utils import wrap_text
import plotly.graph_objects as go
from . import CSV_FILE_PATH
import os

# Blueprint for chart drawing
chart_bp = Blueprint("chart", __name__)

# Leverage pandas and plotly to generate a figure; conforming attributes if needed and dropping those that don't exist
@chart_bp.route("/price_trend_chart", methods=["GET"])
def show_price_trend_chart():
    if not os.path.isfile(CSV_FILE_PATH):
        return "CSV file not found", 404

    df = pd.read_csv(CSV_FILE_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d")
    df["price"] = pd.to_numeric(df["price"].str.replace("£", "").str.replace(",", ""), errors="coerce")
    df = df.dropna(subset=["price"])
    pivot_df = df.pivot_table(index="date", columns="title", values="price").fillna(0)

    fig = go.Figure()
    # Wrap text if it gets too long and add traces for each title used
    for title in pivot_df.columns:
        wrapped_title = wrap_text(title, 30)
        fig.add_trace(go.Scatter(x=pivot_df.index, y=pivot_df[title], mode="lines+markers", name=wrapped_title))

    fig.update_layout(title="Price Trends", xaxis_title="Date", yaxis_title="Price (£)", template="plotly_white")
    plot_html = fig.to_html(full_html=False)

    return render_template("price_trend_chart.html", plot_html=plot_html)
