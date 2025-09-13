import frappe
from frappe.utils import get_datetime, time_diff_in_seconds

def execute(filters=None):
    columns = get_columns()
    data = []

    # Get all employees with currently "Open" assignments
    open_assignments = frappe.get_all("Site Visit Assignment",
        filters={"status": "Open"},
        fields=["name", "assigned_to", "target_location", "geofence_radius"])

    for assignment in open_assignments:
        employee = assignment.assigned_to
        if not employee:
            continue

        # Get the latest location log for this employee
        latest_log = frappe.get_all("Employee Location Log",
            filters={"employee": employee},
            fields=["location", "timestamp"],
            order_by="timestamp desc",
            limit=1
        )

        if not latest_log:
            row = {
                "employee": employee,
                "assignment": assignment.name,
                "last_seen": "No location logged yet",
                "status": "Unknown",
                "location_link": "N/A"
            }
            data.append(row)
            continue
        
        last_location = latest_log[0].location
        last_timestamp = latest_log[0].timestamp

        time_since_ping = time_diff_in_seconds(frappe.utils.now_datetime(), last_timestamp)
        status = "Online" if time_since_ping < 300 else "Offline" # Online if pinged in last 5 mins
        
        map_link = f"https://maps.google.com/maps?q={last_location}"
        
        row = {
            "employee": employee,
            "assignment": assignment.name,
            "last_seen": last_timestamp,
            "status": status,
            "location_link": map_link
        }
        data.append(row)

    return columns, data

def get_columns():
    return [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "User", "width": 200},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Last Seen", "fieldname": "last_seen", "fieldtype": "Datetime", "width": 200},
        {"label": "Active Assignment", "fieldname": "assignment", "fieldtype": "Link", "options": "Site Visit Assignment", "width": 200},
        {"label": "View on Map", "fieldname": "location_link", "fieldtype": "Data", "width": 150}
    ]
