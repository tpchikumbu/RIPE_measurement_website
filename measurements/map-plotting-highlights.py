import matplotlib.pyplot as plt
import geopandas as gpd
import requests
import tempfile
import os

def download_world_map_data():
    """
    Downloads world map data from Natural Earth website
    Returns a GeoDataFrame with world boundaries
    """
    url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        response = requests.get(url)
        zip_path = os.path.join(tmpdir, "world.zip")
        
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        
        world = gpd.read_file(f"zip://{zip_path}")
    
    return world

def create_highlighted_map(countries_to_highlight_1, countries_to_highlight_2=None, title="Highlighted Countries Map", highlight_colors=['#08519c', '#de2d26', '#31a354']):
    """
    Creates a map with specified countries highlighted
    
    Parameters:
    countries_to_highlight_1: List of country names to highlight with the first color
    countries_to_highlight_2: List of country names to highlight with the second color (optional)
    countries_to_highlight_3: List of country names to highlight with the third color (optional)
    title: Title for the map
    highlight_colors: List of colors to use for highlighted countries
    """
    # Load world map data
    try:
        world = download_world_map_data()
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None, None
    
    # Create figure and subplots
    fig, axs = plt.subplots(1, 2, figsize=(50, 28))
    
    # Set margins around the plot
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.1)
    
    # Create a color array
    world['color'] = 'lightgrey'  # Default color for non-highlighted countries
    
    # Plot highlighted countries on a given axis
    def plot_highlighted_countries(ax, countries, color, label):
        world['color'] = 'lightgrey'  # Reset colors
        if countries:
            # Use different image ranges for each region
            x_range, y_range = 30, 37
            if label == 'European Probes':
                x_range, y_range = 25, 25
            world.loc[world['NAME'].isin(countries), 'color'] = color
            # Center the map around the highlighted countries
            highlighted_geometry = world[world['NAME'].isin(countries)].geometry
            bounds = highlighted_geometry.total_bounds
            x_center = (bounds[0] + bounds[2]) / 2
            y_center = (bounds[1] + bounds[3]) / 2
            ax.set_xlim(x_center-x_range, x_center+x_range)
            ax.set_ylim(y_center-y_range, y_center+y_range)
            ax.set_aspect('equal')

        world.plot(ax=ax, color=world['color'], edgecolor='white')
        ax.set_title(label, fontsize=32)
        ax.axis('off')

    # Plot each set of highlighted countries on a different subplot
    plot_highlighted_countries(axs[0], countries_to_highlight_1, highlight_colors[0], 'African Probes')
    plot_highlighted_countries(axs[1], countries_to_highlight_2, highlight_colors[1], 'European Probes')
    
    # Add a legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=highlight_colors[0], label='African Probes'),
        Patch(facecolor=highlight_colors[1], label='European Probes'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', fontsize=48)
    
    # Title for the entire figure
    fig.suptitle(title, fontsize=48)
    
    # Hide axes for all subplots
    for ax in axs:
        ax.axis('off')
    
    return fig, axs

if __name__ == "__main__":
    # List of African countries
    african_countries = [
        'South Africa',
        'Kenya',
        'Malawi',
        'Tunisia',
        'Angola',
        'Mauritius',
        'Chad',
        'Burkina Faso',
    ]
    # List of European countries
    european_countries = [
        'Sweden',
        'Portugal',
        'Italy',
        'Ireland',
        'Romania'
    ]
    
    # Create the map
    fig, ax = create_highlighted_map(
        african_countries,
        european_countries,
        title="RIPE Atlas Probe Countries",
    )
    
    if fig is not None:
        plt.savefig('RIPE_probe_countries_big.png', bbox_inches='tight', dpi=20)
        plt.close()
