from flask import Blueprint, render_template
import pandas as pd
import os
from ..services.utils import produce_df
from ..services import product_manager
from . import CSV_FILE_PATH

# Blueprint for CSV related tasks
csv_bp = Blueprint("csv", __name__)

# Route appends current refreshed products to existing CSV file if it exists
@csv_bp.route("/update_csv", methods=["POST"])
def update_csv():
    products = product_manager.get_all_products()
    df = produce_df(products)

    if os.path.isfile(CSV_FILE_PATH):
        df.to_csv(CSV_FILE_PATH, mode="a", header=False, index=False)
    return "CSV updated successfully", 200

# Route to download the CSV of the products rather than append it to existing CSV
@csv_bp.route("/download_csv", methods=["GET"])
def download_csv():
    products = product_manager.get_all_products()
    if not products:
        return "No products found", 200
    df = produce_df(products)
    full_path = os.path.join(os.getcwd(), CSV_FILE_PATH)
    df.to_csv(full_path, index=False)

    return "CSV downloaded successfully", 200

# Route to see if a CSV file exists currently, and if it does to turn it into a html table to be looked through on the web page
@csv_bp.route("/view_csv", methods=["GET"])
def view_csv():
    products = product_manager.get_all_products()
    df = produce_df(products)
    if not os.path.isfile(CSV_FILE_PATH):
        return "CSV file not found", 404

    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except Exception as e:
        return f"Error reading file: {e}", 500

    html_table = df.to_html(classes="table table-striped", index=False)

    return render_template("csv_view.html", table_html=html_table)

