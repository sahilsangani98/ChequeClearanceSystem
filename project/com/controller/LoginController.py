from project import app
from flask import render_template, redirect, request, url_for, session
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.LoginVO import LoginVO
from project.com.dao.BankDAO import BankDAO
from project.com.vo.BankVO import BankVO
from project.com.dao.BranchDAO import BranchDAO
from project.com.vo.BranchVO import BranchVO
from project.com.vo.StaffVO import StaffVO
from project.com.dao.StaffDAO import StaffDAO
from project.com.vo.ComplaintVO import ComplaintVO
from project.com.dao.ComplaintDAO import ComplaintDAO
from project.com.vo.ChequeVO import ChequeVO
from project.com.dao.ChequeDAO import ChequeDAO

@app.route('/checkLogin', methods=['post'])
def checkLogin():

    # Creating objects of LoginVO and LoginDAO
    loginDAO = LoginDAO()
    loginVO = LoginVO()

    # Getting infromation from HTML form and storing it in VO objects
    loginVO.loginEmail = request.form['loginEmail']
    loginVO.loginPassword = request.form['loginPassword']

    # print(loginVO.loginEmail)
    # print(loginVO.loginPassword)
    loginDict = loginDAO.searchLogin(loginVO)
    print(loginDict)



    # print(loginDict['loginPassword'])
    # print(loginVO.loginPassword)

    if(len(loginDict) == 0):

        return render_template('admin/login.html', msg = 'Please enter valid Email Address')

    elif(loginVO.loginPassword != loginDict[0]['loginPassword']):

        return render_template('admin/login.html', msg='Please enter correct password...!!')

    elif(loginDict[0]['loginRole'] == 'admin'):

                # Storing loginEmail & Password in Session
                session['loginId'] = loginDict[0]['loginId']
                session['loginRole'] = loginDict[0]['loginRole']

                complaintDAO = ComplaintDAO()
                complaintVO = ComplaintVO()
                complaintVO.complaintTo_LoginId = str(session['loginId'])
                complaintDict = complaintDAO.getComplaintData(complaintVO)
                print('complaintDict: {}'.format(complaintDict))

                chequeDAO = ChequeDAO()
                chequeVO = ChequeVO()
                chequeDict = chequeDAO.getChequeData()
                print('chequeDict: {}'.format(chequeDict))

                return render_template('admin/index.html', complaintDict=complaintDict, chequeDict=chequeDict)

    elif (loginDict[0]['loginRole'] == 'bank'):

                # Storing loginEmail & Password in Session
                session['loginId'] = loginDict[0]['loginId']
                session['loginRole'] = loginDict[0]['loginRole']

                bankVO = BankVO()
                # bankVO.bankId = str(session['loginId'])
                bankDAO = BankDAO()
                # bankdata = bankDAO.getBankId(bankVO)
                loginVO.loginId = str(session['loginId'])
                bankId = bankDAO.getBankId(loginVO)
                print("+++++++++++++++++++++++++BANKDATA+++++++++++++++++++++++++++++++++++")
                print(bankId)
                bankId = bankId[0]['bankId']
                print(bankId)
                session['bankId'] = bankId

                complaintDAO = ComplaintDAO()
                complaintVO = ComplaintVO()
                complaintVO.complaintTo_LoginId = str(session['loginId'])
                complaintDict = complaintDAO.getComplaintData(complaintVO)
                print('complaintDict: {}'.format(complaintDict))

                # Total Branches, Employees , Issued Cheques
                branchVO = BranchVO()
                branchDAO = BranchDAO()
                branchVO.branch_BankId = str(bankId)
                totalBranchesDict = branchDAO.getBankBranches(branchVO)

                staffVO = StaffVO()
                staffDAO = StaffDAO()
                staffVO.staff_BankId = str(bankId)
                totalEmployeesDict = staffDAO.getBankEmployees(staffVO)

                chequeDAO = ChequeDAO()
                chequeVO = ChequeVO()
                chequeVO.cheque_FromBankId = str(bankId)
                totalChequesDict = chequeDAO.getIssuedCheques(chequeVO)

                mainDisplayDict = {}
                mainDisplayDict.update(totalBranchesDict)
                mainDisplayDict.update(totalEmployeesDict)
                mainDisplayDict.update(totalChequesDict)
                print(mainDisplayDict)

                return render_template('bank/index.html',complaintDict=complaintDict, mainDisplayDict=mainDisplayDict)

    elif (loginDict[0]['loginRole'] == 'cashier'):

                # Storing loginEmail & Password in Session
                session['loginId'] = loginDict[0]['loginId']
                session['loginRole'] = loginDict[0]['loginRole']
                staffVO = StaffVO()
                staffDAO = StaffDAO()
                staffVO.staff_LoginId = str(session['loginId'])
                staffIdDict = staffDAO.getStaffIds(staffVO)
                print(staffIdDict)
                staffId = staffIdDict[0]['staffId']
                staff_BankId = staffIdDict[0]['staff_BankId']
                staff_BranchId = staffIdDict[0]['staff_BranchId']
                bank_LoginId = staffIdDict[0]['bank_LoginId']
                print(staffId)
                session['staffId'] = staffId
                session['staff_BankId'] = staff_BankId  # For cheque
                session['staff_BranchId'] = staff_BranchId
                session['bank_LoginId'] = bank_LoginId # Not needed

                # For display on index page
                chequeDAO = ChequeDAO()
                chequeVO = ChequeVO()
                chequeVO.cheque_StaffId = str(staffId)
                chequeDict = chequeDAO.StaffGetIssuedCheques(chequeVO)

                # branchVO = BranchVO()
                # branchDAO = BranchDAO()
                # branchVO.branchId = str(session['loginId'])
                # branchdata = branchDAO.getBranchId(branchVO)
                # branchId = branchdata[0]

                # return redirect(url_for(checkLogin), msg = 'You are not admin...!!!')
                return render_template('staff/index.html', chequeDict=chequeDict)

