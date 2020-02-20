from project.com.dao import con_db

class StaffDAO:
    print("STAFFDAO CLASS")

    def insertStaff(self,staffVO):
        print('========================IN INSERT STAFF FUNCTION=============================')
        connection = con_db()
        cursor1 = connection.cursor()
        print('qqqq')
        cursor1.execute(" INSERT INTO staffmaster(staffFirstName, staffLastName, staffGender, staffDateOfBirth, staffRole, staffAddress, staffContact, staff_CityId, staff_AreaId, staff_BankId, staff_BranchId, staff_LoginId) VALUES (' " + staffVO.staffFirstName + " ' , ' " + staffVO.staffLastName + " '  , ' " + staffVO.staffGender + " ' , ' " + staffVO.staffDateOfBirth + " ' , ' " + staffVO.staffRole + " ' , ' " + staffVO.staffAddress + " ', ' " + staffVO.staffContact + " ', ' " + staffVO.staff_CityId + " ',  ' " + staffVO.staff_AreaId + " ',  ' " + staffVO.staff_BankId + " ',  ' " + staffVO.staff_BranchId + " ', ' " + staffVO.staff_LoginId + " ') ")
        connection.commit()
        cursor1.close()
        connection.close()


    def viewStaff(self, staffVO):
        print('========================IN VIEW STAFF FUNCTION=============================')
        connection = con_db()
        cursor2 = connection.cursor()

        cursor2.execute("SELECT staffId, staffFirstName, staffLastName, staffGender, staffDateOfBirth, staffRole, staffAddress, staffContact, loginEmail , cityName, areaName, bankName, branchName FROM staffmaster INNER JOIN citymaster ON staffmaster.staff_CityId = citymaster.cityId INNER JOIN areamaster ON staffmaster.staff_AreaId = areamaster.areaId INNER JOIN bankmaster ON staffmaster.staff_BankId = bankmaster.bankId INNER JOIN branchmaster ON staffmaster.staff_BranchId = branchmaster.branchId INNER JOIN loginmaster ON staffmaster.staff_LoginId = loginmaster.loginId WHERE staffActiveStatus= 'active' AND staff_BankId = '"+ staffVO.staff_BankId +"' ")
        # cursor2.execute("SELECT * FROM staffmaster where staffActiveStatus= 'active' ")

        # Chage code to show particular branch's staff --- WHERE CONDITION PENDING

        staffDict = cursor2.fetchall()
        print('staff dict')
        print(staffDict)
        cursor2.close()
        connection.close()
        return staffDict


    def deleteStaff(self,staffVO):
        print('========================IN DELETE STAFF FUNCTION=============================')
        connection = con_db()
        cursor5 = connection.cursor()
        cursor5.execute("UPDATE staffmaster SET staffActiveStatus='deactive' WHERE staffId='" + staffVO.staffId + "'")
        connection.commit()
        cursor5.close()
        connection.close()


    def editStaff(self,staffVO):
        print('========================IN EDIT STAFF FUNCTION=============================')
        connection = con_db()
        cursor4 = connection.cursor()
        cursor4.execute("SELECT *, loginEmail FROM staffmaster INNER JOIN loginmaster ON loginmaster.loginId = staffmaster.staff_LoginId WHERE staffId='" + staffVO.staffId + "' ")
        # cursor4.execute("select * from staffmaster WHERE staffId='" + staffVO.staffId + "' ")
        staffDict = cursor4.fetchall()
        cursor4.close()
        connection.close()
        return staffDict


    def updateStaff(self,staffVO):
        print('========================IN UPDATE STAFF FUNCTION=============================')
        connection = con_db()
        cursor3 = connection.cursor()
        print('QA')
        cursor3.execute(" UPDATE staffmaster SET staffFirstName = '" + staffVO.staffFirstName + "', staffLastName = '" + staffVO.staffLastName + "', staffGender = '" + staffVO.staffGender + "', staffDateOfBirth = '"+ staffVO.staffDateOfBirth + "', staffRole = '" + staffVO.staffRole + "', staffAddress = '"+ staffVO.staffAddress +"', staffContact = '" + staffVO.staffContact + "', staff_CityId = '" + staffVO.staff_CityId + "', staff_AreaId = '" + staffVO.staff_AreaId + "', staff_BranchId = '" + staffVO.staff_BranchId + "' WHERE staffId = '" + staffVO.staffId +"' ")
        print('QB')
        connection.commit()
        cursor3.close()
        connection.close()

    def getStaffIds(self,staffVO):
        print('========================IN GET STAFFID FUNCTION=============================')
        connection = con_db()
        cursor6 = connection.cursor()
        cursor6.execute(" SELECT staffId, staff_BankId, staff_BranchId, bank_LoginId  FROM staffmaster s INNER JOIN loginmaster l ON s.staff_LoginId = l.loginId INNER JOIN bankmaster b ON s.staff_BankId = b.bankId  WHERE loginId = '" + staffVO.staff_LoginId + "' ")
        # cursor6.execute(" SELECT * from bankmaster b INNER JOIN loginmaster l WHERE b.bankId = '" + bankVO.bankId + "' ")
        bankDict = cursor6.fetchall()
        cursor6.close()
        connection.close()
        return bankDict

    def getBankEmployees(self,staffVO):
        print("===================IN getBankEmployees ============================")
        connection = con_db()
        cursor7 = connection.cursor()
        cursor7.execute("SELECT COUNT(staffId) as TotalEmployees FROM staffmaster WHERE staff_BankId = '"+ staffVO.staff_BankId +"' AND staffActiveStatus = 'active'  ")
        staffDict = cursor7.fetchone()
        print('staffDict: {}'.format(staffDict))
        cursor7.close()
        connection.close()
        return staffDict