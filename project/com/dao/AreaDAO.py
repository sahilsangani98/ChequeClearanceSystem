from project.com.dao import con_db

class AreaDAO:

    def insertArea(self,areaVO):
        print("==============Insert Area Function==============")
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(
            "INSERT INTO areamaster(areaName,areaDescription,area_CityId)VALUES('" + areaVO.areaName + "','" + areaVO.areaDescription + "','" + areaVO.area_CityId + "') ")
        connection.commit()
        cursor1.close()
        connection.close()

    def viewArea(self):
        print("==============View Area Function==============")
        connection = con_db()
        cursor2 = connection.cursor()
        cursor2.execute(" SELECT areaId, areaName, areaDescription, cityName FROM areamaster INNER JOIN citymaster ON areamaster.area_CityId = citymaster.cityId WHERE areaActiveStatus = 'active'  ")
        # cursor2.execute("select areamaster.areaId, areamaster.areaName, areamaster.areaDescription, citymaster.cityName FROM areamaster INNER JOIN citymaster ON areamaster.area_CityId = citymaster.cityId where areaActiveStatus='active' ")
        areaDict = cursor2.fetchall()
        print(areaDict)
        connection.commit()
        cursor2.close()
        connection.close()
        return areaDict

    def editArea(self,areaVO):
        print("==============Edit Area Function==============")
        connection = con_db()
        cursor3 = connection.cursor()
        cursor3.execute(" SELECT * from areamaster WHERE areaId= ' "+ areaVO.areaId + " '   ")
        areaDict = cursor3.fetchall()
        connection.commit()
        cursor3.close()
        connection.close()
        print(areaDict)
        return areaDict

    def updateArea(self,areaVO):
        print("==============Update Area Function==============")
        connection = con_db()
        cursor4 = connection.cursor()
        cursor4.execute(
            "UPDATE areamaster SET areaDescription= '" + areaVO.areaDescription + "', areaName= '" + areaVO.areaName + "', area_CityId= '" + areaVO.area_CityId + "' WHERE areaId='" + areaVO.areaId + "'")
        connection.commit()
        cursor4.close()
        connection.close()

    def deleteArea(self,areaVO):
        connection = con_db()
        cursor5 = connection.cursor()
        cursor5.execute("UPDATE areamaster SET areaActiveStatus='deactive' WHERE areaId='" + areaVO.areaId + "'")
        connection.commit()
        cursor5.close()
        connection.close()

    def ajaxViewArea(self,areaVO):
        connection = con_db()
        cursor6 = connection.cursor()
        cursor6.execute("SELECT * FROM areamaster  WHERE area_CityId='" + str(areaVO.area_CityId) + "'")
        areaDict = cursor6.fetchall()
        connection.commit()
        cursor6.close()
        connection.close()
        return areaDict
