frappe.ready(function() {
    // Only run on parent info form
    if (window.location.pathname !== '/parent-info-form') return;
    
    // Add OTP verification section
    $('.page-content').append(`
        <div class="otp-section" style="margin-top: 20px; display: none;">
            <div class="form-group">
                <label for="otp">Verification Code</label>
                <input type="text" id="otp" class="form-control" placeholder="Enter OTP sent to your phone">
            </div>
            <button class="btn btn-default btn-send-otp">Send OTP</button>
            <button class="btn btn-primary btn-verify-otp">Verify OTP</button>
        </div>
    `);
    
    // Handle OTP sending
    $('.btn-send-otp').on('click', function() {
        const phone = $('input[data-fieldname="phone_number"]').val();
        if (!phone) {
            frappe.msgprint('Please enter a phone number first');
            return;
        }
        
        // Collect all form data
        const formData = {
            student_name: $('input[data-fieldname="student_name"]').val(),
            parent_name: $('input[data-fieldname="parent_name"]').val(),
            grade: $('input[data-fieldname="grade"]').val(),
            phone_number: phone,
            email: $('input[data-fieldname="email"]').val()
        };
        
        frappe.call({
            method: 'school_parent_portal.school_parent_portal.doctype.parent_information_form.parent_information_form.submit_parent_form',
            args: {
                data: formData
            },
            callback: function(r) {
                if (r.message) {
                    window.docname = r.message;
                    $('.otp-section').show();
                    frappe.msgprint('OTP sent to your phone number');
                }
            }
        });
    });
    
    // Handle OTP verification
    $('.btn-verify-otp').on('click', function() {
        const otp = $('#otp').val();
        if (!otp) {
            frappe.msgprint('Please enter the OTP');
            return;
        }
        
        frappe.call({
            method: 'school_parent_portal.school_parent_portal.doctype.parent_information_form.parent_information_form.verify_otp',
            args: {
                docname: window.docname,
                otp: otp
            },
            callback: function(r) {
                if (r.message) {
                    frappe.msgprint('Phone number verified successfully!');
                    // Submit the form
                    $('.btn-form-submit').click();
                } else {
                    frappe.msgprint('Invalid OTP. Please try again.');
                }
            }
        });
    });
    
    // Override form submission to require OTP verification first
    $('.btn-form-submit').on('click', function(e) {
        if (!window.docname) {
            e.preventDefault();
            frappe.msgprint('Please send and verify OTP first');
            return false;
        }
    });
});
