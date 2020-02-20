from project import app
from flask import render_template, redirect, request, url_for, session, flash
from project.com.dao.StaffDAO import StaffDAO
from project.com.vo.StaffVO import StaffVO
from project.com.dao.CityDAO import CityDAO     # For access of City
from project.com.dao.AreaDAO import AreaDAO     # For access of Area
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.BankVO import BankVO
from project.com.dao.BankDAO import BankDAO
from project.com.dao.BranchDAO import BranchDAO
from project.com.vo.BranchVO import BranchVO
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

@app.route('/loadStaff')
def loadStaff():
    if session['loginRole'] != 'bank':
        return render_template('admin/login.html')

    print('======================In /loadStaff=============================')
    cityDAO = CityDAO()
    cityDict = cityDAO.viewCity()

    areaDAO = AreaDAO()
    areaDict = areaDAO.viewArea()

    bankDAO = BankDAO()
    bankDict = bankDAO.viewBank()

    bankVO = BankVO()
    bankVO.bankId = str(session['bankId'])

    branchDAO = BranchDAO()
    branchDict = branchDAO.viewBranch(bankVO)
    print("Branch DICT")
    print(branchDict)

    return render_template('bank/addStaff.html', cityDict=cityDict, bankDict=bankDict, branchDict=branchDict)

@app.route('/insertStaff', methods=['post'])
def insertStaff():
    if session['loginRole'] != 'bank':
        return render_template('admin/login.html')

    print('======================In /insertStaff=============================')

    staffVO = StaffVO()
    staffDAO = StaffDAO()
    loginVO = LoginVO()
    loginDAO = LoginDAO()

    try:

        staffVO.staffFirstName = request.form['staffFirstName']
        print(type(staffVO.staffFirstName))

        staffVO.staffLastName = request.form['staffLastName']
        print(type(staffVO.staffLastName))

        staffVO.staffGender = request.form['staffGender']
        print(type(staffVO.staffGender))

        staffVO.staffDateOfBirth = request.form['staffDateOfBirth']
        print(type(staffVO.staffDateOfBirth))

        staffVO.staffAddress = request.form['staffAddress']
        print(type(staffVO.staffAddress))

        staffVO.staff_CityId = str(request.form['staff_CityId'])
        print(type(staffVO.staff_CityId))

        staffVO.staff_AreaId = str(request.form['staff_AreaId'])
        print(type(staffVO.staff_AreaId))

        staffVO.staff_BranchId = str(request.form['staff_BranchId'])
        print(type(staffVO.staff_BranchId))

        staffVO.staffRole = request.form['staffRole']
        print(type(staffVO.staffRole))

        staffVO.staffContact = str(request.form['staffContact'])
        print(type(staffVO.staffContact))

        staffVO.staff_BankId = str(session['bankId'])
        print(type(staffVO.staff_BankId))

        loginVO.loginEmail = request.form['staffEmail']
        loginVO.loginRole = request.form['staffRole']

    except:

        flash("Please enter appropriate details...!!!")
        return redirect(url_for('loadStaff'))

    registerPassword = ''.join(
        (random.choice(string.ascii_letters + string.digits)) for x in range(8))  # Creating 8 Char dynamic Password
    # loginVO.loginEmail = request.form['staffEmail']
    loginVO.loginPassword = registerPassword
    # loginVO.loginRole = request.form['staffRole']
    print("LoginVO Complete")

    print("registerPassword=" + registerPassword)

    # staffVO.staffEmail = request.form['staffEmail']
    # print(type(staffVO.staffEmail))

    #bankid logic problem -->>loginId str(session['loginId'])

    # print(staffVO)
    try:
        fromaddr = "dummy814131@gmail.com"

        # testpy4321@gmail.com
        senderPassword = "ccs814131"
        toaddr = loginVO.loginEmail  # Bank Email here loginVO.loginEmail

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "PYTHON PASSWORD - STAFF"

        msg.attach(MIMEText(registerPassword, 'plain'))

        print('MIME Done')
        server = smtplib.SMTP("smtp.gmail.com", 587)
        # server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        print('Server Logged In 1')

        server.login(fromaddr, senderPassword)
        # server.login(fromaddr, senderPassword)
        print('Server Logged In 2')

        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)

        server.quit()
    except:
        flash('Password could not be send due to internet connectivity. Please, try after some time.')
        return redirect(url_for('loadStaff'))

    # first insert into loginmaster then staffmaster
    loginDAO.insertLogin(loginVO)

    staff_LoginId = loginDAO.getLoginId()
    print(staff_LoginId)
    staffVO.staff_LoginId = str(staff_LoginId[0]['MAX(loginId)'])

    staffDAO.insertStaff(staffVO)

    return redirect(url_for('loadStaff'))


