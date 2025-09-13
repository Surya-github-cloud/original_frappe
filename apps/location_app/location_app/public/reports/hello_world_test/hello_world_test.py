def execute(filters=None):
    columns = [{"label": "Message", "fieldname": "message", "fieldtype": "Data"}]
    data = [{"message": "Hello World - The connection is working!"}]
    return columns, data
