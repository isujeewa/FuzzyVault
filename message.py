class Message:
    def __init__(self):
        self._id = "-"
        self.hash = "-"
        self.authurl = "None"
        # Note: In Python, you can't directly convert a GUID to int as in C#. You might need a different approach.
        # Here, I've just assigned 0b11011011 as a placeholder for the secret value.
        self.secret = 0b11011011
        self.height1 = 200
        self.height2 = 200
        self.authOption = 0
        self.distance = 2