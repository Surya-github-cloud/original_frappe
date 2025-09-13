frappe.query_reports["Employee Live Status"] = {
    "filters": [],
    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        
        if (column.fieldname === "status" && data.status === "Online") {
            value = `<span style="color: green;">● ${data.status}</span>`;
        } else if (column.fieldname === "status" && data.status === "Offline") {
            value = `<span style="color: red;">● ${data.status}</span>`;
        }

        if (column.fieldname === "location_link" && data.location_link !== "N/A") {
            return `<a href="${data.location_link}" target="_blank">View on Google Maps</a>`;
        }
        
        return value;
    }
};
