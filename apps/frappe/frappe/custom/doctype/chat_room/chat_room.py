# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ChatRoom(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.custom.doctype.chat_participant.chat_participant import ChatParticipant
		from frappe.types import DF

		amended_from: DF.Link | None
		created_by: DF.Link | None
		last_message_time: DF.Datetime | None
		long_message: DF.LongText | None
		participants: DF.Table[ChatParticipant]
		room_type: DF.Literal["Direct", "Group"]
		title: DF.Data
	# end: auto-generated types

	pass
