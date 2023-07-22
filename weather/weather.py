import requests

def get_weather_info(api_key, location):
    base_url = "http://api.weatherstack.com/current"

    params = {
        "access_key": api_key,
        "query": location
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        data = response.json()

        if "error" in data:
            return {"error": data["error"]["info"]}

        # Extracting the required weather information from the JSON response
        temperature = data["current"]["temperature"]
        weather_description = data["current"]["weather_descriptions"][0]
        humidity = data["current"]["humidity"]
        wind_speed = data["current"]["wind_speed"]
        
        # Construct the weather information response
        weather_info = {
            "location": location,
            "temperature": f"{temperature}°C",
            "description": weather_description,
            "humidity": f"{humidity}%",
            "wind_speed": f"{wind_speed} km/h"
        }
        
        return weather_info
        
    except requests.exceptions.HTTPError as errh:
        return {"error": f"Http Error: {errh}"}
    except requests.exceptions.ConnectionError as errc:
        return {"error": f"Error Connecting: {errc}"}
    except requests.exceptions.Timeout as errt:
        return {"error": f"Timeout Error: {errt}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"OOps: Something Else {err}"}

# Lambda handler function
def lambda_handler(event, context):
    # Replace 'YOUR_API_KEY' with your actual weatherstack API key
    api_key = "40ba0bb8ee6553e4d72261f34e881328"
    
    # Extract the location from the Lambda event object
    location = event["location"]
    
    weather_info = get_weather_info(api_key, location)
    return weather_info

