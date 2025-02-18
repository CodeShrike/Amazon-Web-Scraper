
This project is a Flask-based web application that allows users to search for products on Amazon, retrieve product details, and visualize price trends. The application also enables downloading and viewing the data as a CSV file.

---

### Features

1. **Product Search**: Query Amazon for product details.  
2. **Data Visualization**: Display price trends over time using Plotly.  
3. **CSV Management**: Update, view, and download product data as a CSV file.  

---

### Technologies Used

- **Flask**: Web framework for building the application.  
- **BeautifulSoup**: Web scraping for extracting product details.  
- **Pandas**: Data manipulation and CSV file handling.  
- **Plotly**: Interactive data visualization.  
- **Bootstrap**: Frontend styling for HTML templates.  

---

### Installation

#### Prerequisites
- Python 3.9 or higher  
- Pip (Python package manager)  

#### Steps
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

---

### Considerations

- The **Download** feature will overwrite the current CSV file, while the **Update** feature will append new data to retain previously written records.  
- For the data visualization function to work correctly, multiple days of product data should be recorded. A dummy CSV file with two dates is provided for testing purposes.  

### TBD

- Update README for Docker instructions
- Add sanitisation to queries
- Replace global list with a database