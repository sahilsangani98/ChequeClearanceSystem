from project.com.dao import con_db

class BranchDAO:
    print("===============BranchDAO Class===============")
    def insertBranch(self,branchVO):
        print('========================IN INSERT BRANCH FUNCTION=============================')
        connection = con_db()
        cursor1 = connection.cursor()
        print("cursor done")
        cursor1.execute(" INSERT INTO branchmaster (branchName, branchIFSCCode, branchContact, branchEmail, branch_CityId, branch_AreaId, branch_BankId) VALUES (' " + branchVO.branchName + " ' , ' " + branchVO.branchIFSCCode+ " '  , ' " + branchVO.branchContact+ " ' , ' " + branchVO.branchEmail + " ' , ' " + str(branchVO.branch_CityId) + " ' , ' " + str(branchVO.branch_AreaId) + " ', ' " + str(branchVO.branch_BankId) + " ' ) ")
        connection.commit()
        cursor1.close()
        connection.close()

    def viewBranch(self,bankVO):
        print('========================IN VIEW BRANCH FUNCTION=============================')
        connection = con_db()
        cursor2 = connection.cursor()
        cursor2.execute("SELECT branchId, branchName, branchIFSCCode, branchContact, branchEmail, cityName, areaName, branch_BankId FROM branchmaster INNER JOIN citymaster ON branchmaster.branch_CityId = citymaster.cityId INNER JOIN areamaster ON branchmaster.branch_AreaId = areamaster.areaId WHERE branchActiveStatus= 'active' AND branch_BankId = '" + bankVO.bankId + "' ")

        # cursor2.execute("SELECT * FROM branchmaster WHERE branchActiveStatus= 'active' AND branch_BankId = '" + bankVO.bankId+ "' ")

        # Change code to show particular bank's branches --- WHERE CONDITION PENDING

        branchDict = cursor2.fetchall()
        connection.commit()
        cursor2.close()
        connection.close()
        return branchDict

    def deleteBranch(self,branchVO):
        print('========================IN DELETE BRANCH FUNCTION=============================')
        connection = con_db()
        cursor5 = connection.cursor()
        cursor5.execute("UPDATE branchmaster SET branchActiveStatus='deactive' WHERE branchId='" + branchVO.branchId + "'")
        connection.commit()
        cursor5.close()
        connection.close()

    def editBranch(self,branchVO):
        print('========================IN EDIT BRANCH FUNCTION=============================')
        connection = con_db()
        cursor4 = connection.cursor()
        cursor4.execute("select * from branchmaster WHERE branchId='" + branchVO.branchId + "' ")
        branchDict = cursor4.fetchall()
        cursor4.close()
        connection.close()
        return branchDict

    def updateBranch(self,branchVO):
        print('========================IN UPDATE BANK FUNCTION=============================')
        connection = con_db()
        cursor3 = connection.cursor()
        cursor3.execute(" UPDATE branchmaster SET branchName = '" + branchVO.branchName + "', branchIFSCCode = '" + branchVO.branchIFSCCode + "', branchContact = '" + branchVO.branchContact + "', branchEmail = '"+ branchVO.branchEmail + "', branch_CityId = '" + branchVO.branch_CityId + "', branch_AreaId = '"+ branchVO.branch_AreaId +"', branch_BankId = '" + branchVO.branch_BankId + "' WHERE branchId = '" + branchVO.branchId +"' ")
        # cursor3.execute("UPDATE branchmaster SET branchName = '"+ branchVO.branchName +"', branchIFSCCode = '"+ branchVO.branchIFSCCode +"', branchContact = '"+ branchVO.branchContact +"', branchEmail = '"+ branchVO.branchEmail +"', branch_CityId = '"+ branchVO.branch_CityId +"', branch_AreaId = '"+ branchVO.branch_AreaId +"' WHERE branchId = '"+ branchVO.branchId +"' ")
        connection.commit()
        cursor3.close()
        connection.close()

    def getBankBranches(self,branchVO):
        print("===================IN getBankBranches ============================")
        connection = con_db()
        cursor6 = connection.cursor()
        cursor6.execute("SELECT COUNT(branchId) as TotalBranches FROM branchmaster WHERE branch_BankId = '"+ branchVO.branch_BankId +"' AND branchActiveStatus = 'active'  ")
        branchDict = cursor6.fetchone()
        print('branchdict: {}'.format(branchDict))
        cursor6.close()
        connection.close()
        return branchDict