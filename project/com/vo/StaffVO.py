from wtforms import *

class StaffVO:

    staffId = IntegerField
    staffFirstName = StringField
    staffLastName = StringField
    staffGender = StringField
    staffDateOfBirth = DateField
    staffRole = StringField
    staffAddress = StringField
    staffContact = StringField
    # staffEmail = StringField
    staff_LoginId = IntegerField
    staff_CityId = IntegerField
    staff_AreaId = IntegerField
    staff_BankId = IntegerField
    staff_BranchId = IntegerField
    staffActiveStatus = StringField