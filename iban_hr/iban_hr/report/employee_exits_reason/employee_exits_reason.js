// Copyright (c) 2025, Mohamed AbdElsabour and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Exits Reason"] = {
  filters: [
    {
      fieldname: "from_date",
      label: __("From Date"),
      fieldtype: "Date",
      default: frappe.datetime.add_months(frappe.datetime.nowdate(), -12),
    },
    {
      fieldname: "to_date",
      label: __("To Date"),
      fieldtype: "Date",
      default: frappe.datetime.nowdate(),
    },
    {
      fieldname: "joining_from_date",
      label: __("Join From Date"),
      fieldtype: "Date",
      default: frappe.datetime.add_months(frappe.datetime.nowdate(), -12),
    },
    {
      fieldname: "joining_to_date",
      label: __("join To Date"),
      fieldtype: "Date",
      default: frappe.datetime.nowdate(),
    },

    {
      fieldname: "custom_reason_of_eos",
      label: __("Reason for Exit"),
      fieldtype: "Select",
      options: ["", "Normal", "Resignation"],
    },
    {
      fieldname: "company",
      label: __("Company"),
      fieldtype: "Link",
      options: "Company",
    },
    {
      fieldname: "department",
      label: __("Department"),
      fieldtype: "Link",
      options: "Department",
    },
    {
      fieldname: "designation",
      label: __("Designation"),
      fieldtype: "Link",
      options: "Designation",
    },
    {
      fieldname: "employee",
      label: __("Employee"),
      fieldtype: "Link",
      options: "Employee",
    },
    {
      fieldname: "reports_to",
      label: __("Reports To"),
      fieldtype: "Link",
      options: "Employee",
    },
    {
      fieldname: "interview_status",
      label: __("Interview Status"),
      fieldtype: "Select",
      options: ["", "Pending", "Scheduled", "Completed"],
    },
    {
      fieldname: "final_decision",
      label: __("Final Decision"),
      fieldtype: "Select",
      options: ["", "Employee Retained", "Exit Confirmed"],
    },
    {
      fieldname: "exit_interview_pending",
      label: __("Exit Interview Pending"),
      fieldtype: "Check",
    },
    {
      fieldname: "questionnaire_pending",
      label: __("Exit Questionnaire Pending"),
      fieldtype: "Check",
    },
    {
      fieldname: "fnf_pending",
      label: __("FnF Pending"),
      fieldtype: "Check",
    },
  ],
};
