import frappe
import random

@frappe.whitelist()
def send_otp_manual(doctype, docname, phone_number_field):
    """Generates and sends an OTP for a document, storing the OTP on the document itself."""
    doc = frappe.get_doc(doctype, docname)
    phone_number = doc.get(phone_number_field)

    if not phone_number:
        frappe.throw("Please enter a phone number first.")

    # Generate a 6-digit random number
    otp = str(random.randint(100000, 999999))

    # Save this OTP in the hidden 'generated_otp' field of the document
    doc.db_set("generated_otp", otp)
    frappe.db.commit()

    # Send the SMS using the configured Twilio settings
    frappe.sendmail(
        recipients=[phone_number],
        message=f"Your verification code is: {otp}",
        sms=True
    )

    return "OTP has been sent successfully."

@frappe.whitelist()
def verify_otp_manual(doctype, docname, otp_code_field):
    """Verifies the OTP entered by the user against the one stored on the document."""
    doc = frappe.get_doc(doctype, docname)
    otp_code = doc.get(otp_code_field)

    if not otp_code:
        frappe.throw("Please enter the OTP code you received.")

    stored_otp = doc.get("generated_otp")

    if stored_otp == otp_code:
        # If it matches, update the status and save
        doc.db_set("phone_verified", 1)
        return "Phone number verified successfully!"
    else:
        # If it doesn't match, raise an error
        frappe.throw("Invalid OTP. Please try again.")