@app.route('/viewStaff')
def viewStaff():

    if session['loginRole'] != 'bank':
        return render_template('admin/login.html')

    print('======================In /viewStaff=============================')

    staffVO = StaffVO()
    staffDAO = StaffDAO()
    staffVO.staff_BankId = str(session['bankId'])
    staffDict = staffDAO.viewStaff(staffVO)

    return render_template('bank/viewStaff.html', staffDict=staffDict)


@app.route('/deleteStaff', methods=['get'])
def deleteStaff():
    if session['loginRole'] != 'bank':
        return render_template('admin/login.html')

    print('======================In /deleteStaff=============================')

    staffVO = StaffVO()
    staffDAO = StaffDAO()

    staffVO.staffId = request.args.get('staffId')
    staffDAO.deleteStaff(staffVO)

    return redirect(url_for('viewStaff'))


# EDIT link url which fetches particular staffId and displays its information
@app.route('/editStaff', methods=['get'])
def editStaff():
    if session['loginRole'] != 'bank':
        return render_template('admin/login.html')

    print('======================In /editStaff=============================')

    cityDAO = CityDAO()
    cityDict = cityDAO.viewCity()

    areaDAO = AreaDAO()
    areaDict = areaDAO.viewArea()

    bankDAO = BankDAO()
    bankDict = bankDAO.viewBank()

    bankVO = BankVO()
    branchDAO = BranchDAO()
    bankVO.bankId = str(session['bankId'])
    branchDict = branchDAO.viewBranch(bankVO)
    print(branchDict)

    # branchDAO = BranchDAO()
    # branchDict = branchDAO.viewBranch(session[''])

    staffVO = StaffVO()
    staffDAO = StaffDAO()

    staffVO.staffId = request.args.get('staffId')
    staffDict = staffDAO.editStaff(staffVO)

    print(staffDict)

    return render_template('bank/editStaff.html', staffDict=staffDict, cityDict=cityDict, areaDict=areaDict, branchDict=branchDict, bankDict=bankDict)


@app.route('/updateStaff', methods=['post'])
def updateStaff():
    if session['loginRole'] != 'bank':
        return render_template('admin/login.html')

    print('======================In /updateStaff=============================')

    staffVO = StaffVO()
    staffDAO = StaffDAO()

    loginVO = LoginVO()
    loginDAO = LoginDAO()

    staffVO.staffId = request.form['staffId']

    staffVO.staffFirstName = request.form['staffFirstName']
    print(type(staffVO.staffFirstName))

    staffVO.staffLastName = request.form['staffLastName']
    print(type(staffVO.staffLastName))

    staffVO.staffGender = request.form['staffGender']
    print(type(staffVO.staffGender))

    staffVO.staffDateOfBirth = request.form['staffDateOfBirth']
    print(type(staffVO.staffDateOfBirth))

    staffVO.staffRole = request.form['staffRole']
    print(type(staffVO.staffRole))

    staffVO.staffAddress = request.form['staffAddress']
    print(type(staffVO.staffAddress))

    staffVO.staffContact = request.form['staffContact']
    print(type(staffVO.staffContact))

    staffVO.staff_CityId = request.form['staff_CityId']
    print(type(staffVO.staff_CityId))

    staffVO.staff_AreaId = request.form['staff_AreaId']
    print(type(staffVO.staff_AreaId))

    staffVO.staff_BranchId = request.form['staff_BranchId']
    print(type(staffVO.staff_BranchId))


    staffVO.staff_BankId = str(request.form['staff_BankId'])  # BankId can't be change so passes same as in database
    print(type(staffVO.staff_BankId))

    print('type done')
    # staffVO.staffEmail = request.form['staffEmail']
    # print(type(staffVO.staffEmail))

    # staffVO.staff_LoginId = request.form['staff_LoginId']
    loginVO.loginId = str(request.form['staff_LoginId'])
    loginVO.loginEmail = request.form['loginEmail'].strip()
    print(loginVO.loginId)
    print(loginVO.loginEmail)
    print('loginvo done')

    print('fetching complete')

    loginDAO.updateLoginEmail(loginVO)
    # loginDAO.updateLoginEmail(loginVO)
    print('login query done')
    staffDAO.updateStaff(staffVO)
    print('updatestaff query done')
    return redirect(url_for('viewStaff'))
