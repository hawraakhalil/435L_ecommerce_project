class InsufficientStock(Exception):
    def __init__(self, message='Insufficient stock'):
        super().__init__(message)

class InsufficientBalance(Exception):
    def __init__(self, message='Insufficient balance'):
        super().__init__(message)
