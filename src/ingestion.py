import requests
import pandas as pd
from datetime import datetime

class PurpleAirIngestor:
    def __init__(self, api_read_key):
        self.api_key = api_read_key
        self.base_url = "https://api.purpleair.com/v1/sensors/"

    def estimate_cost(self, num_sensors, start_date, end_date, fields):
        # Formula based on PurpleAir documentation:
        # Each request has a base cost, plus points per field per result row.
        base_cost = 2 
        field_cost_per_row = len(fields) * 0.2 # Standard historical rate
        
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        total_hours = (end - start).total_seconds() / 3600
        
        # We are using 'average=60' (hourly), so rows = total_hours
        estimated_rows = total_hours 
        
        total_points = (base_cost + (field_cost_per_row * estimated_rows)) * num_sensors
        return int(total_points)

    def fetch_historical_data(self, sensor_index, start_timestamp, end_timestamp, fields):
        headers = {"X-API-Key": self.api_key}
        params = {
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "fields": ",".join(fields),
            "average": 60 
        }
        response = requests.get(f"{self.base_url}{sensor_index}/history", headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['data'], columns=data['fields'])
            df['sensor_index'] = sensor_index
            return df
        return None
    
    def fetch_sensor_metadata(self, sensor_ids):
        # Fetches lat, lon, and other metadata for specific sensors.
        headers = {"X-API-Key": self.api_key}
        # Fields required for geocoding and metadata
        params = {
            "fields": "latitude,longitude,name,location_type",
            "show_only": ",".join(map(str, sensor_ids))
        }
        
        response = requests.get(self.base_url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            df_meta = pd.DataFrame(data['data'], columns=data['fields'])
            # Save metadata to persist for future use
            df_meta.to_csv("data/raw/sensor_metadata.csv", index=False)
            return df_meta
        else:
            print(f"Error fetching metadata: {response.status_code}")
            return None
