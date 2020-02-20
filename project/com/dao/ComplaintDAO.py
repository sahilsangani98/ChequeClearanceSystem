from project.com.dao import con_db

class ComplaintDAO:
    print("IN COMPLAINTDAO CLASS")

    def insertComplaint(self, complaintVO):
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute(" INSERT INTO complaintmaster (complaintDate, complaintSubject, complaintDescription, complaintTo_LoginId, complaintFrom_LoginId) VALUES ('"+ complaintVO.complaintDate +"', '"+ complaintVO.complaintSubject +"', '"+ complaintVO.complaintDescription +"', '"+ complaintVO.complaintTo_LoginId +"', '"+ str(complaintVO.complaintFrom_LoginId) +"') ")
        # cursor1.execute("INSERT INTO complainmaster(complainTitle,complainDescription,complainActiveStatus,complainStatus,complainFrom_LoginId,complainTo)VALUES('" + complainVO.complainTitle + "','" + complainVO.complainDescription + "','" + complainVO.complainActiveStatus + "','"+complainVO.complainStatus+"','"+str(complainVO.complainFrom_LoginId)+"','"+str(complainVO.complainTo)+"') ")
        connection.commit()
        cursor1.close()
        connection.close()

    # To view own posted complaint
    def viewComplaint(self,complaintVO):
        print('========================IN VIEW COMPLAINT FUNCTION=============================')
        connection = con_db()
        cursor2 = connection.cursor()
        # print(complaintVO.complaintFrom_LoginId)
        # AND complaintStatus='pending'
        cursor2.execute("SELECT complaintId, complaintDate, complaintSubject, complaintDescription, complaintStatus, loginEmail FROM complaintmaster INNER JOIN loginmaster ON complaintmaster.complaintTo_LoginId = loginmaster.loginId WHERE complaintFrom_LoginId = '" + str(complaintVO.complaintFrom_LoginId) + "' AND complaintActiveStatus = 'active'   ")
        complaintDict = cursor2.fetchall()
        print(complaintDict)
        cursor2.close()
        connection.close()
        return complaintDict


    def deleteComplaint(self, complaintVO):
        connection = con_db()
        cursor3 = connection.cursor()
        cursor3.execute("UPDATE complaintmaster SET complaintActiveStatus='deactive' WHERE complaintId = '" + complaintVO.complaintId + "'")
        connection.commit()
        cursor3.close()
        connection.close()


    def editComplaint(self,complaintVO):
        print('========================IN EDIT COMPLAINT FUNCTION=============================')
        connection = con_db()
        cursor4 = connection.cursor()
        cursor4.execute("SELECT * FROM complaintmaster WHERE complaintId ='" + complaintVO.complaintId + "' ")
        complaintDict = cursor4.fetchall()
        print(complaintDict)
        cursor4.close()
        connection.close()
        return complaintDict


    def updateComplaint(self, complaintVO):
        connection = con_db()
        cursor4 = connection.cursor()
        cursor4.execute(" UPDATE complaintmaster SET complaintSubject = '"+ complaintVO.complaintSubject +"', complaintDescription = '" + complaintVO.complaintDescription +"' WHERE complaintId = '"+ complaintVO.complaintId +"' ")
        # cursor4.execute("UPDATE complaintmaster SET complaintStatus='"+complaintVO.complainStatus+"', complainDescription='" + complainVO.complainDescription + "',complainTitle='" + complainVO.complainTitle + "',complainReply='" + complainVO.complainReply + "',complainTo='"+str(complainVO.complainFromid)+"',complainFrom_LoginId='"+str(complainVO.complainTo)+"' WHERE complainId='" + complainVO.complainId + "'")
        print('UPDATE Q DONE')
        connection.commit()
        cursor4.close()
        connection.close()

    # For admin to view complaints posted by banks
    def viewbankComplaint(self):
        connection = con_db()
        cursor5 = connection.cursor()

         # AND complaintStatus = 'pending'
        cursor5.execute(" SELECT *, loginEmail  FROM complaintmaster INNER JOIN loginmaster ON complaintmaster.complaintFrom_LoginId = loginmaster.loginId WHERE complaintActiveStatus = 'active' AND complaintStatus = 'pending' AND loginmaster.loginRole = 'bank' ")
        # cursor5.execute(" SELECT * FROM complaintmaster INNER JOIN loginmaster ON complaintmaster.complaintFrom_LoginId = loginmaster.loginId WHERE complaintActiveStatus = 'active' AND complaintStatus = 'pending' AND loginmaster.loginRole = 'bank' ")
        # cursor5.execute("SELECT * FROM complaintmaster where complaintActiveStatus = 'active' AND complaintStatus = 'pending' AND loginmaster.loginId IN (SELECT loginmaster.loginId FROM loginmaster WHERE loginmaster.loginRole = 'bank') ")
        complaintDict = cursor5.fetchall()
        print(complaintDict)
        cursor5.close()
        connection.close()
        return complaintDict

    def viewStaffComplaint(self):
        connection = con_db()
        cursor8 = connection.cursor()

         # AND complaintStatus = 'pending'

        cursor8.execute(" SELECT * FROM complaintmaster INNER JOIN loginmaster ON complaintmaster.complaintFrom_LoginId = loginmaster.loginId WHERE complaintActiveStatus = 'active' AND complaintStatus = 'pending' AND loginmaster.loginRole = 'cashier' ")
        # cursor5.execute("SELECT * FROM complaintmaster where complaintActiveStatus = 'active' AND complaintStatus = 'pending' AND loginmaster.loginId IN (SELECT loginmaster.loginId FROM loginmaster WHERE loginmaster.loginRole = 'bank') ")
        complaintDict = cursor8.fetchall()
        print(complaintDict)
        connection.commit()
        cursor8.close()
        connection.close()
        return complaintDict

    def replyComplaint(self, complaintVO):
        connection = con_db()
        cursor6 = connection.cursor()
        cursor6.execute("SELECT * FROM complaintmaster WHERE complaintId = ' " + complaintVO.complaintId + " ' ")
        complaintDict = cursor6.fetchall()
        cursor6.close()
        connection.close()
        return complaintDict

    def submitReply(self,complaintVO):
        connection = con_db()
        cursor7 = connection.cursor()
        cursor7.execute(
            " UPDATE complaintmaster SET complaintReply = '" + complaintVO.complaintReply + "', complaintStatus = '"+ complaintVO.complaintStatus +"' WHERE complaintId = '" + complaintVO.complaintId + "' ")
        # cursor4.execute("UPDATE complaintmaster SET complaintStatus='"+complaintVO.complainStatus+"', complainDescription='" + complainVO.complainDescription + "',complainTitle='" + complainVO.complainTitle + "',complainReply='" + complainVO.complainReply + "',complainTo='"+str(complainVO.complainFromid)+"',complainFrom_LoginId='"+str(complainVO.complainTo)+"' WHERE complainId='" + complainVO.complainId + "'")
        connection.commit()
        cursor7.close()
        connection.close()


    def getAdminLoginID(self):
        connection = con_db()
        cursor8 = connection.cursor()
        cursor8.execute(" SELECT loginId FROM loginmaster WHERE loginRole = 'admin' ")
        adminLoginIds = cursor8.fetchall()
        cursor8.close()
        connection.close()
        print('adminloginid')
        print(adminLoginIds)
        return adminLoginIds

    def getComplaintData(self, complaintVO):
        connection = con_db()
        cursor9 = connection.cursor()
        complaintDataDict ={}

        cursor9.execute("SELECT COUNT(complaintId) as PendingComplaints FROM complaintmaster WHERE complaintTo_LoginId = '"+ complaintVO.complaintTo_LoginId +"' AND complaintStatus = 'pending'  AND complaintActiveStatus = 'active' ")
        complaintDict = cursor9.fetchall()
        complaintDataDict.update(complaintDict[0])


        cursor9.execute("SELECT COUNT(complaintId) as ResolvedComplaints FROM complaintmaster WHERE complaintTo_LoginId = '" + complaintVO.complaintTo_LoginId + "' AND complaintStatus = 'replied'  AND complaintActiveStatus = 'active' ")
        complaintDict = cursor9.fetchall()
        print('None test: {}'.format(complaintDict))  # Max function will retuen 'None'
        complaintDataDict.update(complaintDict[0])

        cursor9.close()
        connection.close()
        print('complaintDict')
        print(complaintDict)
        print(complaintDataDict)
        return complaintDataDict