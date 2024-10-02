import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from dotenv import load_dotenv
from services.calculators.running import calculate_average_run_time, calculate_average_run_pace, calculate_suggested_runs
from services.calculators.cycling import calculate_average_ride_pace, calculate_average_ride_time, calculate_suggested_rides
from services.calculators.swimming import calculate_average_swim_pace, calculate_average_swim_time, calculate_suggested_swims 

load_dotenv()

strava_url = 'https://www.strava.com/api/v3/'
STRAVA_CLIENT_SECRET = os.environ['STRAVA_CLIENT_SECRET']
STRAVA_CLIENT_ID = os.environ['STRAVA_CLIENT_ID']

def get_stats(strava_stats: dict) -> dict:
    average_ride_pace = calculate_average_ride_pace(strava_stats)
    average_ride_time = calculate_average_ride_time(strava_stats)
    suggested_rides = calculate_suggested_rides(average_ride_pace, average_ride_time)
    average_run_pace = calculate_average_run_pace(strava_stats)
    average_run_time = calculate_average_run_time(strava_stats)
    suggested_runs = calculate_suggested_runs(average_run_pace, average_run_time)
    average_swim_pace = calculate_average_swim_pace(strava_stats)
    average_swim_time = calculate_average_swim_time(strava_stats)
    suggested_swims = calculate_suggested_swims(average_swim_pace, average_swim_time)
    return {"suggested_rides": suggested_rides, "suggested_runs": suggested_runs, "suggested_swims": suggested_swims}

class StravaStatsView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        return Response({"message": "Received"}, status=200)
    
    def get(self, request, format=None):
        athlete_id = request.query_params.get('athlete_id')
        access_token = request.query_params.get('access_token')
        url = strava_url + f'athletes/{athlete_id}/stats'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        print(headers)
        print(url)
        response = requests.get(url, headers=headers)
        print(response)
        
        if response.status_code >= 400:
            return Response({"message": "Error from Strava API", "details": response.json()}, status=response.status_code)
        
        suggested_workouts = get_stats(response.json())
        
        print('suggested workouts', suggested_workouts)
        
        return Response({"suggested_workouts": suggested_workouts}, status=200)