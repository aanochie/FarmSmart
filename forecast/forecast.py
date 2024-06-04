from flask import Flask, render_template, request, Blueprint
import requests
from app import login_required
# Written by: Zheng (c2041164)
forecast_bp = Blueprint('forecast', __name__, template_folder='templates')


@forecast_bp.route('/forecast', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        # Get user's input from the form
        postcode = request.form['postcode']

        # Check if the postcode is empty and return a message if it is
        if not postcode:
            message = "Please enter postcode"
            return render_template('forecast/forecast.html', message=message)

        # API key for the weather service
        api_key = '284b5275cc1d04e72de867edb9e50c5c'
        base_url = "http://api.weatherstack.com/current"
        # Construct the complete URL for the API request
        complete_url = base_url + "?access_key=" + api_key + "&query=" + postcode

        # Make the request to the weather API
        response = requests.get(complete_url)
        # Parse the response JSON
        data = response.json()

        # Extract data from the API response
        location = data['location']['name']
        temperature = data['current']['temperature']
        description = data['current']['weather_descriptions'][0]
        wind_speed = data['current']['wind_speed']
        wind_degree = data['current']['wind_degree']
        humidity = data['current']['humidity']
        feelslike = data['current']['feelslike']
        visibility = data['current']['visibility']
        wind_dir = data['current']['wind_dir']
        uv_index = data['current']['uv_index']
        cloudcover = data['current']['cloudcover']
        precip = data['current']['precip']
        pressure = data['current']['pressure']
        icon_url = data['current']['weather_icons'][0]

        # Render the forecast.html template with the weather data
        return render_template('forecast/forecast.html',
                               location=location,
                               temperature=temperature,
                               wind_speed=wind_speed,
                               description=description,
                               wind_degree=wind_degree,
                               humidity=humidity,
                               feelslike=feelslike,
                               visibility=visibility,
                               wind_dir=wind_dir,
                               uv_index=uv_index,
                               cloudcover=cloudcover,
                               precip=precip,
                               pressure=pressure,
                               icon_url=icon_url)
    else:
        # Render the forecast.html template without weather data
        return render_template('forecast/forecast.html')

