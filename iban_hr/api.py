import frappe

from frappe import _
from frappe.utils import flt, date_diff
from dateutil.relativedelta import relativedelta
import datetime


@frappe.whitelist()
def calculate_employee_end_service_salary(
    joining_date, relieving_date, basic_salary, employee_name, reason_of_eos
):

    if not reason_of_eos:
        frappe.throw(_("Reason of End of Service is required."))

    # Convert date strings to datetime.date
    if isinstance(joining_date, str):
        joining_date = datetime.datetime.strptime(joining_date, "%Y-%m-%d").date()
    if isinstance(relieving_date, str):
        relieving_date = datetime.datetime.strptime(relieving_date, "%Y-%m-%d").date()

    # Calculate service duration
    diff = relativedelta(relieving_date, joining_date)
    years = diff.years
    months = diff.months
    days = diff.days

    total_years = years + months / 12 + days / 360
    basic_salary = float(basic_salary)

    # Fetch EOS settings
    settings = frappe.get_single("End of Service Gratuity Entitlement Settings")
    normal_slabs = settings.end_of_service or []
    resignation_slabs = settings.end_of_service_resignation or []

    if not normal_slabs:
        frappe.throw(_("No Normal EOS slabs found in settings."))

    # Step 1: Calculate normal EOS amount
    normal_slabs = sorted(normal_slabs, key=lambda x: x.from_year)
    eos_base_amount = 0.0
    remaining_years = total_years

    for slab in normal_slabs:
        start = slab.from_year
        end = slab.to_year
        rate = slab.eos_award

        if remaining_years <= 0:
            break

        if total_years > start:
            duration = min(remaining_years, end - start)
            eos_base_amount += duration * rate * basic_salary
            remaining_years -= duration

    # Step 2: Apply Resignation Multiplier if applicable
    final_award_amount = eos_base_amount

    if reason_of_eos == "Resignation":
        if not resignation_slabs:
            frappe.throw(_("No Resignation EOS slabs found in settings."))

        # Find multiplier based on total_years
        resignation_multiplier = 0.0
        for slab in resignation_slabs:
            if total_years > slab.from_year and total_years <= slab.to_year:
                resignation_multiplier = slab.eos_award
                break

        final_award_amount = eos_base_amount * resignation_multiplier

    return {
        "years": years,
        "months": months,
        "days": days,
        "total_years": round(total_years, 4),
        "base_eos_amount": round(eos_base_amount, 2),
        "award_amount": round(final_award_amount, 2),
        "reason_of_eos": reason_of_eos,
    }


@frappe.whitelist()
def create_end_of_service_additional_salary(
    employee_name,
    relieving_date,
    normal_eos_total,
    net_eos_total,
    reason_of_eos,
):
    """
    Create a additional Salary  for End of Service if it does not already exist.
    """
    additional_name = f"End of Service - {employee_name}"
    normal_eos_total = float(normal_eos_total)
    net_eos_total = float(net_eos_total)

    if frappe.db.exists("Additional Salary", additional_name):
        frappe.throw(
            _("Additional Salary '{0}' already exists.").format(additional_name)
        )

    additional_salary = frappe.new_doc("Additional Salary")
    additional_salary.payroll_date = relieving_date
    additional_salary.amount = net_eos_total
    additional_salary.salary_component = "End of Service"
    additional_salary.employee = employee_name
    additional_salary.insert()
    additional_salary.save()
    frappe.db.commit()

    return additional_salary.name
