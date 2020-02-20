from project.com.dao import con_db

class BankDAO:

    def insertBank(self,bankVO):
        print('========================IN INSERT BANK FUNCTION=============================')
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(" INSERT INTO bankmaster(bankName, bankCode, bankContact, bank_LoginId, bank_CityId, bank_AreaId) VALUES (' " + bankVO.bankName + " ' , ' " + bankVO.bankCode + " '  , ' " + bankVO.bankContact + " ' , ' " + bankVO.bank_LoginId + " ' , ' " + bankVO.bank_CityId + " ' , ' " + bankVO.bank_AreaId + " ') ")
        connection.commit()
        cursor1.close()
        connection.close()

    def viewBank(self):
        print('========================IN VIEW BANK FUNCTION=============================')
        connection = con_db()
        cursor2 = connection.cursor()
        cursor2.execute("SELECT bankId, bankName, bankCode, bankContact, loginEmail, cityName, areaName  FROM bankmaster INNER JOIN loginmaster ON bankmaster.bank_LoginId = loginmaster.loginId INNER JOIN citymaster ON bankmaster.bank_CityId = citymaster.cityId INNER JOIN areamaster ON bankmaster.bank_AreaId = areamaster.areaId WHERE bankActiveStatus='active' ")
        # cursor2.execute("SELECT bankId, bankName, bankCode, bankContact, loginEmail,  FROM bankmaster b  INNER JOIN loginmaster l WHERE bankActiveStatus= 'active' AND b.bank_LoginId = l.loginId ")
        bankDict = cursor2.fetchall()
        # print('bankdict hereeeeeeeeee')
        # print(bankDict)
        connection.commit()
        cursor2.close()
        connection.close()
        return bankDict

    def deleteBank(self,bankVO):
        print('========================IN DELETE BANK FUNCTION=============================')
        connection = con_db()
        cursor5 = connection.cursor()
        cursor5.execute("UPDATE bankmaster b, loginmaster l SET b.bankActiveStatus='deactive', l.loginActiveStatus = 'deactive' WHERE bankId='" + bankVO.bankId + "' AND b.bank_LoginId = l.loginID")
        connection.commit()
        cursor5.close()
        connection.close()

    def editBank(self,bankVO):
        print('========================IN EDIT BANK FUNCTION=============================')
        connection = con_db()
        cursor4 = connection.cursor()
        # cursor4.execute("SELECT * FROM bankmaster b INNER JOIN loginmaster l  WHERE b.bank_LoginId = l.loginId AND bankId='" + bankVO.bankId + "' ")
        cursor4.execute("SELECT * FROM bankmaster INNER JOIN loginmaster ON bankmaster.bank_LoginId = loginmaster.loginId WHERE bankId='" + bankVO.bankId + "' ")
        bankDict = cursor4.fetchall()
        # print(bankDict)
        cursor4.close()
        connection.close()
        return bankDict

    def updateBank(self,bankVO, loginVO):
        print('========================IN UPDATE BANK FUNCTION=============================')
        connection = con_db()
        cursor3 = connection.cursor()
        cursor3.execute("UPDATE bankmaster b, loginmaster l SET b.bankName = '" + bankVO.bankName + "', b.bankCode = '" + bankVO.bankCode + "', b.bankContact = '" + bankVO.bankContact + "', l.loginEmail = '" + loginVO.loginEmail + "', b.bank_CityId = '" + bankVO.bank_CityId + "', b.bank_AreaId = '" + bankVO.bank_AreaId + "' WHERE b.bankId = '" + bankVO.bankId + "' AND b.bank_LoginId = l.loginId")
        # cursor3.execute("UPDATE bankmaster SET bankName = '"+ bankVO.bankName +"', bankCode = '"+ bankVO.bankCode +"', bankContact = '"+ bankVO.bankContact +"', bankEmail = '"+ bankVO.bankEmail +"', bank_CityId = '"+ bankVO.bank_CityId +"', bank_AreaId = '"+ bankVO.bank_AreaId +"' WHERE bankId = '"+ bankVO.bankId +"' ")
        connection.commit()
        cursor3.close()
        connection.close()

    def getBankId(self,loginVO):
        print('========================IN GET BANKID FUNCTION=============================')
        connection = con_db()
        cursor6 = connection.cursor()
        cursor6.execute(" SELECT bankId from bankmaster b INNER JOIN loginmaster l ON b.bank_LoginId = l.loginId WHERE loginId = '" + loginVO.loginId + "' ")
        # cursor6.execute(" SELECT * from bankmaster b INNER JOIN loginmaster l WHERE b.bankId = '" + bankVO.bankId + "' ")
        staffDict = cursor6.fetchall()
        cursor6.close()
        connection.close()
        return staffDict

    def getBankName(self,bankVO):
        print('========================IN GET BANKNAME FUNCTION=============================')
        connection = con_db()
        cursor7 = connection.cursor()
        cursor7.execute("SELECT bankName FROM bankmaster WHERE bankId = ' "+ bankVO.bankId + " ' ")
        bankDict = cursor7.fetchall()
        cursor7.close()
        connection.close()
        return bankDict

