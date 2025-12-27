

```markdown
# Django Weather Analytics and Prediction System

## 📌 Project Overview

This project is a **Django-based Weather Analytics and Prediction System** that collects historical weather data, performs exploratory data analysis (EDA), applies multiple machine learning models, and predicts **temperature and air quality index (AQI)** based on date and time inputs.

The project also includes an **interactive Streamlit dashboard** for visualization and prediction, making it suitable for academic projects and ML demonstrations.

---

## 🎯 Objectives

- Collect and store historical weather data
- Perform exploratory data analysis (EDA)
- Train and compare multiple ML models
- Predict temperature and AQI
- Visualize trends using an interactive dashboard
- Expose weather data through Django APIs

---

## 🏗️ Tech Stack

- **Backend:** Django
- **Database:** SQLite
- **Machine Learning:**  
  - Linear Regression  
  - Decision Tree  
  - Random Forest  
  - XGBoost  
  - LSTM  
- **Visualization:** Streamlit, Matplotlib, Seaborn
- **Data Source:** Visual Crossing Weather API

---

## 📂 Project Structure

```

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
├── weather_data.csv                 # Dataset
├── random_forest_model.pkl          # Trained ML model
├── Data_analysis_weather_backend.ipynb
└── manage.py

````

---

## 🗄️ Database Schema

| Column | Description |
|------|------------|
| city | City name |
| date | Date |
| time | Hour |
| temperature | Temperature (°C) |
| air_quality_index | AQI |
| created_at | Auto timestamp |

---

## 🔄 Data Collection

- Hourly historical weather data fetched using **Visual Crossing Weather API**
- AQI calculated using **temperature-based logic**
- Data stored using Django ORM
- Automated data fetching via Django management commands

---

## 📊 Exploratory Data Analysis (EDA)

EDA was performed using:
- Pandas
- Matplotlib
- Seaborn

Analysis includes:
- Temperature trends
- AQI distribution
- Correlation heatmaps
- Hourly and daily patterns

---

## 🤖 Machine Learning Models

| Model | Observation |
|-----|------------|
| Linear Regression | Underfitting |
| Decision Tree | Overfitting |
| Random Forest | Acceptable |
| XGBoost | Best generalization |
| LSTM | Overfitting (small dataset) |

**Final Model Selected:** XGBoost

---

## 📈 Model Evaluation Metrics

- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)

Models were compared to identify overfitting and underfitting behavior.

---

## 🖥️ Streamlit Dashboard

Features:
- Date & time input
- Temperature prediction
- AQI prediction
- Weather condition classification
- Interactive graphs showing trends

Run dashboard:
```bash
streamlit run app.py
````

---

## 🔌 Django APIs

* Fetch historical weather data
* Filter data by date
* Filter data by time
* JSON responses for Postman testing

---

## 🚀 How to Run the Project

### Django Backend

```bash
python manage.py migrate
python manage.py runserver
```

### Streamlit Dashboard

```bash
streamlit run app.py
```

---

## 🧠 Key Learnings

* Weather data is non-linear and time-dependent
* Simple models underfit complex data
* Complex models may overfit small datasets
* Model selection requires balancing bias and variance

---

## 🔮 Future Enhancements

* Real-time weather updates
* Rainfall and wind prediction
* Model deployment via REST APIs
* Cloud deployment

---

## 👩‍💻 Author

**Sneha Dammani**
GitHub: [https://github.com/snehadammani](https://github.com/snehadammani)


```
