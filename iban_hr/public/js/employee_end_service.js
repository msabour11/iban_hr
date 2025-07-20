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
              console.log(r.message);
                frappe.show_alert({
                  message: __("Salary Component created Successfully"),

                  indicator: "green",
                });
              //   if (r.message.salary_component) {
              //     frappe.msgprint(
              //       __("Salary Component created: {0}", [
              //         r.message.salary_component,
              //       ])
              //     );
              //   }
              // Optionally, redirect to the Salary Component form
              // Uncomment the following line if you want to redirect to the Salary Component form
              // frappe.set_route("Form", "Salary Component", {
              //   name: r.message.salary_component,
              //   frappe.set_route("Form", "Salary Component", {
              //     name: r.message.salary_component,
              //   });
            }
          },
        });
      });
    }
  },
});
