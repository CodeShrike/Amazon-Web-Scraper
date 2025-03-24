
This project is a Flask-based web application that allows users to search for products on Amazon, retrieve product details, and visualize price trends. The application also enables downloading and viewing the data as a CSV file.

---

### Features

1. **Product Search**: Query Amazon for product details.  
2. **Data Visualization**: Display price trends over time using Plotly.  
3. **CSV Management**: Update, view, and download product data as a CSV file.  
4. **Scraping Automation**: Scrape multiple user-defined products at a user-given interval.
5. **Containerisation**: Run the entire application, including its dependencies and services, inside Docker containers for an OS-agnostic setup.



---

### Technologies Used

- **Flask**: Web framework for building the application.  
- **BeautifulSoup**: Web scraping for extracting product details.  
- **Pandas**: Data manipulation and CSV file handling.  
- **Plotly**: Interactive data visualization.  
- **Bootstrap**: Frontend styling for HTML templates. 
- **MongoDB**: Database storage for products
- **Schedule**: Automate scraping processes extracting queries from config.json
- **AsyncIO/aiohttp**: Asynchronous HTTP requests for efficient data extraction
- **Docker**: Containerisation platform to package and deploy the application consistently across different environments.

---

### Installation

#### Prerequisites
- Python 3.9 or higher  
- Pip (Python package manager)  
- Docker and Docker Compose (if running via containerisation)

#### Steps
# Running Locally (Without Docker)
Note: Ensure MongoDB is installed and running on your machine before starting the application. If MongoDB is not running, the application will be unable to connect to the database, and you'll encounter connection errors.
1. Clone the repository.  
2. Navigate to the project directory.  
3. Install the required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:  
   ```bash
   python run.py
   ```
5. Open your web browser and navigate to `http://127.0.0.1:5000/`.  
6. Use search queries as appropriate.  

# Running via Docker
1. Clone the repository.
2. Navigate to the project directory.
3. Build and start the Docker containers using Docker Compose:
   ```bash
   docker-compose up --build
   ```
This command will build the Docker image(s) for the Flask application, set up a container for MongoDB, and start all services.
4. Open your web browser and navigate to http://127.0.0.1:5000/.
5. Use search queries as appropriate

# Automated Scraping
1. Clone the repository.
2. Navigate to the project directory.
3. Configure config.json with the relevant queries and desired search interval in minutes
4. Run the script
   ```bash
   python automated_scrape.py
   ```
5. The process will run in the background and update to amazonProductScraperRes.csv
---

### Considerations

- The **Download** feature will overwrite the current CSV file, while the **Update** feature will append new data to retain previously written records.  
- For the data visualization function to work correctly, multiple days of product data should be recorded. A dummy CSV file with two dates is provided for testing purposes.  

### TBD

- ~~Update README for Docker instructions~~
- ~~Add sanitisation to queries~~
- ~~Replace global list with a database~~
- Add separate collections for searches