// Copyright (c) 2023, Kossivi and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Redevances mensuelles IPR, INSS INPP par Province"] = {
	"filters": [
		{
			fieldname:"pay_period",
			label: __("Période"),
			fieldtype: "Link",
			options: "Payroll Period",
			//default: frappe.datetime.month_start(),
			reqd: 1
		},
		{
			fieldname:"currency",
			label: __("Devise"),
			fieldtype: "Link",
			options: "Currency",
			//default: frappe.datetime.month_end(),
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
			read_only: 1,
		},

	]
};
