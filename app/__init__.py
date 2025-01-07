from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['CSV_FILE_PATH'] = "amazonProductScraperRes.csv"

  #   Register blueprints
    from .routes.main import main_bp
    from .routes.csv_routes import csv_bp
    from .routes.chart_routes import chart_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(csv_bp)
    app.register_blueprint(chart_bp)

    return app
