# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ParentInquiry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		address: DF.SmallText | None
		email: DF.Data
		form_source: DF.Data | None
		grade: DF.Literal["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7"]
		lead_created: DF.Link | None
		parent_name: DF.Data
		phone_number: DF.Data
		phone_verified: DF.Check
		student_name: DF.Data
		submission_method: DF.Data | None
	# end: auto-generated types

	pass
