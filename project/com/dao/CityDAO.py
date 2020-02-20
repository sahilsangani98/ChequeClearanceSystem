from project.com.dao import con_db


class CityDAO:

    def insertCity(self,cityVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute("INSERT INTO citymaster(cityName,cityDescription) VALUES (' " + cityVO.cityName + " ', ' " + cityVO.cityDescription + "')")
        connection.commit()
        cursor1.close()
        connection.close()

    def viewCity(self):
        connection = con_db()
        cursor2 = connection.cursor()
        cursor2.execute("SELECT * FROM citymaster where cityActiveStatus= 'active' ")
        cityDict = cursor2.fetchall()
        connection.commit()
        cursor2.close()
        connection.close()
        return cityDict

    def updateCity(self,cityVO):
        connection = con_db()
        cursor3 = connection.cursor()
        cursor3.execute(
            "UPDATE citymaster SET cityDescription='" + cityVO.cityDescription + "',cityName='" + cityVO.cityName + "' WHERE cityId='" + cityVO.cityId + "'")
        # cursor3.execute(" UPDATE citymaster SET cityName= '" + cityVO.cityName + "', cityDescription='" + cityVO.cityDescription +"'  ")
        connection.commit()
        cursor3.close()
        connection.close()

    def editCity(self, cityVO):
        connection = con_db()
        cursor4 = connection.cursor()
        cursor4.execute("SELECT * FROM citymaster WHERE cityId='" + cityVO.cityId + "' ")
        cityDict = cursor4.fetchall()
        cursor4.close()
        connection.close()
        return cityDict

    def deleteCity(self,cityVO):
        connection = con_db()
        cursor5 = connection.cursor()
        cursor5.execute(" UPDATE citymaster SET  cityActiveStatus='deactive' WHERE cityId=' " +cityVO.cityId + " ' ")
        connection.commit()
        cursor5.close()
        connection.close()

    # def change_area_according_to_city(self, cityVO):
    #     connection = con_db()
    #     cursor5 = connection.cursor()
    #     cursor5.execute("select cityId from citymaster WHERE cityName='" + cityVO.cityName + "' ")
    #     cityId = cursor5.fetchone()["cityId"]
    #     print(cityId)
    #     print(type(cityId))
    #     cursor5.execute("select areaName from areamaster WHERE area_CityId={}".format(cityId))
    #     newAreaDict = cursor5.fetchall()
    #
    #     print(newAreaDict)
    #     newArealist = []
    #     for areaName in newAreaDict:
    #         print(areaName)
    #         newAreaDict = newArealist.append(areaName["areaName"])
    #     cursor5.close()
    #     connection.close()
    #     return newArealist