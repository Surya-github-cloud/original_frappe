import frappe
from frappe.model.document import Document
import qrcode
import io
import base64
from twilio.rest import Client

class ParentInformationForm(Document):
    def validate(self):
        # Create lead when form is submitted
        if self.docstatus == 1 and not self.lead_reference:
            self.create_lead()
    
    def create_lead(self):
        # Create a new Lead in ERPNext
        lead = frappe.get_doc({
            "doctype": "Lead",
            "lead_name": self.parent_name,
            "email_id": self.email,
            "phone": self.phone_number,
            "notes": f"Student: {self.student_name}, Grade: {self.grade}"
        })
        lead.insert(ignore_permissions=True)
        
        # Update reference to lead
        self.lead_reference = lead.name
        self.db_update()
    
    def send_otp(self):
        # Generate random 6-digit OTP
        import random
        otp = str(random.randint(100000, 999999))
        
        # Store OTP in document (hidden field)
        self.verification_code = otp
        self.save()
        
        # Send OTP via Twilio
        try:
            # Get Twilio credentials from Site Config
            account_sid = frappe.conf.get('twilio_account_sid')
            auth_token = frappe.conf.get('twilio_auth_token')
            from_number = frappe.conf.get('twilio_phone_number')
            
            if not all([account_sid, auth_token, from_number]):
                frappe.throw("Twilio credentials not configured. Please contact administrator.")
            
            # Initialize Twilio client
            client = Client(account_sid, auth_token)
            
            # Send message
            message = client.messages.create(
                body=f"Your verification code is: {otp}",
                from_=from_number,
                to=self.phone_number
            )
            
            return True
        except Exception as e:
            frappe.throw(f"Failed to send OTP: {str(e)}")
    
    def generate_qr_code(self):
        # Generate URL for this form
        site_url = frappe.utils.get_url()
        form_url = f"{site_url}/parent-info-form?name={self.name}"
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(form_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        
        # Convert to base64 for embedding in HTML
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def get_form_link(self):
        site_url = frappe.utils.get_url()
        return f"{site_url}/parent-info-form?name={self.name}"
    
    def verify_otp(self, otp):
        if self.verification_code == otp:
            self.phone_verified = 1
            self.save()
            return True
        return False

# API endpoint for OTP verification
@frappe.whitelist(allow_guest=True)
def verify_otp(docname, otp):
    doc = frappe.get_doc("Parent Information Form", docname)
    return doc.verify_otp(otp)

# API endpoint for form submission
@frappe.whitelist(allow_guest=True)
def submit_parent_form(data):
    # Create new Parent Information Form
    doc = frappe.get_doc({
        "doctype": "Parent Information Form",
        "student_name": data.get("student_name"),
        "parent_name": data.get("parent_name"),
        "grade": data.get("grade"),
        "phone_number": data.get("phone_number"),
        "email": data.get("email")
    })
    
    doc.insert(ignore_permissions=True)
    
    # Send OTP
    doc.send_otp()
    
    return doc.name
