import folium
from flask import Flask, render_template_string, request, render_template

app = Flask(_name_)

# ----- CAMPUS MAP GENERATOR -----
def create_campus_map():
    # Center coordinates of your campus
    campus_center = [12.9352, 77.5340]  # Change to your college's latitude, longitude

    # Create base map
    campus_map = folium.Map(location=campus_center, zoom_start=17, tiles='CartoDB positron')

    # Add markers for key locations
    locations = {
        "Library": [12.9355, 77.5335],
        "Canteen": [12.9358, 77.5345],
        "Auditorium": [12.9360, 77.5350],
        "Admin Block": [12.9348, 77.5340],
        "Hostel": [12.9345, 77.5328]
    }

    for name, coord in locations.items():
        folium.Marker(
            location=coord,
            popup=f"<b>{name}</b>",
            tooltip=name,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(campus_map)
