frappe.query_reports["Agent Receivable Report"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.now_date(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.now_date(),
            "reqd": 1
        },
        {
            "fieldname": "agent",
            "label": __("Agent"),
            "fieldtype": "Link",
            "options": "Customer",
            "reqd": 0
        },
        {
            "fieldname": "overdue_days",
            "label": __("Overdue Days"),
            "fieldtype": "Int",
            "reqd": 0,
            "description": __("Filter invoices overdue by the specified number of days.")
        }
    ]
};