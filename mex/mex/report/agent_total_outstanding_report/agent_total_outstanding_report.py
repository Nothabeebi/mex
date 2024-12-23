import frappe  # Add this import

from frappe.utils import flt  # Ensure utility functions are imported if used

def execute(filters=None):
    """
    Entry point for the report. Returns the columns and data.
    """
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    """
    Defines the columns for the report.
    """
    return [
        {"label": "Agent", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": "Total Outstanding", "fieldname": "total_outstanding", "fieldtype": "Currency", "width": 150},
        {"label": "Paid Amount", "fieldname": "paid_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Due Amount", "fieldname": "due_amount", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    """
    Fetches and processes the data for the report based on filters.
    """
    data = []
    conditions = []
    query_params = {}

    # Add agent filter
    if filters.get("agent"):
        conditions.append("si.customer = %(agent)s")
        query_params["agent"] = filters["agent"]

    # Add date filters
    if filters.get("from_date"):
        conditions.append("si.posting_date >= %(from_date)s")
        query_params["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions.append("si.posting_date <= %(to_date)s")
        query_params["to_date"] = filters["to_date"]

    # Ensure we are only fetching submitted invoices
    conditions.append("si.docstatus = 1")  # Only submitted invoices

    # Handle the WHERE clause based on conditions
    condition_string = " AND ".join(conditions)

    # Debugging condition and params
    print("Condition String:", condition_string)
    print("Query Params:", query_params)

    # Build the final SQL query
    query = f"""
        SELECT
            si.customer,
            SUM(si.outstanding_amount) AS total_outstanding,
            IFNULL(SUM(DISTINCT pe.paid_amount), 0) AS paid_amount,
            SUM(si.outstanding_amount) - IFNULL(SUM(DISTINCT pe.paid_amount), 0) AS due_amount
        FROM
            `tabSales Invoice` si
        LEFT JOIN
            `tabPayment Entry` pe ON pe.party_type = 'Customer' AND pe.party = si.customer
        WHERE
            pe.docstatus = 1 AND pe.payment_type = 'Receive'
            {"AND " + condition_string if condition_string else ""}
        GROUP BY
            si.customer
        ORDER BY
            total_outstanding DESC
    """

    print("Final Query:", query)

    customers = frappe.db.sql(query, query_params, as_dict=True, debug=True)

    for customer in customers:
        data.append({
            "customer": customer.customer,
            "total_outstanding": flt(customer.total_outstanding),
            "paid_amount": flt(customer.paid_amount),
            "due_amount": flt(customer.due_amount),
        })

    return data
