import frappe
from frappe.utils import add_days, today

def on_submit_easy_sales_invoice(doc, method):
    # Default due date logic: 30 days from today or document date
    due_date = add_days(doc.date or today(), 30)

    # Create Sales Invoice
    sales_invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": doc.customer,
        "posting_date": doc.date,
        "due_date": due_date,
        "items": [
            {
                "item_code": doc.item or "mex item",
                "qty": doc.quantity,
                "rate": doc.selling_rate
            }
        ],
        "total": doc.total_selling_amount
    })
    sales_invoice.insert(ignore_permissions=True)
    sales_invoice.submit()

    # Create Purchase Invoice
    purchase_invoice = frappe.get_doc({
        "doctype": "Purchase Invoice",
        "supplier": doc.supplier,
        "posting_date": doc.date,
        "due_date": due_date,
        "items": [
            {
                "item_code": doc.item or "mex item",
                "qty": doc.quantity,
                "rate": doc.purchase_rate
            }
        ],
        "total": doc.total_buying_amount
    })
    purchase_invoice.insert(ignore_permissions=True)
    purchase_invoice.submit()


