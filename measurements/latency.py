import requests
import json
import time
import matplotlib.pyplot as plt


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
    latency_measurements = {}
    if data:
        count = 0
        for obj in data:
            prb_id = obj["prb_id"]
            src_ip = obj["from"]
            ping_avg = obj["avg"]
            server = obj["dst_name"]
            count += 1
            
            

            print(f"Probe ID: {prb_id}, {src_ip}, {ping_avg}")
            # for result in obj["result"]:
            ##########################################
            country = get_country(src_ip)
            print("--------------------")
            
            print(server)
            if server == "d2idaxovs4aj5h.cloudfront.net":
                service = "aws"
            elif server == "ripe-measurement-demo.pages.dev":
                service = "cloudflare"
            elif server == "purple-wave-0cddfaf1e.5.azurestaticapps.net":
                service = "azure"
            else:
                service = "google"
                
            
            country_service = country + "_"+ service
            print(count)
            print(country_service)
            
            if(latency_measurements.get(country_service) == None):
                latency_measurements[country_service] = [ping_avg]
            else:
                latency_measurements[country_service].append(ping_avg)
            
            
    return latency_measurements

def get_med_lat(data):
    # Get the RTT of the ping
    latency_measurements = []
    if data:
        count = 0
        for obj in data:
            prb_id = obj["prb_id"]
            src_ip = obj["from"]
            ping_avg = obj["avg"]
            server = obj["dst_name"]
            count += 1
            
            
            latency_measurements.append(float(ping_avg))
            print(f"Probe ID: {prb_id}, {src_ip}, {ping_avg}")
    median_measure = statistics.median(latency_measurements)
    return median_measure
    

# Function to get country from IP using ip-api.com
def get_country(ip):
    time.sleep(1)  # Basic rate limiting
    response = requests.get(f"http://ip-api.com/json/{ip}")
    data = response.json()
    
    return data.get("country", "Unknown")


# Define the function to transform the input data into the required format for plotting
def transform_data_for_plot(input_data):
    # Initialize an empty dictionary for transformed data
    transformed_data = {}
    
    # Loop through the input dictionary to organize data by country and metric
    for key, values in input_data.items():
        # Split the key to extract country name and metric
        country, metric = key.split('_')
        
        # Initialize the country's entry in transformed_data if not already present
        if country not in transformed_data:
            transformed_data[country] = []
        
        # Append the metric data (values) to the country's list
        transformed_data[country].append(values)

    return transformed_data



def box_plot_data(sorted_data):
    # Initialize the plot
    
    # Define metric names and assign colors to each one
    metric_names = ['AWS', 'Azure', 'Cloudflare', 'Google']
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']
    
    fig, ax = plt.subplots(figsize=(13, 6))

    # Track position offsets for each country
    positions = []
    country_names = []
    start_pos = 0  # Initial position on x-axis

    # Loop through each country in the transformed data
    for country, metrics in sorted_data.items():
        num_metrics = len(metrics)  # Get the number of metrics for each country
        # # Plot each metric as a box plot
        # bp = ax.boxplot(metrics, positions=range(start_pos, start_pos + num_metrics), widths=0.6)
        
        # Plot each metric as a box plot with a specified color
        for i, metric_data in enumerate(metrics):
            ax.boxplot(metric_data, positions=[start_pos + i], widths=0.6, patch_artist=True,
                    boxprops=dict(facecolor=colors[i], color=colors[i]),
                    medianprops=dict(color='black'), showfliers=False  )
        
        # Save positions for custom tick labels
        positions.append(start_pos + num_metrics // 2)  # Middle position for the country label
        country_names.append(country)
        
        # Update start_pos for the next country
        start_pos += num_metrics + 2  # Add spacing between countries
        
    for i, metric_name in enumerate(metric_names):
        ax.plot([], [], color=colors[i], label=metric_name)

    # Set x-ticks and labels to display country names
    ax.set_xticks(positions)
    ax.set_xticklabels(country_names)
    plt.legend(title="Cloud Service Providers")
    ax.set_ylabel('Latency (ms)')
    ax.set_title('Box Plot of Latency Measures By Country Per Cloud Service Provider')
    

    plt.show()

def write_into_file(data):
    # Write to file
    with open('actual_box_plot_data.txt', 'w') as file:
        for key, values in data.items():
            line = f"{key}: {','.join(map(str, values))}\n"
            file.write(line)

def read_from_file(file_name):
    data = {}
    with open(file_name, 'r') as file:
        for line in file:
            # Split the line at the colon to separate the key and values
            key, values = line.strip().split(': ')
            # Convert the comma-separated values to a list of floats
            values_list = list(map(float, values.split(',')))
            # Store the key and values list in the dictionary
            data[key] = values_list
        return  data


import statistics

def calculate_latency_medians_from_file(filename):
    #39.0944977 (african cdn)
    #96.70515066666667 (africa region)
    #11.7400 (europe cdn)
    #47.545002000000004 (europe data centre)
    """
    Read latency data from a file and calculate medians for each country.
    
    Args:
        filename (str): Path to the file containing latency data
        
    Returns:
        dict: Dictionary with country names and their median latencies, sorted by median value
    """
    # Dictionary to store country data
    country_data = {}
    
    try:
        with open(filename, 'r') as file:
            current_country = None
            total_valid_values = []
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                
                # Check if line contains country name
                if '_aws:' in line:
                    current_country = line.split('_aws:')[0]
                    values_str = line.split('_aws:')[1].strip()
                    
                    # Convert string of values to floats, removing invalid values
                    values = [float(x.strip()) for x in values_str.split(',')]
                    valid_values = [x for x in values if x > 0]  # Remove negative values
                    #print(valid_values)
                    total_valid_values += valid_values
                    
                    if valid_values:
                        median = statistics.median(valid_values)
                        country_data[current_country] = median
    
        # Sort results by median value
        sorted_results = dict(sorted(country_data.items(), key=lambda x: x[1]))
        total_median = statistics.median(total_valid_values)
        return total_median
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None


import matplotlib.pyplot as plt
import numpy as np

def plot_latency_comparison():
    # Data
    categories = ['Africa CDN', 'Africa DC', 'Europe CDN', 'Europe DC']
    values = [39.0944977, 96.70515067, 11.7400, 47.54500200]
    
    # Create bar plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, values)
    
    # Customize the plot
    plt.title('CDN vs Data Centre Latency Comparison', fontsize=14, pad=20)
    plt.ylabel('Latency (ms)', fontsize=12)
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}ms',
                ha='center', va='bottom')
    
    # Customize colors
    bars[0].set_color('#2E86C1')  # Africa CDN
    bars[1].set_color('#EC7063')  # Africa DC
    bars[2].set_color('#2E86C1')  # Europe CDN
    bars[3].set_color('#EC7063')  # Europe DC
    
    # Add grid for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=0)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    return plt

