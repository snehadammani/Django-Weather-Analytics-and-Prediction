import streamlit as st
import pandas as pd
import numpy as np
import pickle
import seaborn as sns
from datetime import datetime, timedelta
import warnings

import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# Optional loaders for model compatibility (joblib/dill); set to None if not installed
try:
    import joblib
except Exception:
    joblib = None

try:
    import dill
except Exception:
    dill = None

# Page config
st.set_page_config(page_title="Weather & AQI Dashboard", layout="wide")

# Load model and data
@st.cache_resource
def load_model():
    model_path = r'D:\Project_MT\weather_backend\random_forest_model.pkl'
    # 1) Try standard pickle load
    try:
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e_pickle:
        # 2) Try pickle with latin1 encoding (useful for py2/np pickles)
        try:
            with open(model_path, 'rb') as f:
                return pickle.load(f, encoding='latin1')
        except Exception as e_pickle_enc:
            # 3) Try joblib
            if joblib is not None:
                try:
                    return joblib.load(model_path)
                except Exception:
                    pass
            # 4) Try dill
            if dill is not None:
                try:
                    with open(model_path, 'rb') as f:
                        return dill.load(f)
                except Exception:
                    pass

            # If all attempts fail, raise a clear error
            raise RuntimeError(
                f"Failed to load model from {model_path}. pickle error: {e_pickle}; "
                f"pickle(encoding='latin1') error: {e_pickle_enc}. Try installing joblib/dill or re-saving the model."
            )

@st.cache_data
def load_data():
    path = r'D:\Project_MT\weather_backend\weather_data.csv'
    df = pd.read_csv(path)
    # Normalize column names and map to expected names used in the app
    col_map = {}
    for c in df.columns:
        lc = c.strip().lower()
        if lc == 'temperature':
            col_map[c] = 'Temperature'
        elif lc in ('air_quality_index', 'aqi'):
            col_map[c] = 'AQI'
        elif lc == 'date':
            col_map[c] = 'date'
        elif lc == 'time':
            col_map[c] = 'time'
    if col_map:
        df = df.rename(columns=col_map)
    # If both date and time are present, combine into a single datetime `date` column
    try:
        if 'date' in df.columns and 'time' in df.columns:
            df['date'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))
        elif 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
    except Exception:
        pass
    return df

model = load_model()
df = load_data()

# Helper to find the first matching column name from common variants
def _first_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

# Detect temperature/AQI column names used in this dataset
TEMP_COL = _first_col(df, ['Temperature', 'temperature', 'temp'])
AQI_COL = _first_col(df, ['AQI', 'air_quality_index', 'aqi', 'airqualityindex'])

# Precompute averages for display (safely)
try:
    avg_temp = df[TEMP_COL].mean() if TEMP_COL is not None else None
except Exception:
    avg_temp = None
try:
    avg_aqi = df[AQI_COL].mean() if AQI_COL is not None else None
except Exception:
    avg_aqi = None

# Title
st.title("🌦️ Weather & AQI Prediction Dashboard")
st.markdown("---")

# Sidebar for inputs
st.sidebar.header("📊 Prediction Settings")
pred_date = st.sidebar.date_input("Select Date", datetime.now())
pred_time = st.sidebar.time_input("Select Time", datetime.now().time())

# Combine date and time
pred_datetime = datetime.combine(pred_date, pred_time)

# Create columns for main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📅 Selected Date", pred_date.strftime("%d-%m-%Y"))
with col2:
    st.metric("⏰ Selected Time", pred_time.strftime("%H:%M"))
with col3:
    temp_display = f"{avg_temp:.1f}°C" if avg_temp is not None and not pd.isna(avg_temp) else "N/A"
    st.metric("🌡️ Avg Temperature", temp_display)
with col4:
    aqi_display = f"{avg_aqi:.1f}" if avg_aqi is not None and not pd.isna(avg_aqi) else "N/A"
    st.metric("💨 Avg AQI", aqi_display)

st.markdown("---")

# Prediction section
st.subheader("🔮 Make Prediction")

