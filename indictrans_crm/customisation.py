from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.naming import make_autoname
import datetime

settings = frappe.get_doc("CRM Settings")
global_settings = frappe.get_doc("Global Defaults")


def set_image(self, method):
	self.sign = settings.signature
	self._address = settings.address
	

def set_address(self,method):
	self._address = settings.address
	self.dododododo = global_settings.current_fiscal_year

def get_user_permission(user):
	pass

@frappe.whitelist()
def set_terriotory(customer):
	terr_ = frappe.db.get_value("Customer",{"name":customer},["territory"])
	return terr_

def autoname(doc,method):
	fis_year = frappe.defaults.get_user_default("fiscal_year")
	fis_year = fis_year.split("-")
	doc.name = make_autoname("IT" + "/" + fis_year[0]+ "-"+fis_year[1][-2:] + "/" + ".###")
	
@frappe.whitelist()
def set_PT_on_sal_slip(doc,method):
	#print ("I am in Salary Slip Customisation")
	if doc:
		for row in doc.deductions:
			if row.salary_component == 'Professional Tax':
				if doc.gross_pay >= 7500.5 and doc.gross_pay < 10000.5 and doc.gender == 'Male':
					#print (":--------------------")
					frappe.db.set_value("Salary Detail", row.name, "amount", 175)
					row.amount=175
				elif doc.gross_pay >= 10000.5 and doc.gross_pay < 150000:
					frappe.db.set_value("Salary Detail", row.name, "amount", 200)
					row.amount = 200
					#print (":--------------------")
				else:
					frappe.db.set_value("Salary Detail", row.name, "amount", 0)
					row.amount = 0
					#print (":--------------------")
					

@frappe.whitelist()
def set_managers_score_on_appraisal(doc, method):
	#print ("I am in Manager's score update")
	total = 0
	if doc:
		for row in doc.goals:
			if row.score > 0:
				row.score = round(row.score)
			elif row.score < 0:
				row.score = 0
			if row.manager_score > 0:
				row.manager_score = round(row.manager_score)
				if row.manager_score > 5:
					row.manager_score = 5
				row.score_adjusted = row.manager_score * row.per_weightage / 100
				total = total + row.score_adjusted
			elif row.manager_score < 0:
				row.manager_score = 0
		if total > 0:
			doc.awarded_total_score = total

			

