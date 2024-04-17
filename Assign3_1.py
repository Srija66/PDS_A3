import requests
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Fetch JSON data from OpenWeatherMap API
def fetch_weather_data(city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": "4982028bb491705e31064295d2b2dd34",  # Replace with your OpenWeatherMap API key
        "units": "metric"
    }
    response = requests.get(url, params=params)
    return response.json()

# Create Dash app
app = dash.Dash(__name__)

# Define layout of the dashboard
app.layout = html.Div([
    html.H1("Weather Dashboard"),
    html.Div([
        html.Label("Enter City:"),
        dcc.Input(id='city-input', type='text', value='New York'),
        html.Button('Submit', id='submit-button', n_clicks=0),
    ]),
    html.Div(id='weather-info'),
])

# Define callback to update weather information
@app.callback(
    Output('weather-info', 'children'),
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('city-input', 'value')]
)
def update_weather_info(n_clicks, city):
    weather_data = fetch_weather_data(city)
    temperature = weather_data.get('main', {}).get('temp', 'N/A')
    humidity = weather_data.get('main', {}).get('humidity', 'N/A')
    description = weather_data.get('weather', [{}])[0].get('description', 'N/A')
    return html.Div([
        html.H3(f"City: {city}"),
        html.H4(f"Temperature: {temperature} °C"),
        html.H4(f"Humidity: {humidity}%"),
        html.H4(f"Description: {description}")
    ])

if __name__ == '__main__':
    app.run_server(debug=True)