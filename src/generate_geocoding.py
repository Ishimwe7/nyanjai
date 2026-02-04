import requests
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

def get_geoid_from_coords(lat, lon):
    #url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates"
    # params = {
    #     "x": lon, 
    #     "y": lat, 
    #     "benchmark": "Public_AR_Current",
    #     "vintage": "Census2020_Current",
    #     "format": "json"
    # }
    url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates"

    # Benchmark 4 = Public_AR_Current

    # Vintage 4 = Current_Current

    params = {
        "x": lon, 
        "y": lat, 
        "benchmark": "4", 
        "vintage": "4", 
        "format": "json"
    }

    # Setup a retry strategy
    retry_strategy = Retry(
        total=3,                          # Retry 3 times
        backoff_factor=1,                 # Wait 1s, 2s, 4s between retries
        status_forcelist=[429, 500, 502, 503, 504], # Retry on these errors
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)

    try:
        # Increase timeout to 20 seconds to give the server more room to breathe
        response = session.get(url, params=params, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            geos = data.get('result', {}).get('geographies', {})
            # Check both possible layer names
            bg_layer = geos.get('Census Block Groups') or geos.get('2020 Census Block Groups')
            
            if bg_layer:
                return bg_layer[0].get('GEOID')
        return None
        
    except Exception as e:
        print(f"Connection failed for {lat}, {lon}: {e}")
        return None