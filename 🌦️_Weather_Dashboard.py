import streamlit as st
import requests
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta


API_KEY = "5c0812134a59c831e3002d7730393cb0"
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

def fetch_weather_data(city, units="metric"):
    try:
        params = {"q": city, "appid": API_KEY, "units": units}
        response = requests.get(WEATHER_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

def fetch_forecast_data(city, units="metric"):
    try:
        params = {"q": city, "appid": API_KEY, "units": units}
        response = requests.get(FORECAST_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching forecast data: {e}")
        return None

def format_time(dt):
    """Convert datetime to 12-hour format (e.g., '3 PM')"""
    return datetime.fromtimestamp(dt).strftime("%I %p").lstrip("0")

def process_forecast_data(forecast_data, forecast_type):
    """Process forecast data based on selected duration and interval"""
    df = pd.DataFrame([{
        'datetime': datetime.fromtimestamp(item['dt']),
        'timestamp': item['dt'],
        'temperature': item['main']['temp'],
        'humidity': item['main']['humidity'],
        'description': item['weather'][0]['description']
    } for item in forecast_data['list']])
    
    current_day_start = df['datetime'].dt.normalize().iloc[0]
    
    if forecast_type == "Current Day":
        df = df[df['datetime'].dt.date == current_day_start.date()]
    else:
        if forecast_type == "3-Day Forecast":
            end_date = current_day_start + timedelta(days=3)
        elif forecast_type == "5-Day Forecast":
            end_date = current_day_start + timedelta(days=5)
        
        df = df[df['datetime'] < end_date]
        df = df.set_index('datetime').resample('6H').first().reset_index()
    
    df['formatted_time'] = df['datetime'].apply(lambda x: x.strftime("%I %p").lstrip("0"))
    df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
    
    return df

def plot_temperature(data):
    temps = [data["main"]["temp"], data["main"]["feels_like"], 
             data["main"]["temp_min"], data["main"]["temp_max"]]
    labels = ["Current", "Feels Like", "Min", "Max"]
    
    df = pd.DataFrame({
        'Measurement': labels,
        'Temperature': temps
    })
    
    fig = px.bar(df,
                 x='Measurement',
                 y='Temperature',
                 title="Temperature Overview",
                 color='Temperature',
                 color_continuous_scale='Viridis')
    
    fig.update_traces(
        hovertemplate="Temperature: %{y:.1f}°<extra></extra>",
        hoverlabel=dict(
            bgcolor="white",
            font_size=20, 
            font_family="Arial",
            bordercolor="black",
            font_color="black"
        )
    )
    
    for i, value in enumerate(temps):
        fig.add_annotation(
            x=labels[i],
            y=value,
            text=f"{value:.1f}°",
            showarrow=False,
            yshift=10,
            font=dict(
                size=14,
                color='black'
            )
        )
    
    fig.update_layout(
        yaxis=dict(range=[0, max(temps) * 1.1]),
        hoverdistance=100
    )
    
    return fig

def plot_forecast(df, metric, forecast_type, units_code):
    metric_label = 'Temperature' if metric == 'temperature' else 'Humidity'
    unit_suffix = f"°{'C' if units_code == 'metric' else 'F'}" if metric == 'temperature' else '%'
    
    fig = px.line(df, 
                  x='formatted_time',
                  y=metric,
                  color='date' if forecast_type != "Current Day" else None,
                  title=f'{forecast_type} - {metric_label} Forecast',
                  labels={
                      'formatted_time': 'Time',
                      metric: f'{metric_label} ({unit_suffix})',
                      'date': 'Date'
                  },
                  markers=True)
    
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title=f"{metric_label} ({unit_suffix})",
        legend_title="Date",
        hovermode='x unified'
    )
    
    return fig

def main():
    st.set_page_config(page_title="Advanced Weather Dashboard", page_icon="🌦️", layout="wide")
    
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("🌦️ Advanced Weather Dashboard")
    st.write("Get detailed weather insights and forecasts for any city utilizing our real time data from OpenWeather API.")

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        city = st.text_input("Enter City Name", placeholder="e.g., Atlanta")
    
    with col2:
        forecast_type = st.selectbox(
            "Forecast Duration",
            ["Current Day", "3-Day Forecast", "5-Day Forecast"],
            help="Choose forecast duration"
        )
    
    with col3:
        forecast_metric = st.selectbox(
            "Forecast Metric",
            ["temperature", "humidity"],
            help="Choose which weather metric to forecast"
        )
    
    with col4:
        units = st.radio("Units", ["Metric (°C)", "Imperial (°F)"], 
                        help="Choose temperature units")
        units_code = "metric" if "Metric" in units else "imperial"

    if st.button("Get Weather Data"):
        if not city.strip():
            st.error("Please enter a valid city name.")
        else:
            weather_data = fetch_weather_data(city.strip(), units_code)
            forecast_data = fetch_forecast_data(city.strip(), units_code)

            if weather_data and forecast_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader(f"Current Weather in {weather_data['name']}, {weather_data['sys']['country']}")
                    
                    st.metric(
                        label="Temperature",
                        value=f"{weather_data['main']['temp']}°{'C' if units_code == 'metric' else 'F'}",
                        delta=f"{weather_data['main']['temp'] - weather_data['main']['feels_like']:.1f}°"
                    )
                    
                    st.write(f"**Description**: {weather_data['weather'][0]['description'].capitalize()}")
                    st.write(f"**Humidity**: {weather_data['main']['humidity']}%")
                    st.write(f"**Wind Speed**: {weather_data['wind']['speed']} {'m/s' if units_code == 'metric' else 'mph'}")
                    
                    icon_code = weather_data["weather"][0]["icon"]
                    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                    st.image(icon_url, caption=f"Current conditions: {weather_data['weather'][0]['description']}")

                with col2:
                    st.subheader("Temperature Distribution")
                    st.plotly_chart(plot_temperature(weather_data), use_container_width=True)

                processed_forecast = process_forecast_data(forecast_data, forecast_type)
                st.subheader(f"{forecast_type} - {forecast_metric.capitalize()} Forecast")
                st.plotly_chart(
                    plot_forecast(processed_forecast, forecast_metric, forecast_type, units_code),
                    use_container_width=True
                )

if __name__ == "__main__":
    main()