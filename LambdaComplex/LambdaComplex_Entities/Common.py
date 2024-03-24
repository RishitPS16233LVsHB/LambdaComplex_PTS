import datetime


class BaseEntity:
    def __init__(self):
        self.CreatedOn = datetime.now()
        self.ModifiedOn = datetime.now()
        self.IsDeleted = False

class Response:
    def __init__(self):
        self.Data = None
        self.Message = ""
        self.WasSuccessful = False