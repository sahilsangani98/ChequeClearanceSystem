from project.com.dao import con_db

class LoginDAO():

    print("LoginDAO Class")
    def searchLogin(self,loginVO):
        print("===================IN SEARCH LOGIN============================")
        connection = con_db()
        cursor1 = connection.cursor()
        cursor1.execute("SELECT * FROM loginmaster where loginEmail = '"+ loginVO.loginEmail +"'  ")
        loginDict = cursor1.fetchall()
        connection.commit()
        cursor1.close()
        connection.close()
        return loginDict

    def insertLogin(self,loginVO):
        print("===================IN INSERT LOGIN============================")
        connection = con_db()
        cursor2 = connection.cursor()
        cursor2.execute("INSERT INTO loginmaster(loginEmail,loginPassword,loginRole)VALUES('" + loginVO.loginEmail + "','"+loginVO.loginPassword+"','"+loginVO.loginRole+"') ")
        connection.commit()
        connection.close()
        cursor2.close()

    def getLoginId(self):
        print("===================IN GET LOGINID============================")
        connection = con_db()
        cursor3 = connection.cursor()
        cursor3.execute("SELECT MAX(loginId) FROM loginmaster ")
        # cursor3.execute("SELECT * FROM loginmaster where loginEmail = '" + loginVO.loginEmail + "'  ")
        loginDict = cursor3.fetchall()
        cursor3.close()
        connection.close()
        return loginDict

    def updateLoginEmail(self,loginVO):
        print("===================IN INSERT LOGIN============================")
        connection = con_db()
        cursor4 = connection.cursor()
        print('cursor done')
        cursor4.execute(" UPDATE loginmaster SET loginEmail = '" + loginVO.loginEmail + "'  WHERE loginId = '" + loginVO.loginId + "'  ")
        # cursor4.execute(" UPDATE loginmaster SET loginEmail '" + loginVO.loginEmail + "'  WHERE loginId = '" + loginVO.loginId + "'  ")
        print('QD')
        # cursor2.execute("INSERT INTO loginmaster(loginEmail,loginPassword,loginRole)VALUES('" + loginVO.loginEmail + "','"+loginVO.loginPassword+"','"+loginVO.loginRole+"') ")
        connection.commit()
        cursor4.close()
        connection.close()

    def restrictDuplicateEmail(self, loginVO):
        print("===================IN restrictDuplicateEmail ============================")
        connection = con_db()
        cursor5 = connection.cursor()
        print('cursor done')

        try:
            cursor5.execute("SELECT COUNT(loginId) as EXISTANCE FROM loginmaster WHERE loginEmail='" + loginVO.loginEmail + "' AND loginActiveStatus = 'active' ")
            email = cursor5.fetchall()
            print('EMAIL: {}'.format(email))
            cursor5.close()
            connection.close()
            # return email[0]
            if email[0]['EXISTANCE'] != 0:
                email[0]['EXISTANCE'] = 'Already Exits'
            else:
                email[0]['EXISTANCE'] = 'Available'

            return email[0]

            # print('Finally found...!!')
            # return 'Already Exits'

        except:
            print('In except')
            # EXCEPT CODE HERE
            # print('Not found..!!')
            # return 'Available'

        # if email[0] == None:
        #     return 'True'
        # else:
        #     return 'False'
        # print('QD')
        # print('Emailllllllll: {}'.format(email[0]))
