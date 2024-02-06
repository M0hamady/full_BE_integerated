
import requests


def get_place_from_location(latitude, longitude):
    api_key = 'AIzaSyBaKNNFMMwoe8fmhuk5fEWHHvyZDyQgxy8'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        results = data['results']
        if results:
            return results[0]['formatted_address']
        else:
            return 'No results found'
    else:
        return 'Geocoding API request failed'