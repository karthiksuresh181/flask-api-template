from flask import Blueprint

weather = Blueprint(name="weather_blueprint", import_name=__name__)


@weather.route('/weather', methods=['GET'])
def get_weather_information():
    return {"Temperature": "30"}
