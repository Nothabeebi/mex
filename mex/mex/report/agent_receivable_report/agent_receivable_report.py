import frappe
from frappe.utils import flt, nowdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "invoice_no", "label": "Invoice No", "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
        {"fieldname": "posting_date", "label": "Posting Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "remarks", "label": "Customer Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "customer", "label": "Agent", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"fieldname": "quantity", "label": "Quantity", "fieldtype": "Int", "width": 100},
        {"fieldname": "selling_price", "label": "Selling Price", "fieldtype": "Currency", "width": 120},
        {"fieldname": "invoice_amount", "label": "Invoice Amount", "fieldtype": "Currency", "width": 120},
        {"fieldname": "paid_amount", "label": "Paid Amount", "fieldtype": "Currency", "width": 120},
        {"fieldname": "net_outstanding", "label": "Net Outstanding", "fieldtype": "Currency", "width": 120},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 120},
        {"fieldname": "overdue_days", "label": "Overdue Days", "fieldtype": "Int", "width": 100},
    ]

def get_data(filters):
    data = []
    conditions = ["si.docstatus != 2"]  # Exclude canceled invoices
    query_params = {"today": nowdate()}

    # Add date filters
    if filters.get("from_date"):
        conditions.append("si.posting_date >= %(from_date)s")
        query_params["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions.append("si.posting_date <= %(to_date)s")
        query_params["to_date"] = filters["to_date"]

    # Add agent filter
    if filters.get("agent"):
        conditions.append("si.customer = %(agent)s")
        query_params["agent"] = filters["agent"]

    # Add overdue days filter
    if filters.get("overdue_days"):
        conditions.append("DATEDIFF(CURDATE(), si.due_date) >= %(overdue_days)s")
        query_params["overdue_days"] = filters["overdue_days"]

    condition_string = " AND ".join(conditions)
    if condition_string:
        condition_string = "WHERE " + condition_string

    invoices = frappe.db.sql(f"""
        SELECT
            si.name AS invoice_no,
            si.posting_date,
            si.customer,
            si.grand_total AS invoice_amount,
            IFNULL(SUM(per.allocated_amount), 0) AS paid_amount,
            (si.grand_total - IFNULL(SUM(per.allocated_amount), 0)) AS net_outstanding,
            CASE
                WHEN si.outstanding_amount = 0 THEN "Paid"
                WHEN si.outstanding_amount > 0 AND si.due_date < CURDATE() THEN "Overdue"
                ELSE "Unpaid"
            END AS status,
            CASE
                WHEN si.outstanding_amount > 0 AND si.due_date < CURDATE() THEN DATEDIFF(CURDATE(), si.due_date)
                ELSE 0
            END AS overdue_days,
            si.remarks,  -- Fetching remarks from the Sales Invoice table (if exists)
            sii.qty AS quantity,
            sii.rate AS selling_price  -- Fetching the selling price or rate
        FROM
            `tabSales Invoice` si
        LEFT JOIN
            `tabPayment Entry Reference` per ON per.reference_name = si.name
        LEFT JOIN
            `tabPayment Entry` pe ON pe.name = per.parent AND pe.docstatus = 1
        LEFT JOIN
            `tabSales Invoice Item` sii ON sii.parent = si.name
        {condition_string}
        GROUP BY
            si.name
        ORDER BY
            si.posting_date DESC, si.customer ASC
    """, query_params, as_dict=True)

    for inv in invoices:
        data.append({
            "invoice_no": inv.invoice_no,
            "posting_date": inv.posting_date,
            "remarks": inv.remarks,        
            "customer": inv.customer,
            "quantity": inv.quantity,
            "selling_price": flt(inv.selling_price),      
            "invoice_amount": flt(inv.invoice_amount),
            "paid_amount": flt(inv.paid_amount),
            "net_outstanding": flt(inv.net_outstanding),
            "status": inv.status,
            "overdue_days": inv.overdue_days,
        })

    return data
