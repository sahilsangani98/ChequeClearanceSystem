from wtforms import *

class ComplaintVO:
    complaintId = IntegerField
    complaintDate = DateTimeField
    complaintSubject = StringField
    complaintDescription = StringField
    complaintStatus = StringField
    complaintTo_LoginId = IntegerField
    complaintFrom_LoginId = IntegerField
    complaintActiveStatus = StringField
    complaintReply = StringField
