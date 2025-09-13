import frappe

def create_lead_from_inquiry(doc, method):
    """
    This function is called when an Admission Inquiry is submitted.
    It creates a new Lead document.
    """
    # Check if a lead with this phone number already exists to avoid duplicates
    if frappe.db.exists("Lead", {"mobile_no": doc.phone_number}):
        frappe.log_error(title="Lead Creation Skipped", message=f"Lead for {doc.phone_number} already exists.")
        return

    try:
        # Create and save the new Lead
        new_lead = frappe.new_doc("Lead")
        new_lead.lead_name = doc.parent_name
        new_lead.mobile_no = doc.phone_number
        new_lead.email_id = doc.email_address
        
        # You can add custom fields here as well
        # For example, if you have a "Student Name" field in Lead:
        # new_lead.custom_student_name = doc.student_name
        # new_lead.custom_grade_of_interest = doc.grade
        
        new_lead.insert(ignore_permissions=True)
        
        # Add a comment to the inquiry to link it to the new lead
        doc.add_comment("Comment", f"Lead {new_lead.name} created from this inquiry.")

    except Exception as e:
        frappe.log_error(title="Failed to create Lead from Inquiry", message=str(e))
