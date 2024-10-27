import requests
import json
import time

def get_data_from_url(url: str):
    # Get data from the URL as a JSON object
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        if response.text:
            lines = response.text.splitlines()
            return [json.loads(line) for line in lines]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
        print("Response text:", response.text)
    return None

def get_cdn_location(data):
    counter = 1
    countries = {}

    for obj in data:

        if "result" not in obj:
            print(f"Skipping entry {counter} due to missing 'result'")
            counter += 1
            continue
        
        src = obj["from"]

        time.sleep(1)
        city, country = get_country(src)
        if country is None:
            print(f"Skipping IP {src} due to failed lookup")
            continue
        
        
        hops = len(obj.get("result", [])) 
        if(country not in countries):
            countries[country] = [hops]
        else:
            countries[country].append(hops)
        
        print(counter)
        counter += 1
    return countries

# Function to get country from IP using ip-api.com
def get_country(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        response.raise_for_status()
        try:
            data = response.json()
            return data.get('city'), data.get("country", "Unknown")
        except json.JSONDecodeError:
            print(f"JSON decoding failed for IP {ip}. Response: {response.text}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for IP {ip}: {e}")
        return None, None

def main():
    data = {"aws": get_data_from_url("https://atlas.ripe.net/api/v2/measurements/80602537/results/?start=1729461900&stop=1729881081&format=txt"),
    "google": get_data_from_url("https://atlas.ripe.net/api/v2/measurements/80604372/results/?start=1729461900&stop=1729881277&format=txt"),
    "cf": get_data_from_url("https://atlas.ripe.net/api/v2/measurements/80602406/results/?start=1729461900&stop=1729881421&format=txt"),
    "azure": get_data_from_url("https://atlas.ripe.net/api/v2/measurements/80602889/results/?start=1729461900&stop=1729881517&format=txt")}

    arr = ["aws", "google", "cf", "azure"]
    for name in arr:
        with open(f'hops_{name}.txt', 'w') as file:
            countries = get_cdn_location(data[name])

            for country, details in countries.items():
                # Convert country data to JSON and write to file
                file.write(f"{country}: {json.dumps(details)}\n")

if __name__ == "__main__":
    main()
