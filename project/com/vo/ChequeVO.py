from wtforms import *

class ChequeVO:

    chequeId = IntegerField
    cheque_FromBankId = IntegerField
    cheque_ToBankId = IntegerField
    cheque_StaffId = IntegerField
    chequeNumber = IntegerField
    chequeDate = DateTimeField
    chequePayTo = StringField
    chequePayFrom = StringField
    chequeAmount = StringField
    chequeIFSCCode = StringField
    chequeSignImagePath = StringField
    chequeSignImageName = StringField
    chequeActiveStatus = StringField
    chequeStatus = StringField


    # chequeUploadBy_LoginId = IntegerField
    #
    # chequeIFSCCode = StringField
    #
    # chequePayAccountNumber = StringField
    # chequeAmountWords = StringField
    # chequeAmountDigit = IntegerField
    # chequeByAccountNumber = StringField
    # chequeSignature = ???

    # chequeUploadDate = DateTimeField