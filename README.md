
# Market Fit Analyzer & Retail AI Predictor Pro

This project is a full-stack solution for market fit analysis, sales prediction, and business intelligence. It consists of:

- **Backend:** Python (Streamlit app) for data analytics, visualization, and machine learning.
- **Frontend:** Flutter app for mobile, web, and desktop platforms.

---

## Features

- Analyze product and shop performance using real sales data
- Predict future sales using machine learning (Random Forest)
- Interactive dashboards and visualizations (Streamlit, Plotly, Seaborn, Folium)
- Cross-platform mobile/web app for business users (Flutter)

---

## Backend (Python/Streamlit)

**Location:** `market-fit-analyzer/backend/`

### Setup
1. Install Python 3.8+
2. Install dependencies:
	```
	pip install -r requirements.txt
	```
3. Run the Streamlit app:
	```
	streamlit run app.py
	```

### Data Files
- Place your sales, products, shops, and transactions CSVs in the backend folder.

---

## Frontend (Flutter App)

**Location:** `mobileapp/`

### Setup
1. Install [Flutter](https://flutter.dev/docs/get-started/install)
2. Get dependencies:
	```
	flutter pub get
	```
3. Run the app (choose your platform):
	- Web: `flutter run -d chrome`
	- Android: `flutter run -d android`
	- Windows: `flutter run -d windows`

---

## Project Structure

- `market-fit-analyzer/backend/` - Python backend, data, and notebooks
- `mobileapp/` - Flutter frontend app

---

## License

MIT License. See `LICENSE` file for details.
