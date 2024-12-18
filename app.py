from flask import Flask

import folium
import pandas as pd

app = Flask(__name__)

def get_locations(file_path):
    df = pd.read_csv(file_path)

    locations = []

    for _, row in df.iterrows():
        if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
            locations.append(
                {
                    'name': row['Name'],
                    'lat': row['Latitude'],
                    'lon': row['Longitude'],
                }
            )

    return locations


@app.route('/')
def index():
    start_coords = (40.6782, -73.9442)
    map = folium.Map(location=start_coords, zoom_start=13)

    locations = get_locations('results-clean-filtered.csv')

    for loc in locations:
        html = '{}'.format(loc['name'])
        iframe = folium.IFrame(html, width=100, height=100)
        folium.Marker(
            [loc['lat'], loc['lon']],
            popup=folium.Popup(iframe)
        ).add_to(map)

    return map._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)
