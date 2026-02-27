import sqlite3
import folium
from folium.plugins import HeatMap
from distance_utils import calculate_distance


def generate_map():
    conn = sqlite3.connect("movement.db")
    cursor = conn.cursor()

    cursor.execute("SELECT latitude, longitude, timestamp, landmark FROM movements")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No movement data found.")
        return

    # Sort rows: timestamp first, null timestamps last
    rows_sorted = sorted(
        rows,
        key=lambda x: (x[2] is None or x[2] == "", x[2])
    )

    start_location = [rows_sorted[0][0], rows_sorted[0][1]]
    m = folium.Map(location=start_location, zoom_start=5)

    locations = []
    total_distance = 0

    for index, row in enumerate(rows_sorted, start=1):
        lat, lon, time, landmark = row
        locations.append([lat, lon])

        # Distance calculation
        if index > 1:
            prev_lat, prev_lon = rows_sorted[index-2][0], rows_sorted[index-2][1]
            total_distance += calculate_distance(prev_lat, prev_lon, lat, lon)

        # Numbered marker
        folium.Marker(
            [lat, lon],
            popup=f"Visit #{index}\n{landmark}\n{time}",
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size:14px;
                    color:white;
                    background:red;
                    border-radius:50%;
                    width:25px;
                    height:25px;
                    text-align:center;
                    line-height:25px;">
                    {index}
                </div>
                """
            )
        ).add_to(m)

    # Movement path
    folium.PolyLine(locations, color="blue", weight=3).add_to(m)

    # Heatmap
    HeatMap(locations).add_to(m)

    m.save("movement_map.html")

    print("Map generated: movement_map.html")
    print(f"Total Travel Distance: {total_distance:.2f} km")