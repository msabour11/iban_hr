frappe.ui.form.on("Employee", {
  //   after_save: function (frm) {
  //     if (frm.doc.status === "Left") {
  //       frappe.call({
  //         method:
  //           "iban_hr.iban_hr.doctype.employee.employee.create_end_service_record",
  //         args: {
  //           employee: frm.doc.name,
  //         },
  //         callback: function (r) {
  //           if (r.message) {
  //             frappe.msgprint(__("End Service Record created successfully."));
  //           }
  //         },
  //       });
  //     }
  //   },

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

      frm.add_custom_button(__("End Service Record"), function () {
        // frappe.set_route("Form", "End Service Record", {
        //   employee: frm.doc.name,
        // });
        frappe.call({
          method: "iban_hr.api.calculate_employee_end_service_salary",
          args: {
            joining_date: joining_date,
            relieving_date: relieving_date,
            basic_salary: basic_salary,
            employee_name: employee_name,
          },
          callback: function (r) {
            if (r.message) {
              //   frappe.set_route("Form", "End Service Record", r.message);
              var end_service_salary = r.message.award_amount;
              console.log(r.message);
              // frappe.show_alert({
              //   message: __("Salary Component created Successfully"),

              //   indicator: "green",
              // });
              frm.set_value("custom_end_of_service_amount", end_service_salary);
              frm.refresh_field("custom_end_of_service_amount");
              frm.save();
            }
          },
        });
      });
    }

    if (frm.doc.relieving_date && frm.doc.custom_end_of_service_amount) {
      frm.add_custom_button(
        __("Create End of Service Additional Salary"),
        function () {
          frappe.call({
            method: "iban_hr.api.create_end_of_service_additional_salary",
            args: {
              employee_name: frm.doc.name,
              relieving_date: frm.doc.relieving_date,
              eos_total: frm.doc.custom_end_of_service_amount,
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
