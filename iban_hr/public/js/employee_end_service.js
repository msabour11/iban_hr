frappe.ui.form.on("Employee", {
  refresh: function (frm) {
    if (
      frm.doc.status === "Active" &&
      frm.doc.date_of_joining &&
      frm.doc.relieving_date &&
      frm.doc.custom_basic_salary
    ) {
      var joining_date = frm.doc.date_of_joining;
      var relieving_date = frm.doc.relieving_date;
      var basic_salary = frm.doc.custom_basic_salary;
      var employee_name = frm.doc.name;
      // var reason_of_eos = frm.doc.custom_reason_of_eos;

      ////////////////////////////////////////////////////////////////////
      frm.add_custom_button(
        __("Choose End Of Service"), // The button label will be translated
        function () {
          // Open a dialog to select the target warehouse
          let d = new frappe.ui.Dialog({
            title: __("Create End Of Service "), // Translate the dialog title
            fields: [
              {
                label: __("Reason of EOS "), // Translate the label
                fieldname: "custom_reason_of_eos",
                fieldtype: "Select",
                options: "Normal\nResignation\n",
                reqd: 1,
              },
            ],
            primary_action_label: __("Create"), // Translate the action button label
            primary_action: function (values) {
              // Call the server-side method
              frappe.call({
                method: "iban_hr.api.calculate_employee_end_service_salary",
                args: {
                  joining_date: joining_date,
                  relieving_date: relieving_date,
                  basic_salary: basic_salary,
                  employee_name: employee_name,
                  reason_of_eos: values.custom_reason_of_eos,
                },
                callback: function (r) {
                  if (!r.exc) {
                    // frappe.msgprint(__("End of service created successfully")); // Translate the success message
                    // frm.reload_doc(); // Reload the form
                    let base_eos_amount = r.message.base_eos_amount;
                    let award_amount = r.message.award_amount;
                    let reason_of_eos = r.message.reason_of_eos;
                    let eos_years = r.message.total_years;
                    console.log(r.message);
                    console.log(r.message.award_amount);

                    if (reason_of_eos === "Normal") {
                      frm.set_value(
                        "custom_end_of_service_amount",
                        base_eos_amount
                      );
                      frm.set_value(
                        "custom_net_end_of_service_amount",
                        award_amount
                      );
                      frm.set_value("custom_reason_of_eos", reason_of_eos);
                    } else if (reason_of_eos === "Resignation") {
                      frm.set_value(
                        "custom_net_end_of_service_amount",
                        award_amount
                      );
                      frm.set_value(
                        "custom_end_of_service_amount",
                        base_eos_amount
                      );
                      frm.set_value("custom_reason_of_eos", reason_of_eos);
                      // Set to 0 for resignation
                    } else {
                      frappe.throw(
                        __("Please select a valid reason for End of Service")
                      );
                    }
                    frm.set_value("custom_eos_years", eos_years);
                    frm.refresh_field("custom_end_of_service_amount");
                    frm.save();

                    frappe.show_alert({
                      message: __("End of service add Successfully"),

                      indicator: "green",
                    });
                  }
                },
              });
              d.hide();
            },
          });
          d.show();
        }
      );
    }
    // Check if relieving date and end of service amount are set
    let reason_of_eos = frm.doc.custom_reason_of_eos;
    if (
      frm.doc.relieving_date &&
      (frm.doc.custom_end_of_service_amount ||
        frm.doc.custom_net_end_of_service_amount)
    ) {
      frm.add_custom_button(
        __("Create End of Service Additional Salary"),
        function () {
          frappe.call({
            method: "iban_hr.api.create_end_of_service_additional_salary",
            args: {
              employee_name: frm.doc.name,
              relieving_date: frm.doc.relieving_date,
              normal_eos_total: frm.doc.custom_end_of_service_amount,
              net_eos_total: frm.doc.custom_net_end_of_service_amount,
              reason_of_eos: reason_of_eos,
            },
            callback: function (r) {
              if (r.message) {
                frappe.show_alert({
                  message: __(
                    "End of Service Salary Component created Successfully"
                  ),
                  indicator: "green",
                });
              }
            },
          });
        }
      );
    }
  },
});
