import requests
import json

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
            print(f"Probe ID: {prb_id}")
            for result in obj["result"]:
                print(result["rtt"])
            print("--------------------")
    return None
     
def main():
    url = "https://atlas.ripe.net/api/v2/measurements/80566291/results/?format=txt"
    data = get_data_from_url(url)
    
    if data:
        get_ping_rtt(data)
        

if __name__ == "__main__":
    main()