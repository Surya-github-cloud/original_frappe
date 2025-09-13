# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CheckIn(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		assigned_to: DF.Link
		photo_proof: DF.AttachImage
		task1: DF.Link
		timestamp: DF.Datetime
		verification_status: DF.Literal["Pending", "Verified", "Out of Radius"]
	# end: auto-generated types

	pass
