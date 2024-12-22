import frappe
from frappe.utils import flt, nowdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "customer", "label": "Agent", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"fieldname": "total_outstanding", "label": "Total Invoice Amount", "fieldtype": "Currency", "width": 150},
        {"fieldname": "paid_amount", "label": "Total Paid", "fieldtype": "Currency", "width": 150},
        {"fieldname": "due_amount", "label": "Amount Due", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    data = []
    conditions = []
    query_params = {}

    # Add customer filter
    if filters.get("customer"):
        conditions.append("si.customer = %(customer)s")
        query_params["customer"] = filters["customer"]

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

    # Now build the final SQL query string
    customers = frappe.db.sql(f"""
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
    """, query_params, as_dict=True)

    for customer in customers:
        data.append({
            "customer": customer.customer,
            "total_outstanding": flt(customer.total_outstanding),
            "paid_amount": flt(customer.paid_amount),
            "due_amount": flt(customer.due_amount),
        })

    return data