# Prepare features for prediction (adjust based on your model)
try:
    # Extract time features
    hour = pred_time.hour
    month = pred_date.month
    day = pred_date.day
    
    # Create prediction input
    prediction_input = np.array([[hour, month, day]])
    
    # Make predictions
    temp_pred = model.predict([[hour, month, day]])[0]
    aqi_pred = model.predict([[hour, month, day]])[0]
    
    # Predictions display
    pred_col1, pred_col2, pred_col3 = st.columns(3)
    
    with pred_col1:
        st.metric("🌡️ Temperature Prediction", f"{temp_pred:.1f}°C")
    with pred_col2:
        st.metric("💨 AQI Prediction", f"{aqi_pred:.1f}")
    with pred_col3:
        if aqi_pred < 50:
            status = "✅ Good"
            color = "green"
        elif aqi_pred < 100:
            status = "🟡 Moderate"
            color = "yellow"
        else:
            status = "🔴 Poor"
            color = "red"
        st.metric("Air Quality", status)
    
except Exception as e:
    st.error(f"Prediction Error: {str(e)}")

st.markdown("---")

# Weather conditions analysis
st.subheader("🌦️ Weather Conditions Analysis")

analysis_col1, analysis_col2 = st.columns(2)

with analysis_col1:
    st.write("**Weather Summary:**")
    if temp_pred > 30:
        st.info("🔥 **HOT** - High temperature expected")
    elif temp_pred < 15:
        st.info("❄️ **COLD** - Low temperature expected")
    else:
        st.success("🌤️ **MILD** - Comfortable temperature")

with analysis_col2:
    st.write("**Pollution Status:**")
    if aqi_pred > 150:
        st.error("🚨 **VERY HIGH POLLUTION** - Poor air quality")
    elif aqi_pred > 100:
        st.warning("⚠️ **HIGH POLLUTION** - Bad air quality")
    else:
        st.success("✅ **GOOD AIR QUALITY** - Pollution levels low")

st.markdown("---")

# Graphs and Comparisons
st.subheader("📈 Temperature & AQI Trends")

graph_col1, graph_col2 = st.columns(2)

# Temperature Trend
with graph_col1:
    st.write("**Temperature Trend**")
    df_sorted = df.sort_values('date') if 'date' in df.columns else df
    
    fig, ax = plt.subplots(figsize=(10, 5))
    if TEMP_COL is not None:
        ax.plot(range(len(df_sorted)), df_sorted[TEMP_COL], marker='o', color='red', linewidth=2)
        ax.axhline(y=temp_pred, color='green', linestyle='--', label='Predicted')
        ax.set_xlabel("Days")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Temperature Over Time")
        ax.legend()
        ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# AQI Trend
with graph_col2:
    st.write("**AQI Trend**")
    fig, ax = plt.subplots(figsize=(10, 5))
    if AQI_COL is not None:
        ax.plot(range(len(df_sorted)), df_sorted[AQI_COL], marker='o', color='purple', linewidth=2)
        ax.axhline(y=aqi_pred, color='green', linestyle='--', label='Predicted')
        ax.set_xlabel("Days")
        ax.set_ylabel("AQI Level")
        ax.set_title("AQI Over Time")
        ax.legend()
        ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.markdown("---")

# Comparison section
st.subheader("🔍 Historical Comparison")

compare_days = st.slider("Days to Compare", 7, 30, 15)

comparison_col1, comparison_col2 = st.columns(2)

with comparison_col1:
    st.write("**Temperature Rise/Fall**")
    fig, ax = plt.subplots(figsize=(10, 5))
    last_days = df_sorted.tail(compare_days)
    if TEMP_COL is not None:
        colors = ['orange'] * len(last_days)
        ax.bar(range(len(last_days)), last_days[TEMP_COL], color='orange', alpha=0.7)
        ax.set_xlabel("Days")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title(f"Temperature Comparison ({compare_days} days)")
        ax.grid(True, alpha=0.3, axis='y')
    st.pyplot(fig)

with comparison_col2:
    st.write("**AQI Variation**")
    fig, ax = plt.subplots(figsize=(10, 5))
    last_days = df_sorted.tail(compare_days)
    if AQI_COL is not None:
        ax.bar(range(len(last_days)), last_days[AQI_COL], color='purple', alpha=0.7)
        ax.set_xlabel("Days")
        ax.set_ylabel("AQI Level")
        ax.set_title(f"AQI Variation ({compare_days} days)")
        ax.grid(True, alpha=0.3, axis='y')
    st.pyplot(fig)

st.markdown("---")

# Footer
st.info("📌 Dashboard Updated: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S"))