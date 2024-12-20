frappe.query_reports["Easy Sales Invoice Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
		},
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": ["", "Draft", "Submitted"]
		},
		{
			"fieldname": "is_return",
			"label": __("Is Return"),
			"fieldtype": "Check",
			"default": 0
		},
		{
			"label": __("Group By"),
			"fieldname": "group_by",
			"fieldtype": "Select",
			"options": ["", "Customer", "Supplier"]
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.bold) {
			value = value.bold();
		}
		return value;
	},
};
