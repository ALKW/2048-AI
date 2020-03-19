"""Custom defined exceptions"""

class Error(Exception):
    """Base class for exceptions in this module"""

class LengthError(Error):
    """
    Exception raised when an array with invalid length is passed
    
    Attributes
        - message: print out of the error
    """

    def __init__(self, message):
        super(LengthError, self).__init__(message)
        self.message = message
    

