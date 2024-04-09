import frappe
from frappe import _

def get_salary_monthly_rate(pay_period):
	taux_de_change = frappe.db.sql(
			"""
			SELECT MAX(taux_de_change) AS taux_de_change
			FROM `tabPayroll Entry`
			WHERE payroll_period = %s 
			""", (pay_period),
			as_dict = 1
		)[0].taux_de_change

	return taux_de_change if taux_de_change else 1