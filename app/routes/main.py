from flask import Blueprint, render_template, request
from ..services.scraper import landing_search
from ..services import product_manager
import asyncio

# Blueprint for main functions
main_bp = Blueprint("main", __name__)

# Route to instantiate the base search page
@main_bp.route("/")
def home():
    return render_template("index.html")

# Route that gets the query and clears instace of product manager so future downloads/appends aren't troubled, ensures a query is used before calling landing search and returning it as results html
@main_bp.route("/search")
def search():
    query = request.args.get("query")
    product_manager.clear_products() #Why do I have this? Check

    if not query:
        return {"error": "Query parameter is required"}, 400
    try:
        amazon_data = asyncio.run(landing_search(query, product_manager))
        return render_template("results.html", products=amazon_data)
    except Exception as e:
        return {"error": f"Error while searching: {str(e)}"}, 500
    
# Route to get attribute from request and order, setting it to asc if not specified otherwise, then confirms validity before calling sort products and returning it as the results html
@main_bp.route("/sort_products", methods=["GET"])
def sort_products():
    attribute = request.args.get("attribute")
    order = request.args.get("order", "asc") 

    valid_attributes = ["price", "rating", "rating_count"]
    if attribute not in valid_attributes:
        return "Invalid attribute", 400

    if order not in ["asc", "desc"]:
        return "Invalid order", 400
    sorted_products = product_manager.sort_products(attribute, order)

    return render_template("results.html", products=sorted_products)