@app.route('/indexpage', methods=['get'])
def indexpage():

    loginDAO = LoginDAO()
    loginVO = LoginVO()

    if session['loginRole'] == 'admin':
        complaintDAO = ComplaintDAO()
        complaintVO = ComplaintVO()
        complaintVO.complaintTo_LoginId = str(session['loginId'])
        complaintDict = complaintDAO.getComplaintData(complaintVO)
        print('complaintDict: {}'.format(complaintDict))

        chequeDAO = ChequeDAO()
        chequeVO = ChequeVO()
        chequeDict = chequeDAO.getChequeData()
        print('chequeDict: {}'.format(chequeDict))

        return render_template('admin/index.html', complaintDict=complaintDict, chequeDict=chequeDict)

    elif session['loginRole'] == 'bank':
        bankVO = BankVO()
        # bankVO.bankId = str(session['loginId'])
        bankDAO = BankDAO()
        # bankdata = bankDAO.getBankId(bankVO)
        loginVO.loginId = str(session['loginId'])
        bankId = bankDAO.getBankId(loginVO)
        print("+++++++++++++++++++++++++BANKDATA+++++++++++++++++++++++++++++++++++")
        print(bankId)
        bankId = bankId[0]['bankId']
        print(bankId)
        session['bankId'] = bankId

        complaintDAO = ComplaintDAO()
        complaintVO = ComplaintVO()
        complaintVO.complaintTo_LoginId = str(session['loginId'])
        complaintDict = complaintDAO.getComplaintData(complaintVO)
        print('complaintDict: {}'.format(complaintDict))

        # Total Branches, Employees , Issued Cheques
        branchVO = BranchVO()
        branchDAO = BranchDAO()
        branchVO.branch_BankId = str(bankId)
        totalBranchesDict = branchDAO.getBankBranches(branchVO)

        staffVO = StaffVO()
        staffDAO = StaffDAO()
        staffVO.staff_BankId = str(bankId)
        totalEmployeesDict = staffDAO.getBankEmployees(staffVO)

        chequeDAO = ChequeDAO()
        chequeVO = ChequeVO()
        chequeVO.cheque_FromBankId = str(bankId)
        totalChequesDict = chequeDAO.getIssuedCheques(chequeVO)

        mainDisplayDict = {}
        mainDisplayDict.update(totalBranchesDict)
        mainDisplayDict.update(totalEmployeesDict)
        mainDisplayDict.update(totalChequesDict)
        print(mainDisplayDict)

        return render_template('bank/index.html', complaintDict=complaintDict, mainDisplayDict=mainDisplayDict)


    elif session['loginRole'] == 'cashier':
        staffVO = StaffVO()
        staffDAO = StaffDAO()
        staffVO.staff_LoginId = str(session['loginId'])
        staffIdDict = staffDAO.getStaffIds(staffVO)
        print(staffIdDict)
        staffId = staffIdDict[0]['staffId']
        staff_BankId = staffIdDict[0]['staff_BankId']
        staff_BranchId = staffIdDict[0]['staff_BranchId']
        bank_LoginId = staffIdDict[0]['bank_LoginId']
        print(staffId)
        session['staffId'] = staffId
        session['staff_BankId'] = staff_BankId  # For cheque
        session['staff_BranchId'] = staff_BranchId
        session['bank_LoginId'] = bank_LoginId  # Not needed

        # For display on index page
        chequeDAO = ChequeDAO()
        chequeVO = ChequeVO()
        chequeVO.cheque_StaffId = str(staffId)
        chequeDict = chequeDAO.StaffGetIssuedCheques(chequeVO)

        # branchVO = BranchVO()
        # branchDAO = BranchDAO()
        # branchVO.branchId = str(session['loginId'])
        # branchdata = branchDAO.getBranchId(branchVO)
        # branchId = branchdata[0]

        # return redirect(url_for(checkLogin), msg = 'You are not admin...!!!')
        return render_template('staff/index.html', chequeDict=chequeDict)




@app.route('/logout', methods=['get'])
def logout():

    # Clearing session
    session.clear()
    return render_template('admin/login.html')


