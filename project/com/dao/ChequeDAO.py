from project.com.dao import con_db

class ChequeDAO:
    print("===============ChequeDAO Class===============")

    def insertChequeDetails(self,chequeVO):
        print('========================IN INSERT CHEQUE DEATILS FUNCTION=============================')
        connection = con_db()
        cursor1 = connection.cursor()
        print("cursor done")
        cursor1.execute("INSERT INTO chequemaster(cheque_FromBankId, cheque_ToBankId, cheque_StaffId, chequeNumber, chequeDate, chequePayTo, chequePayFrom, chequeAmount, chequeIFSCCode, chequeSignImagePath, chequeSignImageName) VALUES ( '"+ chequeVO.cheque_FromBankId+"', '"+ chequeVO.cheque_ToBankId+"', '"+ chequeVO.cheque_StaffId+"', '"+ chequeVO.chequeNumber +"', '"+ chequeVO.chequeDate +"', '"+ chequeVO.chequePayTo +"', '"+ chequeVO.chequePayFrom +"', '"+ chequeVO.chequeAmount +"', '"+ chequeVO.chequeIFSCCode +"', '"+ chequeVO.chequeSignImagePath +"', '"+ chequeVO.chequeSignImageName +"' ) ")
        connection.commit()
        cursor1.close()
        connection.close()

    def lastChequeId(self):
        print('========================IN LAST CHEQUEID FUNCTION=============================')
        connection = con_db()
        cursor8 = connection.cursor()
        cursor8.execute(" SELECT MAX(chequeId) FROM chequemaster ")
        lastchequeIdDict = cursor8.fetchall()
        print('lastchequeIdDict')
        print(lastchequeIdDict)
        cursor8.close()
        connection.close()
        return lastchequeIdDict

    def viewCheque(self, chequeVO):
        print('========================IN VIEW CHEQUE FUNCTION=============================')
        connection = con_db()
        cursor2 = connection.cursor()
        cursor3 = connection.cursor()

        print("QC")
        cursor2.execute(" SELECT chequeId,chequeStatus,chequeNumber,chequeDate,chequePayTo,chequePayFrom,chequeAmount,chequeIFSCCode,chequeSignImagePath,chequeSignImageName,bankName as cheque_FromBankName FROM chequemaster INNER JOIN bankmaster ON chequemaster.cheque_FromBankId = bankmaster.bankId WHERE cheque_StaffId = '"+ chequeVO.cheque_StaffId +"' AND chequeActiveStatus =  'active' ")

        print("QD")
        chequeDict = cursor2.fetchall()
        # fetchchequeId = str(chequeDict[0]['chequeId'])
        # print(fetchchequeId)
        # print('chequeId: {}'.format(fetchchequeId))
        print(chequeDict)

        if len(chequeDict) > 0:
            cursor3.execute(" SELECT bankName as cheque_ToBankName FROM chequemaster INNER JOIN bankmaster ON chequemaster.cheque_ToBankId = bankmaster.bankId ")
            cheque_ToBankName = cursor3.fetchall()
            print(cheque_ToBankName)
            print('length of chequeDict: {}'.format(len(chequeDict)))

            for i in range(0,len(chequeDict)):
                chequeDict[i].update(cheque_ToBankName[0])

            print('cheque dict')
            print(chequeDict)
            cursor3.close()

        cursor2.close()
        connection.close()
        return chequeDict

    def viewChequeAdmin(self):
        print('========================IN VIEW CHEQUE ADMIN FUNCTION=============================')
        connection = con_db()
        cursor4 = connection.cursor()
        cursor5 = connection.cursor()

        print("QC")
        #  WHERE PENDING -----ONLY FOR ADMIN
        cursor4.execute(" SELECT chequeId,chequeStatus,chequeNumber,chequeDate,chequePayTo,chequePayFrom,chequeAmount,chequeIFSCCode,chequeSignImagePath,chequeSignImageName,bankName as cheque_FromBankName FROM chequemaster INNER JOIN bankmaster ON chequemaster.cheque_FromBankId = bankmaster.bankId WHERE chequeActiveStatus = 'active' ")

        print("QD")
        chequeDict = cursor4.fetchall()

        print(chequeDict)

        if len(chequeDict) > 0:
            fetchchequeIds = []
            for j in range(0,len(chequeDict)):
                print(str(chequeDict[j]['chequeId']))
                fetchchequeIds.append(str(chequeDict[j]['chequeId']))


            # fetchchequeId = str(chequeDict[0]['chequeId'])
            print(fetchchequeIds)
            print('chequeIds: {}'.format(fetchchequeIds))

            for k in range(0,len(fetchchequeIds)):
                cursor5.execute(" SELECT bankName as cheque_ToBankName, chequeId FROM chequemaster INNER JOIN bankmaster ON chequemaster.cheque_ToBankId = bankmaster.bankId WHERE chequeId = '"+fetchchequeIds[k]+"' AND chequeActiveStatus = 'active' ")
                cheque_ToBankName = cursor5.fetchall()
                # number of fetchchequeIds is same as length of chequeDict so not needed another loop
                chequeDict[k].update(cheque_ToBankName[0])


            # print(cheque_ToBankName)
            print('length of chequeDict: {}'.format(len(chequeDict)))

            # for i in range(0,len(chequeDict)):
            #     chequeDict[i].update(cheque_ToBankName[0])

            print('cheque dict')
            print(chequeDict)
            cursor5.close()

        cursor4.close()
        connection.close()
        return chequeDict

    def viewChequeDetailsAdmin(self,chequeVO):
        print('========================IN VIEW CHEQUE FUNCTION=============================')
        connection = con_db()
        cursor6 = connection.cursor()
        cursor6.execute(" SELECT * FROM chequemaster WHERE chequeId = '"+ chequeVO.chequeId +"' ")
        chequeDict = cursor6.fetchall()
        print('chequeDict')
        print(chequeDict)
        cursor6.close()
        connection.close()
        return chequeDict

    def chequeValidateStatus(self, chequeVO):
        print('========================IN UPDATE CHEQUE VALIDATE STATUS FUNCTION=============================')
        connection = con_db()
        cursor7 = connection.cursor()
        print("cursor done")
        cursor7.execute(" UPDATE chequemaster SET chequeStatus = '"+ chequeVO.chequeStatus +"' WHERE chequeId = '"+ chequeVO.chequeId +"'  ")
        connection.commit()
        cursor7.close()
        connection.close()

    def getChequeData(self):
        connection = con_db()
        cursor8 = connection.cursor()
        chequeDataDict ={}


        cursor8.execute("SELECT COUNT(chequeId) as ApprovedCheques FROM chequemaster WHERE chequeStatus = 'Approved' AND chequeActiveStatus = 'active' ")
        chequeDict = cursor8.fetchall()
        chequeDataDict.update(chequeDict[0])


        cursor8.execute("SELECT COUNT(chequeId) as RejectedCheques FROM chequemaster WHERE chequeStatus = 'Rejected'AND chequeActiveStatus = 'active' ")
        chequeDict = cursor8.fetchall()
        chequeDataDict.update(chequeDict[0])


        cursor8.execute("SELECT COUNT(chequeId) as PendingCheques FROM chequemaster WHERE chequeStatus = 'pending' AND chequeActiveStatus = 'active' ")
        chequeDict = cursor8.fetchall()
        chequeDataDict.update(chequeDict[0])


        cursor8.close()
        connection.close()
        print('chequeDataDict')
        print(chequeDataDict)
        return chequeDataDict


    def getIssuedCheques(self,chequeVO):
        print("===================IN getIssuedCheques ============================")
        connection = con_db()
        cursor9 = connection.cursor()
        cursor9.execute("SELECT COUNT(chequeId) as TotalIssuedCheques FROM chequemaster WHERE cheque_FromBankId = '"+ chequeVO.cheque_FromBankId +"' AND chequeActiveStatus = 'active'  ")
        chequeDict = cursor9.fetchone()
        print('chequeDict: {}'.format(chequeDict))
        cursor9.close()
        connection.close()
        return chequeDict

    def StaffGetIssuedCheques(self,chequeVO):
        connection = con_db()
        cursor10 = connection.cursor()
        chequeDataDict = {}

        cursor10.execute(
            "SELECT COUNT(chequeId) as ApprovedCheques FROM chequemaster WHERE cheque_StaffId = '"+ chequeVO.cheque_StaffId +"' AND  chequeStatus = 'Approved' AND chequeActiveStatus = 'active' ")
        chequeDict = cursor10.fetchall()
        chequeDataDict.update(chequeDict[0])

        cursor10.execute(
            "SELECT COUNT(chequeId) as RejectedCheques FROM chequemaster WHERE cheque_StaffId = '"+ chequeVO.cheque_StaffId +"' AND chequeStatus = 'Rejected'AND chequeActiveStatus = 'active' ")
        chequeDict = cursor10.fetchall()
        chequeDataDict.update(chequeDict[0])

        cursor10.execute(
            "SELECT COUNT(chequeId) as PendingCheques FROM chequemaster WHERE cheque_StaffId = '"+ chequeVO.cheque_StaffId +"' AND chequeStatus = 'pending' AND chequeActiveStatus = 'active' ")
        chequeDict = cursor10.fetchall()
        chequeDataDict.update(chequeDict[0])

        cursor10.close()
        connection.close()
        print('chequeDataDict')
        print(chequeDataDict)
        return chequeDataDict
