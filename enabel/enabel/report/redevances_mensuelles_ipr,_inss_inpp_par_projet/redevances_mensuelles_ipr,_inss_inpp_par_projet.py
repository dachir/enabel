# Copyright (c) 2023, Kossivi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	columns = [
		{ "label": _("Code Projet Débiteur"), "fieldtype": "Link",	"fieldname": "projet", "options": "Project", "width": 100, },
		{ "label": _("Acronyme ou nom du projet"), "fieldtype": "Data", "fieldname": "project_name", "width": 100, },
		{ "label": _("Effectif DOP"), "fieldtype": "int", "fieldname": "effectif", "width": 100, },
		{ "label": _("Effectif Data"), "fieldtype": "int", "fieldname": "nb", "width": 100, },
		{ "label": _("Base CNSS"), "fieldtype": "Currency", "fieldname": "base_inss", "options": "currency", "width": 100, },
		{ "label": _("Base IPR"), "fieldtype": "Currency", "fieldname": "base_ipr", "options": "currency", "width": 100, },
		{ "label": _("IPR"), "fieldtype": "Currency", "fieldname": "ipr", "options": "currency", "width": 100, },
		{ "label": _("CNSS QPO"), "fieldtype": "Currency", "fieldname": "inssqpo", "options": "currency", "width": 100, },
		{ "label": _("CNSS QPP"), "fieldtype": "Currency", "fieldname": "inssqpp", "options": "currency", "width": 100, },
		{ "label": _("TOTAL CNSS"), "fieldtype": "Currency", "fieldname": "total_inss", "options": "currency", "width": 100, },
		{ "label": _("ONEM"), "fieldtype": "Currency", "fieldname": "onem", "options": "currency", "width": 100, },
		{ "label": _("INPP"), "fieldtype": "Currency", "fieldname": "inpp", "options": "currency", "width": 100, },
		{ "label": _("TOTAL"), "fieldtype": "Currency", "fieldname": "total", "options": "currency", "width": 100, },
	]
	return columns

#get the data
def get_data(filters):

	data = frappe.db.sql(
        """
        SELECT v.*, v.inssqpo + v.inssqpp AS total_inss, v.ipr AS total_ipr, %(currency)s AS currency,
        v.inssqpo + v.inssqpp + v.ipr + v.onem + v.inpp as total,
         (SELECT COUNT(e2.name) FROM tabEmployee e2 WHERE e2.status = 'Active' AND e2.projet = v.projet) as effectif
		FROM(
			SELECT t.projet, t.project_name, COUNT(DISTINCT t.name) AS nb, SUM(t.base) *  %(exchange_rate)s AS base_inss, SUM(t.base * 0.95) *  %(exchange_rate)s AS base_ipr, SUM(t.base) *  %(exchange_rate)s AS base_INPP, 
			SUM(t.ipr) *  %(exchange_rate)s AS ipr, SUM(t.inssqpo) *  %(exchange_rate)s AS inssqpo, SUM(t.inssqpp) *  %(exchange_rate)s AS inssqpp, SUM(onem) *  %(exchange_rate)s AS onem, SUM(inpp) *  %(exchange_rate)s AS inpp
			FROM
				(SELECT s.pay_period, s.name, e.branch, e.projet, p.project_name,s.currency,
					SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'SJ' THEN amount ELSE 0 END) + SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'AP' THEN amount ELSE 0 END) + 
					SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'AE' THEN amount ELSE 0 END) + SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'APM' THEN amount ELSE 0 END) + 
					SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'CM' THEN amount ELSE 0 END) + SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'PC' THEN amount ELSE 0 END) + 
					SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'PFA' THEN amount ELSE 0 END) + SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'CA' THEN amount ELSE 0 END) + 
					SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'H130' THEN amount ELSE 0 END) + SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'H160' THEN amount ELSE 0 END) +
					SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'H200' THEN amount ELSE 0 END) + SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'CMJ' THEN amount ELSE 0 END) + 
					SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'CC' THEN amount ELSE 0 END) + SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'CMT6' THEN amount ELSE 0 END) + 
					SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'CMT8' THEN amount ELSE 0 END) + SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'Préavispresté' THEN amount ELSE 0 END) + 
                    SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'preavisnonpresté' THEN amount ELSE 0 END) + SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'Créditencours' THEN amount ELSE 0 END) +
                    SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'Créditnonpris' THEN amount ELSE 0 END) + SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'CPREAVIS' THEN amount ELSE 0 END) +
                    SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'PéculeCongéprorata' THEN amount ELSE 0 END) + SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'Primefindannéeprorata' THEN amount ELSE 0 END) + 
                    SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'Primederentrescolaireprorata' THEN amount ELSE 0 END) + SUM(CASE WHEN d.parentfield = 'earnings' AND d.abbr = 'P' THEN amount ELSE 0 END)
					AS base,
					SUM(CASE WHEN d.parentfield = 'deductions' AND d.abbr = 'CNSS' THEN amount ELSE 0 END) AS inssqpo,
					SUM(CASE WHEN d.parentfield = 'deductions' AND d.abbr = 'inssemp' THEN amount ELSE 0 END) AS inssqpp,
					SUM(CASE WHEN d.parentfield = 'deductions' AND d.abbr = 'inppemp' THEN amount ELSE 0 END) AS inpp,
					SUM(CASE WHEN d.parentfield = 'deductions' AND d.abbr = 'IPR' THEN amount ELSE 0 END) AS ipr,
					SUM(CASE WHEN d.parentfield = 'deductions' AND d.abbr = 'onememp' THEN amount ELSE 0 END) AS onem
				FROM `tabSalary Slip` s INNER JOIN `tabSalary Detail` d ON s.name = d.parent INNER JOIN tabEmployee e ON e.name = s.employee LEFT JOIN tabProject p ON p.name = e.projet
				GROUP BY s.pay_period, s.name, e.branch, e.projet, p.project_name,s.currency) AS t
			WHERE t.pay_period = %(pay_period)s
			GROUP BY t.projet, t.project_name
		) v
        """,{"pay_period": filters.pay_period, "currency": filters.currency, "exchange_rate": filters.exchange_rate}, as_dict = 1
    )

	return data

