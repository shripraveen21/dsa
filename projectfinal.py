from geopy.distance import geodesic
import heapq
import folium
import webbrowser
from tkinter import *


class RideMatchingService:
    def __init__(self):
        self.graph = {}
        self.drivers = []

    def add_location(self, name, edges):
        self.graph[name] = edges

    def add_driver(self, name, location):
        self.drivers.append({"name": name, "location": location})

    def find_shortest_path(self, start, end):
        distances = {location: float("inf") for location in self.graph}
        distances[start] = 0
        previous_locations = {location: None for location in self.graph}
        pq = [(0, start)]
        while pq:
            current_distance, current_location = heapq.heappop(pq)
            if current_distance > distances[current_location]:
                continue
            for neighbor, distance in self.graph[current_location]:
                new_distance = current_distance + distance
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_locations[neighbor] = current_location
                    heapq.heappush(pq, (new_distance, neighbor))
        path = []
        current_location = end
        while current_location != start:
            path.append(current_location)
            current_location = previous_locations[current_location]
        path.append(start)
        return path[::-1]

    def find_nearest_driver(self, start):
        nearest_driver = None
        min_distance = float("inf")
        for driver in self.drivers:
            path = self.find_shortest_path(start, driver["location"])
            distance = 0
            for i in range(len(path) - 1):
                distance += [x[1] for x in self.graph[path[i]] if x[0] == path[i+1]][0]
            if distance < min_distance:
                min_distance = distance
                nearest_driver = driver
        return nearest_driver

    def show_map(self, start, end, location_coords):
        m = folium.Map(location=location_coords[start], zoom_start=15)

        for location, coordinates in location_coords.items():
            folium.Marker(
                location=coordinates,
                icon=folium.Icon(color="red"),
                popup=location
            ).add_to(m)

        path = self.find_shortest_path(start, end)

        for i in range(len(path) - 1):
            loc1 = location_coords[path[i]]
            loc2 = location_coords[path[i + 1]]
            folium.PolyLine(
                locations=[loc1, loc2],
                color="red",
                weight=3,
                opacity=0.8
            ).add_to(m)

        source_lat, source_lon = location_coords[start]
        dest_lat, dest_lon = location_coords[end]
        distance_km = geodesic((source_lat, source_lon), (dest_lat, dest_lon)).km
        time_hours = distance_km / 60

        source_popup_content = f'''
        <!DOCTYPE html>
        <html>
          <head>
            <title>Driving Routes</title>
          </head>
          <body>
            <h1>Driving Directions</h1>
            <p>Source: {start}</p>
            <p>Destination: {end}</p>
            <p>Distance: {distance_km:.2f} km</p>
            <p>Estimated Time: {time_hours:.2f} hours</p>
          </body>
        </html>
        '''
        source_popup = folium.Popup(source_popup_content, max_width=250)
        folium.Marker(
            location=location_coords[start],
            icon=folium.Icon(color="red"),
            popup=source_popup
        ).add_to(m)

        for driver in self.drivers:
            driver_location = driver["location"]
            distance_driver_to_source = 0
            time_to_reach_driver_to_source = 0

            path_to_driver = self.find_shortest_path(start, driver_location)
            for i in range(len(path_to_driver) - 1):
                distance_driver_to_source += [
                    x[1] for x in self.graph[path_to_driver[i]]
                    if x[0] == path_to_driver[i + 1]
                ][0]
            time_to_reach_driver_to_source = distance_driver_to_source / 60

            popup_content = f'''
            <!DOCTYPE html>
            <html>
              <head>
                <title>Driver Details</title>
              </head>
              <body>
                <h1>Driver: {driver["name"]}</h1>
                <p>Distance to Source: {distance_driver_to_source:.2f} km</p>
                <p>Time to Reach Source: {time_to_reach_driver_to_source:.2f} hours</p>
              </body>
            </html>
            '''
            popup = folium.Popup(popup_content, max_width=250)
            if driver_location == self.find_nearest_driver(start)["location"]:
                folium.Marker(
                    location=location_coords[driver_location],
                    icon=folium.Icon(color="green"),
                    popup=popup
                ).add_to(m)
            else:
                folium.Marker(
                    location=location_coords[driver_location],
                    icon=folium.Icon(color="blue"),
                    popup=popup
                ).add_to(m)

        folium.Marker(
            location=location_coords[end],
            icon=folium.Icon(color="black"),
            popup="Destination"
        ).add_to(m)

        m.save("map.html")
        webbrowser.open("map.html")


