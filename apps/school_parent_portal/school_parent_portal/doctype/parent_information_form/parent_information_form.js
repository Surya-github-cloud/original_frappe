frappe.ui.form.on('Parent Information Form', {
    refresh: function(frm) {
        // Add button to send OTP
        if (!frm.doc.phone_verified && frm.doc.phone_number) {
            frm.add_custom_button(__('Send OTP'), function() {
                frm.call('send_otp')
                    .then(r => {
                        if (r.message) {
                            frappe.msgprint(__('OTP sent successfully'));
                        }
                    });
            }).addClass('btn-primary');
        }
        
        // Add button to generate QR code and link
        frm.add_custom_button(__('Generate Share Options'), function() {
            frappe.prompt([
                {
                    fieldname: 'method',
                    fieldtype: 'Select',
                    label: 'Select Sharing Method',
                    options: 'QR Code\nLink\nManual Entry',
                    reqd: 1
                }
            ], function(values) {
                if (values.method === 'QR Code') {
                    frm.call('generate_qr_code')
                        .then(r => {
                            if (r.message) {
                                // Show QR code in dialog
                                var dialog = new frappe.ui.Dialog({
                                    title: __('QR Code'),
                                    size: 'small'
                                });
                                
                                dialog.$body.append(`<div style="text-align:center"><img src="${r.message}" style="width:200px;height:200px"></div>`);
                                dialog.show();
                            }
                        });
                } else if (values.method === 'Link') {
                    frm.call('get_form_link')
                        .then(r => {
                            if (r.message) {
                                frappe.msgprint(__('Form Link: ') + r.message);
                            }
                        });
                }
                // Manual entry doesn't require special handling
            }, __('Select Sharing Method'), __('Proceed'));
        });
    },
    
    phone_number: function(frm) {
        // Reset verification if phone number changes
        if (frm.doc.phone_verified) {
            frm.set_value('phone_verified', 0);
        }
    },
    
    validate: function(frm) {
        // Ensure phone is verified before submission
        if (frm.doc.__islocal && !frm.doc.phone_verified) {
            frappe.throw(__('Please verify your phone number before submitting'));
        }
    }
});
