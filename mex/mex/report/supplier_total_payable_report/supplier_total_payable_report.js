frappe.query_reports["Supplier Total Payable Report"] = {
    "filters": [
        {
            "fieldname": "supplier",
            "label": __("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier",
            "default": null,  // Set to null or leave blank for no default
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_start(),
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_end(),
        }
    ],
    onload: function(report) {
        // Add custom functionality on report load if necessary
    }
};
