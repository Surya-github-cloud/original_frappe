import frappe
import random
from frappe.utils import now

# This decorator makes the function accessible from the client-side script
@frappe.whitelist(allow_guest=True)
def send_admission_otp(phone_number, doc_name):
    """
    Generates a 6-digit OTP, stores it in the cache, and sends it via SMS
    using Frappe's standard SMS functionality.
    """
    if not phone_number or not doc_name:
        frappe.throw("Phone Number and Document ID are required.")

    # Generate a 6-digit OTP
    otp = str(random.randint(100000, 999999))

    # Store the OTP in Frappe's cache for 5 minutes.
    cache_key = f"admission_otp_{doc_name}"
    frappe.cache().set(cache_key, otp, expires_in_sec=300)

    # --- Use Frappe's built-in SMS function ---
    # This will automatically use the credentials from Twilio Settings.
    try:
        message = f"Your OTP for school admission is {otp}. It is valid for 5 minutes."
        
        # The recipient's phone number must be in E.164 format (e.g., +919876543210)
        # We will assume the number is from India (+91) if it doesn't have a country code.
        recipient_phone_number = phone_number
        if not recipient_phone_number.startswith('+'):
            recipient_phone_number = f"+91{phone_number}"

        frappe.sendmail(
            recipients=[recipient_phone_number],
            message=message,
            send_sms=True
        )
        
        frappe.logger().info(f"SMS dispatch requested for {recipient_phone_number}.")

    except Exception as e:
        frappe.log_error(title="Frappe SMS Error", message=str(e))

    return {"status": "success", "message": "OTP has been sent to your mobile number."}


@frappe.whitelist(allow_guest=True)
def verify_admission_otp(otp_code, doc_name):
    """
    Verifies the submitted OTP against the one stored in the cache.
    """
    if not otp_code or not doc_name:
        frappe.throw("OTP and Document ID are required.")

    cache_key = f"admission_otp_{doc_name}"
    stored_otp = frappe.cache().get(cache_key)

    if not stored_otp:
        return {"status": "error", "message": "OTP has expired. Please request a new one."}

    if str(stored_otp) == str(otp_code):
        # OTP is correct. Update the document to mark it as verified.
        try:
            doc = frappe.get_doc("Admission Inquiry", doc_name)
            doc.is_verified = 1
            doc.save(ignore_permissions=True) # ignore_permissions is needed for guest
            frappe.cache().delete_key(cache_key) # Clean up the cache
            return {"status": "success", "message": "Phone number verified successfully."}
        except Exception as e:
            frappe.log_error(title="OTP Verification Error", message=str(e))
            return {"status": "error", "message": "Could not update verification status."}
    else:
        # OTP is incorrect
        return {"status": "error", "message": "Invalid OTP. Please try again."}

