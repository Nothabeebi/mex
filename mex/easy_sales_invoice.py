import frappe

def on_submit_easy_sales_invoice(doc, method):
    # Create Sales Invoice
    sales_invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": doc.customer,
        "posting_date": doc.date,
        "items": [
            {
                "item_code": doc.item or "mex item",
                "qty": doc.quantity,
                "rate": doc.selling_rate            }
        ],
        "total": doc.total_selling_amount,
        "remarks": doc.customer_remark

    })
    sales_invoice.insert(ignore_permissions=True)
    sales_invoice.submit()

    # Link Sales Invoice to Easy Sales Invoice
    doc.db_set("sales_invoice", sales_invoice.name)

    # Create Purchase Invoice
    purchase_invoice = frappe.get_doc({
        "doctype": "Purchase Invoice",
        "supplier": doc.supplier,
        "posting_date": doc.date,
        "items": [
            {
                "item_code": doc.item or "mex item",
                "qty": doc.quantity,
                "rate": doc.purchase_rate
            }
        ],
        "total": doc.total_buying_amount,
        "remarks": doc.customer_remark
    
    })
    purchase_invoice.insert(ignore_permissions=True)
    purchase_invoice.submit()

    # Link Purchase Invoice to Easy Sales Invoice
    doc.db_set("purchase_invoice", purchase_invoice.name)

def on_cancel_easy_sales_invoice(doc, method):
    # Cancel the linked Sales Invoice
    if doc.sales_invoice:
        sales_invoice = frappe.get_doc("Sales Invoice", doc.sales_invoice)
        if sales_invoice.docstatus == 1:  # Ensure it's submitted before canceling
            sales_invoice.cancel()

    # Cancel the linked Purchase Invoice
    if doc.purchase_invoice:
        purchase_invoice = frappe.get_doc("Purchase Invoice", doc.purchase_invoice)
        if purchase_invoice.docstatus == 1:  # Ensure it's submitted before canceling
            purchase_invoice.cancel()
