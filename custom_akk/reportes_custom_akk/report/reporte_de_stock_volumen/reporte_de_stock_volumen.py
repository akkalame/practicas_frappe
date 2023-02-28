# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe


# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _


def execute(filters=None):
	#validate_warehouse(filters)
	columns = get_columns()
	data = get_data()
	return columns, data


def validate_warehouse(filters):
	company = filters.company
	warehouse = filters.warehouse
	if not frappe.db.exists("Warehouse", {"name": warehouse, "company": company}):
		frappe.throw(_("Warehouse: {0} does not belong to {1}").format(warehouse, company))


def get_columns():
	columns = [
		{"label": _("Codigo"), "fieldname": "item_code", "fieldtype": "Data", "width": 100},
		{"label": _("Producto"), "fieldname": "item_name", "fieldtype": "Data", "width": 200},
		{"label": _("Stock Actual"), "fieldname": "stock_qty", "fieldtype": "Float", "width": 150},
		{"label": _("Volumen"), "fieldname": "volumen", "fieldtype": "Float", "width": 150},
		{"label": _("Total Volumen"), "fieldname": "total_volumen", "fieldtype": "Float", "width": 150},
	]

	return columns


def get_data():
	item_list = frappe.get_all(
		"Item",
		fields=["item_code", "item_name", "volumen"],
	)

	data = []
	for item in item_list:

		actual_qty = frappe.db.get_value(
			"Bin", fieldname=["actual_qty"], filters={"item_code": item.item_code}
		)

		# frappe.db.get_value returns null if no record exist.
		if not actual_qty:
			actual_qty = 0

		total_volumen = item.volumen * actual_qty
		row = {
			"item_code": item.item_code,
			"item_name": item.item_name,
			"stock_qty": actual_qty,
			"volumen": item.volumen,
			"total_volumen": total_volumen
		}

		data.append(row)

	return data

