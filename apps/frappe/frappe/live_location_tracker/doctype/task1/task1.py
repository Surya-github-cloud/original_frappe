# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Task1(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		assigned_to: DF.Link
		geofence_radius: DF.Float
		party: DF.DynamicLink
		party_type: DF.Literal["Customer", "Lead"]
		status: DF.Literal["Open", "Submitted", "Completed"]
	# end: auto-generated types

	pass
