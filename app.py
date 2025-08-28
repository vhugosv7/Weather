from flask import Flask, render_template, request
import requests
from datetime import datetime


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form.get('location')
        return render_template('index.html', data=get_weather(location))
    #  'Mexico city' by default, to avoid an 'error' - Could be replaced.
    return render_template('index.html', data=get_weather('Mexico city'))


def get_weather(location) -> dict:
    try:
        #  API Access Key
        key = 'cf6ee8225dd9f2d57efd890a8674c051'
        url = f'''https://api.weatherstack.com/current?access_key={key}'''
        #  Getting the location from the input.
        querystring = {"query": location}
        response = requests.get(url, params=querystring)
        #  Get the response in JSON format.
        data = response.json()
        data['location']['localtime'] = date_format()
        # Returned as list, bucle for to iterate and clear format.
        for item in data['current']['weather_descriptions']:
            item.replace('[', '').replace(']', '').replace("'", '')
            data['current']['weather_descriptions'] = item

        # Assign the weather for a variable for best understanding.
        weather = data['current']['weather_descriptions']

        #  Asign an image according to the weather.
        if 'Sunny' in weather:
            data['current']['weather_icons'] = '/static/weather_status/sunny.svg'

        elif 'cloud' in weather or 'sunny_intervals' in weather:
            data['current']['weather_icons'] = '/static/weather_status/Partly cloudy.svg'

        elif 'clear' in weather:
            data['current']['weather_icons'] = '/static/weather_status/clear.svg'

        elif 'fog' in weather:
            data['current']['weather_icons'] = '/static/weather_status/fog.svg'

        elif 'mist' in weather:
            data['current']['weather_icons'] = '/static/weather_status/mist.svg'

        elif 'Rain' or 'rain' in weather:
            data['current']['weather_icons'] = '/static/weather_status/rain.svg'

        elif 'Cloudy' or 'cloudy' in weather:
            data['current']['weather_icons'] = '/static/weather_status/cloudy.svg'

        elif 'Overcast' in weather:
            data['current']['weather_icons'] = '/static/weather_status/overcast.svg'

        else:
            pass

        return data

    except KeyError:
        return 'error'


# Function to get format the date.
def date_format():
    current = datetime.now()
    format = current.strftime("%B %d, %A")
    return format


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
