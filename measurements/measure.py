import requests
import json
from collections import defaultdict

country_probe_map = defaultdict(set)

def get_data_from_url(url : str):
    # Get data from the URL as a JSON object
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        if response.text:
            lines = response.text.splitlines()
            return [json.loads(line) for line in lines]
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def get_ping_rtt(data):
    # Get the RTT of the ping
    if data:
        for obj in data:
            prb_id = obj["prb_id"]
            src_ip = obj["from"]
            print(f"Probe ID: {prb_id}")
            # for result in obj["result"]:
            loc = get_country(src_ip)
            country_probe_map[loc].add(prb_id)
            print("--------------------")
    return None

# Function to get country from IP using ip-api.com
def get_country(ip):
    response = requests.get(f"http://ip-api.com/json/{ip}")
    data = response.json()
    return data.get("country", "Unknown")
     
def main():
    url = "https://atlas.ripe.net/api/v2/measurements/80602536/results/?start=1729461600&stop=1729571509&format=txt"
    data = get_data_from_url(url)
    
    if data:
        get_ping_rtt(data)
        print(country_probe_map)
        

if __name__ == "__main__":
    main()