import requests
import json
import time

countries = {'Kenya': ['41.89.1.251', '212.22.174.222', '212.22.174.2', '41.212.57.66', '41.60.232.39', '105.21.42.14', '105.21.32.82', '196.6.220.42', '102.217.156.154'], 
             'Angola': ['197.149.149.17', '102.222.16.193'], 
             'Mauritius': ['102.113.47.249', '102.117.190.180', '196.192.112.245', '196.1.0.9', '102.117.44.222', '102.222.106.178']}

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
    cities = {}
    current = ""
    kenya = {}
    angola = {}
    mauritius = {}

    for obj in data:
        if obj['from'] in countries['Kenya']:
            current = "Kenya"
        elif obj['from'] in countries['Angola']:
            current = "Angola"
        elif obj['from']  in countries['Mauritius']:
            current = "Mauritius"
        else:
            current = ""
            continue

        if "dst_addr" not in obj:
            print(f"Skipping entry {counter} due to missing 'dst_addr'")
            counter += 1
            continue
        
        dest_ip = obj["dst_addr"]

        time.sleep(1)
        city, country = get_country(dest_ip)
        if city is None or country is None:
            print(f"Skipping IP {dest_ip} due to failed lookup")
            continue

        counter += 1
        if current == "Kenya":
            kenya[country] = kenya.get(country, 0) + 1
        elif current == "Angola":
            angola[country] = angola.get(country, 0) + 1
        elif current == "Mauritius":
            mauritius[country] = mauritius.get(country, 0) + 1

    return kenya, angola, mauritius

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
    aws_afr = get_data_from_url("https://atlas.ripe.net/api/v2/measurements/80602537/results/?start=1729461900&stop=1729881081&format=txt")
    
    if aws_afr:
        with open('neighbours.txt', 'w') as file:
            kenya, angola, mauritius = get_cdn_location(aws_afr)
            file.write("Kenya\n")
            file.write(json.dumps(kenya))
            file.write("\nAngola\n")
            file.write(json.dumps(angola))
            file.write("\nMauritius\n")
            file.write(json.dumps(mauritius))

if __name__ == "__main__":
    main()
