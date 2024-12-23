// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Party Ledger Report"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
            reqd: 1,
        },
        {
            fieldname: "party_type",
            label: __("Party Type"),
            fieldtype: "Autocomplete",
            options: ["Customer", "Supplier"],
            reqd: 1,
            on_change: function () {
                frappe.query_report.set_filter_value("party", "");
            },
        },
        {
            fieldname: "party",
            label: __("Party"),
            fieldtype: "MultiSelectList",
            get_data: function (txt) {
                if (!frappe.query_report.filters) return;

                let party_type = frappe.query_report.get_filter_value("party_type");
                if (!party_type) return;

                return frappe.db.get_link_options(party_type, txt);
            },
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            reqd: 1,
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1,
        },
        {
            fieldname: "group_by",
            label: __("Group by"),
            fieldtype: "Select",
            options: [
                "",
                {
                    label: __("Group by Voucher"),
                    value: "Group by Voucher",
                },
                {
                    label: __("Group by Account"),
                    value: "Group by Account",
                },
            ],
            default: "Group by Voucher",
        },
        {
            fieldname: "show_opening_entries",
            label: __("Show Opening Entries"),
            fieldtype: "Check",
        },
        {
            fieldname: "show_cancelled_entries",
            label: __("Show Cancelled Entries"),
            fieldtype: "Check",
        },
        
        {
            fieldname: "show_remarks",
            label: __("Show Remarks"),
            fieldtype: "Check",
        },
        
    ],
};

erpnext.utils.add_dimensions("Party Ledger", 10);

//# sourceURL=party_ledger.js
