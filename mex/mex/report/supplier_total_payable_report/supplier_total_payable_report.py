import frappe
from frappe.utils import flt, nowdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "supplier", "label": "Supplier", "fieldtype": "Link", "options": "Supplier", "width": 200},
        {"fieldname": "total_invoice_amount", "label": "Total Invoice Amount", "fieldtype": "Currency", "width": 150},
        {"fieldname": "total_paid", "label": "Total Paid", "fieldtype": "Currency", "width": 150},
        {"fieldname": "amount_due", "label": "Amount Due", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    data = []
    conditions = []
    query_params = {}

    # Add supplier filter
    if filters.get("supplier"):
        conditions.append("pi.supplier = %(supplier)s")
        query_params["supplier"] = filters["supplier"]

    # Add date filters
    if filters.get("from_date"):
        conditions.append("pi.posting_date >= %(from_date)s")
        query_params["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions.append("pi.posting_date <= %(to_date)s")
        query_params["to_date"] = filters["to_date"]

    # Ensure we are only fetching submitted purchase invoices
    conditions.append("pi.docstatus = 1")  # Only submitted invoices

    # Add condition for payment made
    if filters.get("payment_from_date"):
        conditions.append("pe.posting_date >= %(payment_from_date)s")
        query_params["payment_from_date"] = filters["payment_from_date"]
    
    if filters.get("payment_to_date"):
        conditions.append("pe.posting_date <= %(payment_to_date)s")
        query_params["payment_to_date"] = filters["payment_to_date"]

    condition_string = " AND ".join(conditions)
    if condition_string:
        condition_string = "WHERE " + condition_string

    # Fixing the query by linking Purchase Invoice to Payment Entry by Supplier and ensuring no duplicates
    suppliers = frappe.db.sql(f"""
        SELECT
            pi.supplier,
            SUM(pi.grand_total) AS total_invoice_amount,
            IFNULL(SUM(DISTINCT pe.paid_amount), 0) AS total_paid,
            SUM(pi.grand_total) - IFNULL(SUM(DISTINCT pe.paid_amount), 0) AS amount_due
        FROM
            `tabPurchase Invoice` pi
        LEFT JOIN
            `tabPayment Entry` pe ON pe.party = pi.supplier AND pe.party_type = 'Supplier' AND pe.docstatus = 1
        {condition_string}
        GROUP BY
            pi.supplier
        ORDER BY
            total_invoice_amount DESC
    """, query_params, as_dict=True)

    for supplier in suppliers:
        data.append({
            "supplier": supplier.supplier,
            "total_invoice_amount": flt(supplier.total_invoice_amount),
            "total_paid": flt(supplier.total_paid),
            "amount_due": flt(supplier.amount_due),
        })

    return data
