# Copyright (c) 2025, Surya and contributors
# For license information, please see license.txt

# Final, Corrected Code for site_visit_log.py with data cleaning
import frappe
from frappe.model.document import Document
from geopy.distance import geodesic
import json
import re # Import the regular expression library

class SiteVisitLog(Document):
    def validate(self):
        assignment = frappe.get_doc("Site Visit Assignment", self.site_visit_assignment)
        captured_location = self.captured_location
        target_location = assignment.target_location

        if not captured_location or not target_location:
            frappe.throw("Both Captured and Target Location are required.")

        # --- This is the updated, more robust helper function ---
        def get_coords_from_location(location_string):
            """
            This function cleans and parses the location string,
            handling both GeoJSON and simple lat,lng formats.
            """
            # Step 1: Clean the string to remove extra commas or spaces
            # This turns "13.0827,, 80.2707" into "13.0827,80.2707"
            location_string = re.sub(r',\s*,', ',', location_string) # Replace ', ,' with ','
            location_string = re.sub(r',,', ',', location_string)     # Replace ',,' with ','

            try:
                if "FeatureCollection" in location_string:
                    data = json.loads(location_string)
                    coords = data["features"][0]["geometry"]["coordinates"]
                    return (coords[1], coords[0]) # Returns (lat, lon)
                else:
                    parts = location_string.split(',')
                    return (float(parts[0]), float(parts[1]))
            except Exception as e:
                 frappe.throw(f"Could not parse cleaned location data: {location_string}. Error: {e}")

        target_coords = get_coords_from_location(target_location)
        captured_coords = get_coords_from_location(captured_location)

        allowed_radius = assignment.geofence_radius or 150
        distance = geodesic(target_coords, captured_coords).meters

        if distance <= allowed_radius:
            self.verification_status = "Pending Verified"
            frappe.db.set_value("Site Visit Assignment", self.site_visit_assignment, "status", "Submitted")
            frappe.msgprint(f"Location Verified. You are {round(distance)} meters from the target.")
        else:
            self.verification_status = "Out of Radius"
            frappe.throw(f"Location Mismatch. You are {round(distance)} meters away (allowed radius: {allowed_radius}m).")
