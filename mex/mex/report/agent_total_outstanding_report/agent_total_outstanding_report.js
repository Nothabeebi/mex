frappe.query_reports["Agent Total Outstanding Report"] = {
    "filters": [
        {
            "fieldname": "customer",
            "label": __("Agent"),
            "fieldtype": "Link",
            "options": "Customer",
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
