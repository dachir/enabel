// Copyright (c) 2023, Kossivi and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Redevances mensuelles IPR, INSS INPP par Projet"] = {
	"filters": [
		{
			fieldname:"pay_period",
			label: __("Période"),
			fieldtype: "Link",
			options: "Payroll Period",
			reqd: 1,
			// a finir le jour ou ils demandent que le cours de la devise soit à la date de transaction
			/*on_change: function(query_report) {
				var fiscal_year = query_report.get_values().fiscal_year;
				if (!fiscal_year) {
					return;
				}
				frappe.model.with_doc("Fiscal Year", fiscal_year, function(r) {
					var fy = frappe.model.get_doc("Fiscal Year", fiscal_year);
					frappe.query_report.set_filter_value({
						from_date: fy.year_start_date,
						to_date: fy.year_end_date
					});
				});
			}*/
		},
		{
			fieldname:"currency",
			label: __("Devise"),
			fieldtype: "Link",
			options: "Currency",
			reqd: 1,
			on_change: function(query_report) {
				const devise_from = frappe.defaults.get_default("currency");
				var devise_to = query_report.get_values().currency;
				if (devise_from && devise_to) {
					if (devise_to != devise_from) {
						frappe.call({
							method: "erpnext.setup.utils.get_exchange_rate",
							args: {
								from_currency: devise_from,
								to_currency: devise_to,
								//transaction_date: end_date,
							},
							callback: function (r) {
								frappe.query_report.set_filter_value({exchange_rate: flt(r.message)});
							}
						});
					} else {
						frappe.query_report.set_filter_value({exchange_rate: 1.0});
					}
				}
				
			}
		},
		{
			fieldname: "exchange_rate",
			label: __("Cours"),
			fieldtype: "Data",
			default: 1,
			//read_only: 1,
		},

	]
};
