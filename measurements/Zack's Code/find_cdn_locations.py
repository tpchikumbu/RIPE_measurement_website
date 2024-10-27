import requests
import json
import time


def get_data_from_url(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status() 
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
    cities = {}
    unique_ip = []
    for obj in data:
        if "dst_addr" not in obj:
            print(f"Skipping entry {counter} due to missing 'dst_addr'")
            counter += 1
            continue

        dest_ip = obj["dst_addr"]

        if dest_ip in unique_ip:
            continue
        else:
            unique_ip.append(dest_ip)

        time.sleep(1)
        city, country = get_country(dest_ip)
        if city is None or country is None:
            print(f"Skipping IP {dest_ip} due to failed lookup")
            continue

        counter += 1
        countries[country] = countries.get(country, 0) + 1
        cities[city] = cities.get(city, 0) + 1

    return cities, countries

# Find the country using the IP
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

    aws_eu = get_data_from_url("https://atlas.ripe.net/api/v2/measurements/80604436/results/?start=1729461900&stop=1729880986&format=txt")
    aws_afr = get_data_from_url("https://atlas.ripe.net/api/v2/measurements/80602537/results/?start=1729461900&stop=1729881081&format=txt")
    
    if aws_afr:
        with open('africa_cdn.txt', 'w') as file:
            cities, countries = get_cdn_location(aws_afr)
            file.write(json.dumps(cities))
            file.write(json.dumps(countries))

if __name__ == "__main__":
    main()