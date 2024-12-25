import frappe
from frappe.utils import flt

def execute(filters=None):
    """
    This is the entry point for the script report. It processes the data and returns the columns and data.
    """
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    """
    Defines the columns for the report.
    """
    return [
        {"fieldname": "customer", "label": "Customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"fieldname": "total_outstanding", "label": "Total Outstanding", "fieldtype": "Currency", "width": 150},
        {"fieldname": "paid_amount", "label": "Paid Amount", "fieldtype": "Currency", "width": 150},
        {"fieldname": "due_amount", "label": "Due Amount", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    """
    Fetches the data for the report based on the provided filters.
    """
    conditions = []
    query_params = {}

    # Add filters
    if filters.get("from_date"):
        conditions.append("si.posting_date >= %(from_date)s")
        query_params["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions.append("si.posting_date <= %(to_date)s")
        query_params["to_date"] = filters["to_date"]

    conditions.append("si.docstatus = 1")  # Include only submitted invoices

    condition_string = " AND ".join(conditions)

    query = f"""
        SELECT
            si.customer AS customer,
            SUM(si.outstanding_amount) AS total_outstanding,
            SUM(pe.paid_amount) AS paid_amount,
            SUM(si.outstanding_amount) - IFNULL(SUM(pe.paid_amount), 0) AS due_amount
        FROM
            `tabSales Invoice` si
        LEFT JOIN
            `tabPayment Entry` pe ON pe.party_type = 'Customer' AND pe.party = si.customer
        WHERE
            {condition_string}
        GROUP BY
            si.customer
        ORDER BY
            total_outstanding DESC
    """

    results = frappe.db.sql(query, query_params, as_dict=True)

    # Format the results
    return [
        {
            "customer": row.customer,
            "total_outstanding": flt(row.total_outstanding),
            "paid_amount": flt(row.paid_amount),
            "due_amount": flt(row.due_amount),
        }
        for row in results
    ]