# Example usage:

def main():
    #get the 4 urls (AFRICAN COUNTRIES)
    # url_aws = "https://atlas.ripe.net/api/v2/measurements/80602536/results/?start=1729461600&stop=1729944314&format=txt"
    # url_azure = "https://atlas.ripe.net/api/v2/measurements/80602888/results/?start=1729461600&stop=1729944275&format=txt"
    # url_cloudflare = "https://atlas.ripe.net/api/v2/measurements/80602405/results/?start=1729461600&stop=1729944229&format=txt"
    # url_google = "https://atlas.ripe.net/api/v2/measurements/80604371/results/?start=1729461600&stop=1729944176&format=txt"
    # data = get_data_from_url(url_aws)
    # data = data + get_data_from_url(url_azure)
    # data = data + get_data_from_url(url_cloudflare)
    # data = data + get_data_from_url(url_google)
    #url_aws_africa = "https://atlas.ripe.net/api/v2/measurements/80797668/results/?format=txt"
    # url_aws_europe = "https://atlas.ripe.net/api/v2/measurements/80797618/results/?format=txt"
    # data_africa = get_data_from_url(url_aws_europe)
    # data_europe = get_data_from_url(url_aws_europe)
    #Europe
    # url_aws = "https://atlas.ripe.net/api/v2/measurements/80604435/results/?start=1729461600&stop=1729967369&format=txt"
    # url_azure = "https://atlas.ripe.net/api/v2/measurements/80604447/results/?start=1729461600&stop=1729967325&format=txt"
    # url_cloudflare = "https://atlas.ripe.net/api/v2/measurements/80603189/results/?start=1729461600&stop=1729967269&format=txt"
    # url_google = "https://atlas.ripe.net/api/v2/measurements/80604391/results/?start=1729461600&stop=1729967221&format=txt"
    
    # data = get_data_from_url(data_africa)
    # data = data + get_data_from_url(url_azure)
    # data = data + get_data_from_url(url_cloudflare)
    # data = data + get_data_from_url(url_google)
    # data = [1]
    #data = data_africa
    
    # plot = plot_latency_comparison()
    # plot.show()
     

    #if data:
        # latency_measures = get_ping_rtt(data)
        # write_into_file(latency_measures)
        # lat_meas = read_from_file('box_plot_data.txt')
        
        # sorted_latency_measurements = transform_data_for_plot(lat_meas)
        # box_plot_data(sorted_latency_measurements)
        #print(get_med_lat(data))
    
    print(calculate_latency_medians_from_file("EUROPE_box_plot_data.txt"))

if __name__ == "__main__":
    main()
    