# 🤖 AtmosAI - AI-Powered Weather Chatbot and Dashboard  

## 📖 Overview  

**AtmosAI** is an AI-driven weather application designed to provide real-time weather analysis and insights. It integrates the OpenWeather API for weather data and Google’s Gemini AI model to power an interactive chatbot, offering tailored weather reports and discussions on environmental impacts, health, and climate. 

Developed as part of Georgia Tech's CS1301 course, this project introduced key concepts in exploratory data analysis (EDA) using Python libraries like Pandas and Matplotlib, alongside practical experience with API integration.

You can test it out by clicking the following link: https://atmos-ai.streamlit.app/

---  

## 🚀 Features  

1. **AI-Driven Weather Chatbot**:  
   - Provides personalized weather insights and tailored reports (News Style, Travel Advisory, and Technical Analysis).  
   - Engages in interactive discussions about weather, health, and environmental considerations.  

2. **Real-Time Weather Dashboard**:  
   - Displays current weather conditions and multi-day forecasts.  
   - Interactive visualizations for temperature and humidity trends using Plotly.  
   - Customizable metrics for user-defined insights.  

3. **Weather Reports Using LLMs**:  
   - Generates detailed weather reports based on real-time data.  
   - Combines data visualization and AI-driven analysis for comprehensive insights.  

---  

## 📊 Data Sources  

- **OpenWeather API**: Provides real-time weather and forecast data.  
- **Google Generative AI (Gemini)**: Powers the chatbot and weather report generation.  

---  

## 🖼️ Key Components  

### **1. Weather Dashboard (🌦️_Weather_Dashboard.py)**  
   - Visualizes real-time and forecasted weather data.  
   - Features customizable metrics for temperature, humidity, and forecast durations (current day, 3-day, and 5-day).  

### **2. AI Weather Chatbot (🤖_Weather_Analysis_Chatbot.py)**  
   - AI-powered chatbot for tailored weather insights.  
   - Generates context-specific reports for news, travel advisories, and technical weather analysis.  

### **3. Interactive Visualizations**  
   - Uses Plotly for dynamic temperature and humidity charts.  
   - Forecast trends displayed with detailed annotations for better understanding.  

---  

## 📦 Installation  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/yourusername/AtmosAI.git  
   cd AtmosAI  
   ```  

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Run the Streamlit app:  
   ```bash  
   streamlit run 🌦️_Weather_Dashboard.py  
   ```  

---  

## 💡 How It Works  

1. **Data Processing**:  
   - Fetches real-time weather data using the OpenWeather API.  
   - Processes and formats weather forecasts for AI consumption.  

2. **AI Chatbot**:  
   - Generates context-aware responses using Google Generative AI.  
   - Provides insights on weather impacts, health, and environmental factors.  

3. **Visualization Tools**:  
   - Presents weather trends through dynamic and interactive charts.  
   - Allows users to explore temperature and humidity across different time periods.  

---  

## 📦 Dependencies  

This project requires:  
- **Python 3.7+**  
- **Streamlit**: For interactive UI.  
- **Google Generative AI**: For chatbot and report generation.  
- **Plotly**: For dynamic data visualizations.  
- **Pandas**: For data handling.  
- **Requests**: To fetch weather data from APIs.  
- **Matplotlib**: For additional plotting.  

To install all dependencies, run:  
```bash  
pip install -r requirements.txt  
```  

---  

## 📝 License  

This project is open-source and available under the [MIT License](LICENSE).  

---  
