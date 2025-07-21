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
# work version

# @frappe.whitelist()
# def calculate_employee_end_service_salary(
#     joining_date, relieving_date, basic_salary, employee_name, reason_of_eos
# ):

#     if not joining_date or not relieving_date:
#         frappe.throw(_("Joining date and Relieving date are required."))

#     if relieving_date < joining_date:
#         frappe.throw(_("Relieving date cannot be earlier than Joining date."))
#     if not reason_of_eos:
#         frappe.throw(_("Reason of End of Service is required."))

#     if isinstance(joining_date, str):
#         joining_date = datetime.datetime.strptime(joining_date, "%Y-%m-%d").date()
#     if isinstance(relieving_date, str):
#         relieving_date = datetime.datetime.strptime(relieving_date, "%Y-%m-%d").date()

#     diff = relativedelta(relieving_date, joining_date)
#     years = diff.years
#     months = diff.months
#     days = diff.days
#     # total_years = years + months / 12 + days / 365.25
#     total_years = years + months / 12 + days / 360

#     basic_salary = float(basic_salary)

#     # Fetch settings from the End of Service Gratuity Entitlement Settings
#     normal_eos_settings = frappe.get_single(
#         "End of Service Gratuity Entitlement Settings"
#     )
#     slabs = normal_eos_settings.end_of_service or []
#     resignation_eos_settings = frappe.get_single(
#         "End of Service Gratuity Entitlement Settings"
#     )
#     resignation_slabs = resignation_eos_settings.end_of_service_resignation or []

#     if not slabs and not resignation_slabs:
#         frappe.throw(_("End of Service slabs not found in settings."))
#     ## NORMAL EOS SLABS
#     if reason_of_eos == "Normal":
#         if not slabs:
#             frappe.throw(_("End of Service slabs not found in settings."))
#         # Use the normal EOS slabs for calculation

#         # Sort slabs by from_year
#         sorted_slabs = sorted(slabs, key=lambda x: x.from_year)

#         eos_total = 0
#         remaining_years = total_years

#         for slab in sorted_slabs:
#             slab_years = 0
#             if remaining_years <= 0:
#                 break

#             slab_from = slab.from_year
#             slab_to = slab.to_year
#             eos_rate = slab.eos_award  # this is per year (e.g., 0.5, 1.0, etc.)

#             # Calculate overlap between employee years and slab
#             slab_range = slab_to - slab_from
#             slab_applicable_years = min(remaining_years, slab_range)

#             if total_years > slab_from:
#                 eos_total += slab_applicable_years * eos_rate * basic_salary
#                 remaining_years -= slab_applicable_years
#     elif reason_of_eos == "Resignation":
#         if not resignation_slabs:
#             frappe.throw(
#                 _("End of Service slabs for resignation not found in settings.")
#             )
#         # Use the resignation EOS slabs for calculation

#         # Sort slabs by from_year
#         sorted_slabs = sorted(resignation_slabs, key=lambda x: x.from_year)

#         eos_total = 0
#         remaining_years = total_years

#         for slab in sorted_slabs:
#             slab_years = 0
#             if remaining_years <= 0:
#                 break

#             slab_from = slab.from_year
#             slab_to = slab.to_year
#             eos_rate = slab.eos_award
#             # Calculate overlap between employee years and slab
#             slab_range = slab_to - slab_from
#             slab_applicable_years = min(remaining_years, slab_range)
#             if total_years > slab_from:
#                 eos_total += slab_applicable_years * eos_rate * basic_salary
#                 remaining_years -= slab_applicable_years

#     return {
#         "years": years,
#         "months": months,
#         "days": days,
#         "total_years": round(total_years, 2),
#         "award_amount": round(eos_total, 2),
#         # "salary_component": (
#         #     salary_component.name if "salary_component" in locals() else None
#         # ),
#     }


###############################################3333


@frappe.whitelist()
def calculate_employee_end_service_salary(
    joining_date, relieving_date, basic_salary, employee_name, reason_of_eos
):
    if relieving_date < joining_date:
        frappe.throw(_("Relieving date cannot be earlier than Joining date."))

    if not reason_of_eos:
        frappe.throw(_("Reason of End of Service is required."))

    # Convert date strings to datetime.date objects
    if isinstance(joining_date, str):
        joining_date = datetime.datetime.strptime(joining_date, "%Y-%m-%d").date()
    if isinstance(relieving_date, str):
        relieving_date = datetime.datetime.strptime(relieving_date, "%Y-%m-%d").date()

    # Calculate difference
    diff = relativedelta(relieving_date, joining_date)
    years = diff.years
    months = diff.months
    days = diff.days

    # Total years as float, using 12 months and 30 days calendar
    total_years = years + (months / 12) + (days / 360)

    basic_salary = float(basic_salary)

    # Fetch settings from the End of Service Gratuity Entitlement Settings
    settings = frappe.get_single("End of Service Gratuity Entitlement Settings")

    if reason_of_eos == "Normal":
        slabs = settings.end_of_service or []
    elif reason_of_eos == "Resignation":
        slabs = settings.end_of_service_resignation or []
    else:
        frappe.throw(_("Invalid reason of end of service."))

    if not slabs:
        frappe.throw(_("No EOS entitlement slabs found for this reason."))

    # Sort slabs by from_year
    sorted_slabs = sorted(slabs, key=lambda x: x.from_year)

    eos_total = 0.0

    for slab in sorted_slabs:
        start = slab.from_year
        end = slab.to_year
        rate = slab.eos_award

        # Check for overlap
        if total_years > start:
            # Get overlapping period within this slab
            effective_years = min(total_years, end) - start
            if effective_years > 0:
                eos_total += effective_years * rate * basic_salary

    return {
        "years": years,
        "months": months,
        "days": days,
        "total_years": round(total_years, 4),
        "award_amount": round(eos_total, 2),
        "reason_of_eos": reason_of_eos,
    }


###########################################3333


@frappe.whitelist()
def create_end_of_service_additional_salary(
    employee_name,
    relieving_date,
    normal_eos_total,
    resignation_eos_total,
    reason_of_eos,
):
    """
    Create a additional Salary  for End of Service if it does not already exist.
    """
    additional_name = f"End of Service - {employee_name}"
    normal_eos_total = float(normal_eos_total)
    resignation_eos_total = float(resignation_eos_total)

    if frappe.db.exists("Additional Salary", additional_name):
        frappe.throw(
            _("Additional Salary '{0}' already exists.").format(additional_name)
        )

    additional_salary = frappe.new_doc("Additional Salary")
    additional_salary.payroll_date = relieving_date
    additional_salary.amount = (
        normal_eos_total if reason_of_eos == "Normal" else resignation_eos_total
    )
    additional_salary.salary_component = "End of Service"
    additional_salary.employee = employee_name
    additional_salary.insert()
    additional_salary.save()
    frappe.db.commit()

    return additional_salary.name
