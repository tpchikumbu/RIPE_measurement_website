import requests
import json
import time

neighbours = ["Kenya", "Angola", "Mauritius"]

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
    unique_ip = []
    
    for obj in data:
        if counter == 100:
            return countries
        
        if "from" not in obj:
            print(f"Skipping entry {counter} due to missing 'src_addr'")
            counter += 1
            continue

        src_ip = obj["from"]


        time.sleep(1)
        src_city, src_country = get_country(src_ip)

        if src_city is None or src_country is None:
            print(f"Skipping IP {src_ip} due to failed lookup")
            continue
        elif src_country in neighbours:
            if src_country in countries and src_ip not in countries[src_country]:
                countries[src_country].append(src_ip)
            else:
                countries[src_country] = [src_ip]

        counter += 1
        

    return countries

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
    data = get_data_from_url("https://atlas.ripe.net/api/v2/measurements/80602537/results/?start=1729461900&stop=1729881081&format=txt")

    if data:
        print(get_cdn_location(data))

if __name__ == '__main__':
    main()