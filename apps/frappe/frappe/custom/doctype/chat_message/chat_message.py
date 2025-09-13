# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ChatMessage(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		chat_room: DF.Link | None
		is_read: DF.Check
		message: DF.LongText
		message_type: DF.Literal["Text", "Image", "File"]
		sender: DF.Link
		sender_name: DF.Data | None
		timestamp: DF.Datetime | None
	# end: auto-generated types

	pass
