# Travel Agent – AI-Powered Trip Planner & Expense Manager  

Travel Agent is an AI-powered tool that helps users plan trips end-to-end.  
It uses **LangGraph agentic orchestration** to fetch attractions, weather forecasts, hotels, restaurants, and generate itineraries while estimating expenses in the user’s preferred currency.  
The system integrates multiple APIs for real-time data and provides an interactive experience via a **Streamlit dashboard**.  

---

## Demo Screenshots  

### Streamlit Dashboard – Home Page  
  
![Streamlit Home](artifacts/assets/pic_2.png) 

### Streamlit Dashboard – Output 

![Streamlit Home](artifacts/assets/pic_3.png) 

![Streamlit Home](artifacts/assets/pic_4.png) 

![Streamlit Home](artifacts/assets/pic_5.png) 

---

## Table of Contents  
- [Project Overview](#project-overview)  
- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Streamlit App](#streamlit-app)  
- [API Keys Required](#api-keys-required)  
- [How It Works](#how-it-works)  
- [Architecture](#architecture)  
- [Requirements](#requirements)  
- [Troubleshooting](#troubleshooting)  

---

## Project Overview  
Travel Agent makes trip planning seamless by combining real-time data sources with AI reasoning.  
It automates:  
- Finding **top attractions & activities**  
- Fetching **weather forecasts** for travel dates  
- Recommending **hotels & restaurants**  
- Generating **itineraries** day by day  
- Performing **currency conversion**  
- Estimating **total expenses** with breakdowns  

The project is powered by **LangGraph**, where each agent node has a role in the workflow:  

- **Attraction Agent** – fetches and ranks top places to visit  
- **Weather Agent** – retrieves weather forecasts for chosen dates  
- **Filter Agent** – eliminates activities based on weather conditions  
- **Hotel Agent** – finds hotels based on budget and location  
- **Restaurant Agent** – suggests dining options  
- **Itinerary Agent** – generates day-wise plan  
- **Currency Agent** – performs conversions to user’s native currency  
- **Expense Agent** – calculates estimated trip cost  
- **Supervisor Agent** – manages flow, validation, and retries  

---

## Features  
- 🌍 **Attractions & Activities** – fetches top tourist spots dynamically  
- ☀️ **Weather-aware filtering** – suggests activities that suit the forecast  
- 🏨 **Hotel Recommendations** – fetches real options with ratings & pricing  
- 🍽️ **Restaurant Suggestions** – local dining recommendations  
- 📝 **Smart Itinerary** – generates structured daily plan  
- 💱 **Currency Conversion** – converts costs to user’s currency  
- 💰 **Expense Estimation** – breakdown of hotel, food, and activities  
- 🎛️ **Streamlit Dashboard** – simple UI for interaction  

---

## Installation  
```bash
git clone https://github.com/your-username/Travel-Agent.git
cd Travel-Agent
pip install -r requirements.txt
```
---

## Usage

```bash
streamlit run app.py
```
---

## Streamlit App

The Streamlit dashboard provides:

*   User input form(city,dates,budget,currency)
*   Real-time retrieval of data from APIs
*   Day-wise itinerary & cost summary
*   Interactive outputs with links(hotels,restaurants,attractions)

---

## API Keys Required

You will need the following API keys (set them in your `.env` file):

*   **OpenAI API Key**-for summarization,filtering and itinerary generation
*   **Serper API Key** – to fetch top attractions (Places API)
*   **Weather API Key**- for weather forecasts (weatherapi.com)
*   **Currency Conversion API Key**- for real time currency conversion values (ExchangeRate.com)


Your final `.env` will look like:

```bash
OPENAI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here
HOTEL_API_KEY=your_key_here
CURRENCY_API_KEY=your_key_here
```
---

## How It Works

1.  User enters travel details (city, dates, budget, currency).
2.  Attractions are fetched via **Serper API**.
3.  Weather data retrieved via **Weather API**.
4.  Activities filtered based on forecast.
5.  Hotels & restaurants fetched using external APIs.
6.  Itinerary generated using OpenAI reasoning.
7.  Costs estimated and converted into user’s currency.
8.  Streamlit displays results interactively.

---

## Architecture

*   **LangGraph Layer** – agentic orchestration & routing

*   **LLM Layer (OpenAI)** – reasoning, summarization, itinerary generation

*   **External API Layer** – attractions, weather, hotels, restaurants, currency

*   **Streamlit Layer** – interactive frontend

*   **Logging & Validation** – retry logic, error handling

---

## Requirements

*   Python 3.9+

*   Streamlit

*   LangGraph

*   OpenAI Python SDK

*   Requests / httpx

*   dotenv

---

## Troubleshooting

*   API request failing: check that the correct API key is in .env.

*   Streamlit not running: run streamlit run streamlit_app.py from project root.

*   Hotels not showing: may be due to missing/expired hotel API key.

*   Currency mismatch: ensure conversion API key is active.