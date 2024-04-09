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
			//default: frappe.datetime.month_start(),
			reqd: 1,
			on_change: function(query_report) {
				//const devise_from = frappe.defaults.get_default("currency");
				var pay_period = query_report.get_values().pay_period;
				var currency = query_report.get_values().currency;
				if (pay_period && currency) {
					frappe.call({
						method: "enabel.enabel.utils.get_salary_monthly_rate",
						args: {
							pay_period: pay_period,
						},
						callback: function (r) {
							frappe.query_report.set_filter_value({exchange_rate: flt(r.message)});
						}
					});
				}
				
			}
		},
		{
			fieldname:"currency",
			label: __("Devise"),
			fieldtype: "Link",
			options: "Currency",
			//default: frappe.datetime.month_end(),
			reqd: 1,
			on_change: function(query_report) {
				//const devise_from = frappe.defaults.get_default("currency");
				var pay_period = query_report.get_values().pay_period;
				var currency = query_report.get_values().currency;
				if (pay_period && currency) {
					frappe.call({
						method: "enabel.enabel.utils.get_salary_monthly_rate",
						args: {
							pay_period: pay_period,
						},
						callback: function (r) {
							frappe.query_report.set_filter_value({exchange_rate: flt(r.message)});
						}
					});
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
