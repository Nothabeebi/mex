# party_ledger_report.py

import frappe
from frappe import _
from frappe.utils import flt, getdate
from erpnext.accounts.report.general_ledger.general_ledger import GeneralLedger

def execute(filters=None):
    # Default filters if none are provided
    filters = filters or {}

    # Fetch party details from filters
    party_type = filters.get('party_type')  # Customer, Supplier, etc.
    party = filters.get('party')  # Party name

    # Fetch the necessary data for the report
    gl_entries = get_party_ledger_data(party_type, party, filters)

    # Format and return the data
    return get_columns(), gl_entries

def get_columns():
    """Define the columns for the Party Ledger report."""
    return [
        _("Date") + ":Date:100",
        _("Voucher Type") + ":Data:150",
        _("Voucher No") + ":Data:150",
        _("Party Name") + ":Data:200",
        _("Account") + ":Data:150",
        _("Debit") + ":Currency:120",
        _("Credit") + ":Currency:120",
        _("Balance") + ":Currency:120",
    ]

def get_party_ledger_data(party_type, party, filters):
    """Fetch the GL entries based on the given party and filters."""
    conditions = [
        "gle.party_type = %s", 
        "gle.party = %s",
        "gle.docstatus = 1"
    ]
    
    # Add filter conditions based on date range and other filters
    if filters.get("from_date"):
        conditions.append("gle.posting_date >= %s")
    if filters.get("to_date"):
        conditions.append("gle.posting_date <= %s")
    
    # Prepare the SQL query
    query = f"""
        SELECT
            gle.posting_date AS date,
            gle.voucher_type,
            gle.voucher_no,
            gle.party,
            gle.account,
            SUM(CASE WHEN gle.debit > 0 THEN gle.debit ELSE 0 END) AS debit,
            SUM(CASE WHEN gle.credit > 0 THEN gle.credit ELSE 0 END) AS credit,
            SUM(CASE WHEN gle.debit > 0 THEN gle.debit ELSE 0 END) - 
            SUM(CASE WHEN gle.credit > 0 THEN gle.credit ELSE 0 END) AS balance
        FROM
            `tabGL Entry` gle
        WHERE
            {conditions}
        GROUP BY
            gle.posting_date, gle.voucher_type, gle.voucher_no, gle.party, gle.account
        ORDER BY
            gle.posting_date ASC
    """

    # Execute the query with the provided filter values
    result = frappe.db.sql(query, tuple([
        party_type,
        party,
        filters.get('from_date'),
        filters.get('to_date')
    ]), as_dict=True)

    # Return the fetched data for report
    return result
