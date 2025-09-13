import frappe

@frappe.whitelist()
def create_crm_project(project_name, customer=None):
    """
    API endpoint to create a new project.
    """
    try:
        # Create the new project document in memory
        project = frappe.get_doc({
            "doctype": "Project",
            "project_name": project_name,
            "customer": customer,
            "status": "Open" # Set a default status
        })
        
        # Insert it into the database
        project.insert()
        frappe.db.commit() # Save changes
        
        # Return the new project's data as a confirmation
        return project.as_dict()
        
    except Exception as e:
        # If something goes wrong, log the error and notify the caller
        frappe.log_error(frappe.get_traceback(), "CRM Project Creation Failed")
        frappe.throw(f"Could not create project: {e}")
