from wtforms import *

class AreaVO:

    areaId = IntegerField
    areaName = StringField
    areaDescription = StringField
    area_CityId = IntegerField
    areaActiveStatus = StringField