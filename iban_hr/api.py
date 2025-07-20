import frappe

from frappe import _
from frappe.utils import flt, date_diff
from dateutil.relativedelta import relativedelta
import datetime


# @frappe.whitelist()
# def calculate_employee_end_service_salary(joining_date, relieving_date, basic_salary):
#     """
#     Calculate the end service salary for an employee based on their joining and relieving dates.
#     Also returns the difference in years, months, and days.
#     """
#     if not joining_date or not relieving_date:
#         frappe.throw(_("Joining date and Relieving date are required."))

#     if relieving_date < joining_date:
#         frappe.throw(_("Relieving date cannot be earlier than Joining date."))

#     # Convert string dates to datetime.date objects if necessary
#     if isinstance(joining_date, str):
#         joining_date = datetime.datetime.strptime(joining_date, "%Y-%m-%d").date()
#     if isinstance(relieving_date, str):
#         relieving_date = datetime.datetime.strptime(relieving_date, "%Y-%m-%d").date()

#     diff = relativedelta(relieving_date, joining_date)
#     years = diff.years
#     months = diff.months
#     days = diff.days
#     total_years = years + months / 12 + days / 365.25

#     end_servcie_settings = frappe.get_single(
#         "End of Service Gratuity Entitlement Settings"
#     ).end_of_service
#     if not end_servcie_settings:
#         frappe.throw(_("End of Service Gratuity Entitlement Settings not found."))
#     # Calculate the end service salary based on the provided settings

#     # Example return: you can adjust as needed
#     # return {
#     #     "years": years,
#     #     "months": months,
#     #     "days": days,
#     #     "total_years": years + months / 12 + days / 365.25,
#     # }

#     return end_servcie_settings

#########################################333


@frappe.whitelist()
def calculate_employee_end_service_salary(
    joining_date, relieving_date, basic_salary, employee_name
):

    if not joining_date or not relieving_date:
        frappe.throw(_("Joining date and Relieving date are required."))

    if relieving_date < joining_date:
        frappe.throw(_("Relieving date cannot be earlier than Joining date."))

    if isinstance(joining_date, str):
        joining_date = datetime.datetime.strptime(joining_date, "%Y-%m-%d").date()
    if isinstance(relieving_date, str):
        relieving_date = datetime.datetime.strptime(relieving_date, "%Y-%m-%d").date()

    diff = relativedelta(relieving_date, joining_date)
    years = diff.years
    months = diff.months
    days = diff.days
    total_years = years + months / 12 + days / 365.25
    basic_salary = float(basic_salary)

    # Fetch settings from the End of Service Gratuity Entitlement Settings
    settings = frappe.get_single("End of Service Gratuity Entitlement Settings")
    slabs = settings.end_of_service or []

    if not slabs:
        frappe.throw(_("End of Service slabs not found in settings."))

    # Sort slabs by from_year
    sorted_slabs = sorted(slabs, key=lambda x: x.from_year)

    eos_total = 0
    remaining_years = total_years

    for slab in sorted_slabs:
        slab_years = 0
        if remaining_years <= 0:
            break

        slab_from = slab.from_year
        slab_to = slab.to_year
        eos_rate = slab.eos_award  # this is per year (e.g., 0.5, 1.0, etc.)

        # Calculate overlap between employee years and slab
        slab_range = slab_to - slab_from
        slab_applicable_years = min(remaining_years, slab_range)

        if total_years > slab_from:
            eos_total += slab_applicable_years * eos_rate * basic_salary
            remaining_years -= slab_applicable_years

    if frappe.db.exists("Salary Component", f"End of Service - {employee_name}"):
        frappe.throw(
            _("Salary Component 'End of Service - {0}' already exists.").format(
                employee_name
            )
        )

    salary_component = frappe.new_doc("Salary Component")
    salary_component.salary_component = f"End of Service - {employee_name}"
    salary_component.amount = eos_total
    salary_component.salary_component_abbr = "EOS"
    salary_component.insert()
    salary_component.save()
    frappe.db.commit()

    return {
        "years": years,
        "months": months,
        "days": days,
        "total_years": round(total_years, 2),
        "award_amount": round(eos_total, 2),
        # "salary_component": (
        #     salary_component.name if "salary_component" in locals() else None
        # ),
    }