def main():
    rms = RideMatchingService()

    location_coords = {
        "A": [11.00181192050863, 76.96284240627635],
        "B": [11.001805924614195, 76.96775084781647],
        "C": [11.004862098960513, 76.9643195271492],
        "D": [11.008062321360944, 76.96188813447952],
        "E": [11.012236420342886, 76.96526223421097],
        "F": [11.017950403276413, 76.96662217378616],
        "G": [10.890000000000000, 76.90880000000000],  
        "H": [11.010200000000000, 76.95040000000000]   
    }

    rms.add_location("A", [("B", geodesic(location_coords["A"], location_coords["B"]).km),
                           ("C", geodesic(location_coords["A"], location_coords["C"]).km),
                           ("G", geodesic(location_coords["A"], location_coords["G"]).km),
                           ("H", geodesic(location_coords["A"], location_coords["H"]).km)
                           ])
    rms.add_location("B", [("A", geodesic(location_coords["B"], location_coords["A"]).km),
                           ("C", geodesic(location_coords["B"], location_coords["C"]).km),
                           ("D", geodesic(location_coords["B"], location_coords["D"]).km),
                           ("G", geodesic(location_coords["B"], location_coords["G"]).km),
                           ("H", geodesic(location_coords["B"], location_coords["H"]).km)])
    rms.add_location("C", [("A", geodesic(location_coords["C"], location_coords["A"]).km),
                           ("B", geodesic(location_coords["C"], location_coords["B"]).km),
                           ("D", geodesic(location_coords["C"], location_coords["D"]).km),
                           ("E", geodesic(location_coords["C"], location_coords["E"]).km),
                           ("G", geodesic(location_coords["C"], location_coords["G"]).km),
                           ("H", geodesic(location_coords["C"], location_coords["H"]).km)])
    rms.add_location("D", [("B", geodesic(location_coords["D"], location_coords["B"]).km),
                           ("C", geodesic(location_coords["D"], location_coords["C"]).km),
                           ("E", geodesic(location_coords["D"], location_coords["E"]).km),
                           ("F", geodesic(location_coords["D"], location_coords["F"]).km),
                           ("G", geodesic(location_coords["D"], location_coords["G"]).km),
                           ("F", geodesic(location_coords["D"], location_coords["F"]).km)])
    rms.add_location("E", [("C", geodesic(location_coords["E"], location_coords["C"]).km),
                           ("D", geodesic(location_coords["E"], location_coords["D"]).km),
                           ("F", geodesic(location_coords["E"], location_coords["F"]).km),
                           ("G", geodesic(location_coords["E"], location_coords["G"]).km)])  
    rms.add_location("F", [("D", geodesic(location_coords["F"], location_coords["D"]).km),
                           ("E", geodesic(location_coords["F"], location_coords["E"]).km),
                           ("H", geodesic(location_coords["F"], location_coords["H"]).km)])  
    rms.add_location("G", [("E", geodesic(location_coords["G"], location_coords["E"]).km),
                            ("A", geodesic(location_coords["G"], location_coords["A"]).km)]) 
    rms.add_location("H", [("F", geodesic(location_coords["H"], location_coords["F"]).km),
                           ("A", geodesic(location_coords["H"], location_coords["A"]).km)])  

    rms.add_driver("Driver1", "B")
    rms.add_driver("Driver2", "D")
    rms.add_driver("Driver3", "E")

    window = Tk()
    window.title("Ride Matching Service")
    window.geometry("400x400")
    source_label = Label(window, text="Source")
    source_label.pack()
    source_entry = Entry(window)
    source_entry.pack()
    dest_label = Label(window, text="Destination")
    dest_label.pack()
    dest_entry = Entry(window)
    dest_entry.pack()
    submit_button = Button(window, text="Submit",
                           command=lambda: rms.show_map(source_entry.get(), dest_entry.get(), location_coords))
    submit_button.pack()
    window.mainloop()


if __name__ == "__main__":
    main()
