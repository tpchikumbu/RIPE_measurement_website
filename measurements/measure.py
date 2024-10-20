import requests

def get_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def main():
    url = "https://atlas.ripe.net/api/v2/measurements/80566292/results/?format=txt"
    data = get_data_from_url(url)
    if data:
        print(data)
        

if __name__ == "__main__":
    main()