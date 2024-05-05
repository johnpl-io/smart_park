import folium
from time import sleep
from IPython.display import display, clear_output

# Define the coordinates for the path
path = [
    (34.0522, -118.2437),  # Los Angeles
    (36.1699, -115.1398),  # Las Vegas
    (37.7749, -122.4194)   # San Francisco
]

# Create a map centered around the starting point
m = folium.Map(location=path[0], zoom_start=6)

# Loop over the coordinates, updating the map
for coord in path:
    clear_output(wait=True)
    m = folium.Map(location=coord, zoom_start=6)
    folium.Marker(coord).add_to(m)
    display(m)
    sleep(1)  # Pause for 1 second

