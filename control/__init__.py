class Status(dict):
    def __init__(self, message=None, success=True, alert=None, **kwargs):
        message = message or 'empty alert message by a lazy coder'
        success = success or True
        alert = alert or None
        self.update(kwargs)
        self.update({'message': message, 'success': success, 'alert': alert})

    def add(self, data):
        self.update(data)