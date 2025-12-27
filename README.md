Django Weather Analytics and Prediction System
📌 Project Overview

This project is a Django-based Weather Analytics and Prediction System that collects historical weather data, performs exploratory data analysis (EDA), applies multiple machine learning models, and predicts temperature and air quality index (AQI) based on date and time inputs.

The system also includes an interactive Streamlit dashboard for visualization and prediction, making it suitable for academic projects, ML demonstrations, and real-world analytics use cases.

🎯 Objectives

Collect and store historical weather data

Perform data analysis and feature engineering

Compare multiple machine learning models

Predict temperature and AQI based on time features

Visualize trends and predictions using an interactive dashboard

Expose weather data via Django APIs

🏗️ System Architecture

Backend: Django (REST-style APIs)

Database: SQLite

ML Models:

Linear Regression

Decision Tree Regressor

Random Forest Regressor

XGBoost Regressor

LSTM (Time Series Model)

Dashboard: Streamlit

Data Source: Visual Crossing Weather API

Model Storage: Pickle (.pkl)

📂 Project Structure
weather_backend/
│
├── weather/                         # Django app
│   ├── migrations/
│   ├── management/commands/
│   ├── models.py
│   ├── views.py
│   ├── services.py
│   ├── urls.py
│   └── utils.py
│
├── weather_backend/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── app.py                           # Streamlit dashboard
├── weather_data.csv                 # Cleaned dataset
├── random_forest_model.pkl          # Trained ML model
├── Data_analysis_weather_backend.ipynb  # EDA & ML notebook
└── manage.py

🗄️ Database Schema
Column Name	Description
city	City name
date	Date of observation
time	Hour of observation
temperature	Temperature in °C
air_quality_index	AQI (logic-based)
created_at	Auto timestamp
🔄 Data Collection

Weather data is fetched using Visual Crossing Weather API

Hourly data collected for multiple past days

AQI is calculated using temperature-based academic logic

Data is stored in SQLite using Django ORM

Automated fetching via Django management commands

📊 Exploratory Data Analysis (EDA)

EDA was performed using:

Pandas

Matplotlib

Seaborn

Analysis included:

Temperature distribution

AQI distribution

Correlation analysis

Hourly and daily trends

Heatmaps for feature relationships

🤖 Machine Learning Models Used
Model	Behavior
Linear Regression	Underfitting
Decision Tree	Overfitting
Random Forest	Acceptable
XGBoost	Best Generalization
LSTM	Overfitting (small dataset)
Final Model Selection

XGBoost was selected as the best model due to its balance between accuracy and generalization.

📈 Model Evaluation Metrics

Models were evaluated using:

Mean Squared Error (MSE)

Root Mean Squared Error (RMSE)

Performance comparison helped identify overfitting and underfitting behavior.

🖥️ Streamlit Dashboard Features

Date and time selection

Temperature prediction

AQI prediction

Weather condition classification

Interactive graphs:

Temperature rise/fall

AQI distribution

Real-time user interaction

Run dashboard:

streamlit run app.py

🔌 Django APIs

Available endpoints:

Fetch historical weather data

Filter data by date

Filter data by time

JSON responses for Postman testing

🚀 How to Run the Project
1. Backend (Django)
python manage.py migrate
python manage.py runserver

2. Streamlit Dashboard
streamlit run app.py

🧠 Key Learnings

Weather data is non-linear and time-dependent

Simple models underfit complex patterns

Complex models can overfit small datasets

Model selection should balance bias and variance

Visualization improves interpretability

📌 Future Enhancements

Real-time weather streaming

Wind speed and rainfall prediction

Model deployment via REST API

Cloud deployment

Larger dataset for improved LSTM performance
