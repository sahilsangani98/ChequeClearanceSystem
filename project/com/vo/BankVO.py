from wtforms import *


class BankVO:

    bankId = IntegerField
    bankName = StringField
    bankCode = StringField
    bankContact = StringField
    bank_LoginId = IntegerField
    # bankEmail = StringField
    bank_CityId = IntegerField
    bank_AreaId = IntegerField
    bankActiveStatus = StringField
