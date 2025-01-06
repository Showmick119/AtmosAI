import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime, timedelta
import requests
import pandas as pd
import json

st.set_page_config(
    page_title="Weather Analysis Chatbot",
    page_icon="🤖",
    layout="wide"
)

if 'weather_data_formatted' not in st.session_state:
    st.session_state.weather_data_formatted = None

if 'messages' not in st.session_state:
    st.session_state.messages = []

WEATHER_API_KEY = "5c0812134a59c831e3002d7730393cb0"
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

GOOGLE_API_KEY = "AIzaSyD45DAm3TRq3QytKjCJqnL0DYRDF-2W_HA" 
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def fetch_weather_data(city, units="metric"):
    """Fetch current weather data"""
    try:
        params = {"q": city, "appid": WEATHER_API_KEY, "units": units}
        response = requests.get(WEATHER_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def fetch_forecast_data(city, units="metric"):
    """Fetch forecast weather data"""
    try:
        params = {"q": city, "appid": WEATHER_API_KEY, "units": units}
        response = requests.get(FORECAST_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching forecast data: {e}")
        return None

def format_weather_data(weather_data, forecast_data, units):
    """Format weather data for LLM consumption"""
    unit_symbol = "°C" if units == "metric" else "°F"
    speed_unit = "m/s" if units == "metric" else "mph"
    
    current = {
        "temperature": f"{weather_data['main']['temp']}{unit_symbol}",
        "feels_like": f"{weather_data['main']['feels_like']}{unit_symbol}",
        "humidity": f"{weather_data['main']['humidity']}%",
        "wind_speed": f"{weather_data['wind']['speed']} {speed_unit}",
        "description": weather_data['weather'][0]['description'],
        "pressure": f"{weather_data['main']['pressure']} hPa"
    }
    
    forecast = []
    for item in forecast_data['list'][:8]:
        forecast.append({
            "time": datetime.fromtimestamp(item['dt']).strftime("%I %p"),
            "temperature": f"{item['main']['temp']}{unit_symbol}",
            "description": item['weather'][0]['description']
        })
    
    return {
        "location": f"{weather_data['name']}, {weather_data['sys']['country']}",
        "current_conditions": current,
        "forecast": forecast
    }

def generate_weather_report(data, report_type):
    """Generate specialized weather report using Gemini"""
    try:
        prompts = {
            "News Style": f"""You are a professional weather reporter. Create a news-style weather report for {data['location']} 
                            using this weather data: {json.dumps(data, indent=2)}. Make it engaging and informative, 
                            highlighting key weather patterns and what people should expect. Keep it to 2-3 paragraphs.""",
            
            "Travel Advisory": f"""You are a travel advisor. Based on this weather data for {data['location']}: 
                                 {json.dumps(data, indent=2)}, create a detailed travel advisory. Include recommendations 
                                 for activities, what to wear, and any precautions travelers should take. Focus on practical advice.""",
            
            "Technical Analysis": f"""You are a meteorologist. Provide a technical analysis of the weather conditions in 
                                    {data['location']} using this data: {json.dumps(data, indent=2)}. Include analysis of 
                                    pressure systems, temperature patterns, and anticipated weather developments. Use technical 
                                    terminology but make it understandable."""
        }
        
        response = model.generate_content(prompts[report_type])
        return response.text
    except Exception as e:
        st.error(f"Error generating weather report: {str(e)}")
        return "Sorry, I couldn't generate the weather report at this time. Please try again later."

def weather_chatbot(user_input, weather_data):
    """Advanced weather and environmental chatbot using Gemini"""
    try:
        context = f"""You are a knowledgeable expert in weather, climate, environmental science, and public health for {weather_data['location']}. 
                     Current weather data: {json.dumps(weather_data, indent=2)}
                     
                     Provide comprehensive insights across these interconnected domains:

                     1. Current Weather & Immediate Impacts:
                        - Real-time weather conditions and forecasts
                        - Air quality and pollution levels
                        - Pollen counts and allergen levels
                        - UV index and sun exposure risks
                        - Impact on daily activities and traffic
                        
                     2. Health & Safety Considerations:
                        - Weather-related health risks (heat exhaustion, frostbite, etc.)
                        - Air quality impacts on respiratory health
                        - Seasonal illness patterns
                        - Outdoor activity safety recommendations
                        - Natural disaster preparedness
                        - Environmental health hazards
                        
                     3. Historical Patterns & Local Knowledge:
                        - Regional weather patterns and extremes
                        - Seasonal health trends
                        - Natural disaster history
                        - Local environmental challenges
                        - Traditional weather wisdom and local adaptations
                        
                     4. Environmental & Climate Factors:
                        - Climate change impacts on local weather
                        - Sea level rise risks
                        - Urban heat island effects
                        - Local ecosystem health
                        - Environmental sustainability challenges
                        
                     5. Geographic & Urban Considerations:
                        - Terrain and elevation effects
                        - Urban planning impacts
                        - Green spaces and their benefits
                        - Water body influences
                        - Local infrastructure resilience
                        
                     When answering questions:
                     - Connect weather conditions to health impacts
                     - Consider both immediate and long-term effects
                     - Provide practical, actionable advice when relevant
                     - Acknowledge the interconnected nature of weather, health, and environment
                     - Include both general guidelines and location-specific insights
                     
                     For sensitive topics (health, safety, future predictions):
                     - Provide evidence-based information
                     - Acknowledge uncertainty when appropriate
                     - Focus on empowering users with information
                     - Suggest reliable sources for more specific guidance
                     - Consider both individual and community impacts

                     Be conversational yet informative, like a knowledgeable local expert who understands
                     the complex relationships between weather, climate, health, and the environment."""
        
        prompt = f"{context}\n\nUser Question: {user_input}\n\nResponse:"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error in chatbot response: {str(e)}")
        return "I apologize, but I'm having trouble processing your request right now. Please try again later."

st.title("🤖 AI Weather Analysis")
st.write("Get AI-powered insights about weather conditions and chat with our weather expert!")

with st.container():
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        city = st.text_input("Enter City Name", placeholder="e.g., Atlanta")

    with col2:
        units = st.radio("Temperature Units", ["Metric (°C)", "Imperial (°F)"])
        units_code = "metric" if "Metric" in units else "imperial"

    with col3:
        report_type = st.selectbox(
            "Report Type",
            ["News Style", "Travel Advisory", "Technical Analysis"]
        )

    if st.button("Get AI Analysis"):
        if not city.strip():
            st.error("Please enter a valid city name.")
        else:
            with st.spinner("Fetching weather data and generating analysis..."):
                weather_data = fetch_weather_data(city.strip(), units_code)
                forecast_data = fetch_forecast_data(city.strip(), units_code)
                
                if weather_data and forecast_data:
                    st.session_state.weather_data_formatted = format_weather_data(weather_data, forecast_data, units_code)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📊 Current Conditions")
                        st.write(f"**Location:** {st.session_state.weather_data_formatted['location']}")
                        st.write(f"**Temperature:** {st.session_state.weather_data_formatted['current_conditions']['temperature']}")
                        st.write(f"**Humidity:** {st.session_state.weather_data_formatted['current_conditions']['humidity']}")
                        st.write(f"**Wind Speed:** {st.session_state.weather_data_formatted['current_conditions']['wind_speed']}")
                        st.write(f"**Description:** {st.session_state.weather_data_formatted['current_conditions']['description'].capitalize()}")
                    
                    with col2:
                        st.subheader("🤖 AI Weather Report")
                        report = generate_weather_report(st.session_state.weather_data_formatted, report_type)
                        st.write(report)

with st.container():
    st.subheader("💬 Chat with Weather Expert")
    
    if st.session_state.weather_data_formatted is None:
        st.info("Please fetch weather data first by entering a city name above.")
    else:
        st.write("Ask me anything about the current weather conditions or forecast!")

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask about the weather..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                response = weather_chatbot(prompt, st.session_state.weather_data_formatted)
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
