import frappe
from frappe import _

def execute(filters=None):
    # Define the columns for the report
    columns = [
    	{
            "label": _("Date"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 120
        },
    	{
            "label": _("Customer Name"),
            "fieldname": "customer_remark",
            "fieldtype": "Small Text",
            "options": "Customer",
            "width": 150
        },
        
        {
            "label": _("Agent"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150
        },
        {
            "label": _("Total Buying Amount"),
            "fieldname": "total_buying_amount",
            "fieldtype": "Currency",
            "width": 150
        },
    	 {
            "label": _("Total Selling Amount"),
            "fieldname": "total_selling_amount",
            "fieldtype": "Currency",
            "width": 150
        },
    	 {
            "label": _("Quantity"),
            "fieldname": "quantity",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": _("Status"),
            "fieldname": "docstatus",
            "fieldtype": "Link",
        	"options": "docstatus",
            "width": 100
        }
        
    ]
    
    # Set default filters if not provided
    if not filters:
        filters = {}

    # Fetch Easy Sales Invoices based on the provided filters
    conditions = " WHERE esi.docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND esi.date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND esi.date <= '{filters['to_date']}'"
    if filters.get("customer"):
        conditions += f" AND esi.customer = '{filters['customer']}'"

    # Fetch data only from the Easy Sales Invoice table
    query = f"""
        SELECT
        	esi.date,
            esi.customer_remark,
            esi.customer,
            esi.supplier,
            esi.total_buying_amount,
            esi.total_selling_amount,
            esi.quantity
           
        FROM
            `tabEasy Sales Invoice` esi
        {conditions}
        ORDER BY esi.date
    """

    data = frappe.db.sql(query, as_dict=True)

    # If a "Group By" filter is provided, group the results
    if filters.get("group_by"):
        group_by = filters["group_by"]
        data = group_data(data, group_by)
    
    return columns, data


def group_data(data, group_by):
    grouped_data = {}
    
    for row in data:
        key = row.get(group_by)
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(row)
    
    # Flatten the grouped data
    result = []
    for group, rows in grouped_data.items():
        for row in rows:
            result.append(row)
    
    return result
