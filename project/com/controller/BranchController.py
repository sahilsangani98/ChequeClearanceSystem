from project import app
from flask import render_template, redirect, request, url_for, session, flash
from project.com.dao.BranchDAO import BranchDAO
from project.com.vo.BranchVO import BranchVO
from project.com.dao.CityDAO import CityDAO     # For access of City
from project.com.dao.AreaDAO import AreaDAO     # For access of Area
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.BankVO import BankVO
from project.com.dao.BankDAO import BankDAO
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

@app.route('/loadBranch')
def loadBranch():

    if session['loginRole'] != 'bank':
        return render_template('admin/login.html')

    print('======================In /loadBranch=============================')
    cityDAO = CityDAO()
    cityDict = cityDAO.viewCity()
    areaDAO = AreaDAO()
    areaDict = areaDAO.viewArea()
    print("location done")

    #------>>> bankId stored in session

    # # Find particular bank's data -- add that query in bankcontRoleer & DAO
    # bankDAO = BankDAO()
    # bankDict = bankDAO.viewBank()
    # print("bank dict")
    # print(bankDict)

    return render_template('bank/addBranch.html', cityDict=cityDict, areaDict=areaDict)


@app.route('/insertBranch', methods=['post'])
def insertBranch():
    if session['loginRole'] != 'bank':
        return render_template('admin/login.html')

    print('======================In /insertBranch=============================')
    # Creating DAO/VO objects for Branch & Login
    branchVO = BranchVO()
    branchDAO = BranchDAO()

    loginVO = LoginVO()
    loginDAO = LoginDAO()

    try:

        # Getting infromation from HTML form and storing it in VO objects
        branchVO.branchName = request.form['branchName']
        branchVO.branchIFSCCode = request.form['branchIFSCCode']
        branchVO.branchContact = request.form['branchContact']
        branchVO.branchEmail = request.form['branchEmail']
        branchVO.branch_CityId = request.form['cityId']
        branchVO.branch_AreaId = request.form['areaId']


        # ==================================================================================================================
        # ==================================================================================================================
        branchVO.branch_BankId = session['bankId']
        # ==================================================================================================================
        # ==================================================================================================================
        # print(branchVO.branchName)
        # print(branchVO.branchIFSCCode)
        # print(branchVO.branchContact)
        # print(branchVO.branchEmail)
        # print(branchVO.branch_CityId)
        # print(branchVO.branch_AreaId)
        # print(branchVO.branch_BankId)
    except:
        print('in except')
        flash("Please enter appropriate details...!!!")
        return redirect(url_for('loadBranch'))

    # registerPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))  # Creating 8 Char dynamic Password
    # # Password = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
    # loginVO.loginUsername = request.form['branchEmail']
    # loginVO.loginPassword = registerPassword
    # loginVO.loginRole = 'user'
    # print("LoginVO Complete")
    # print("registerPassword=" + registerPassword)
    # BRANCH DOES NOT HAVE LOGIN CAPABILITIES
    # fromaddr = "testpy4321@gmail.com"
    #
    # # testpy4321@gmail.com
    # senderPassword = "test@0101"
    # toaddr = loginVO.loginUsername  # Bank Email here loginVO.loginUsername
    #
    # msg = MIMEMultipart()
    # msg['From'] = fromaddr
    # msg['To'] = toaddr
    # msg['Subject'] = "PYTHON PASSWORD - Branch/Staff"
    #
    # msg.attach(MIMEText(registerPassword, 'plain'))
    #
    # print('MIME Done')
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    #
    # server.starttls()
    # print('Server Logged In 1')
    #
    # server.login(fromaddr, senderPassword)
    #
    # print('Server Logged In 2')
    #
    # text = msg.as_string()
    # server.sendmail(fromaddr, toaddr, text)
    #
    # server.quit()
    # bankDAO.insertBank(bankVO)
    branchDAO.insertBranch(branchVO)
    # loginDAO.insertLogin(loginVO)

    return redirect(url_for('loadBranch'))

@app.route('/viewBranch')
def viewBranch():

    if session['loginRole'] != 'bank':
        return render_template('admin/login.html')

    print('======================In /viewBranch=============================')
    bankVO = BankVO()
    # branchVO = BranchVO()
    branchDAO = BranchDAO()


    # branchVO.branch_BankId = str(session['bankId'])

    bankVO.bankId = str(session['bankId'])
    # branchDict = branchDAO.viewBranch(branchVO)
    branchDict = branchDAO.viewBranch(bankVO)
    print(branchDict)

    return render_template('bank/viewBranch.html', branchDict=branchDict)

@app.route('/deleteBranch', methods=['get'])
def deleteBranch():
    if session['loginRole'] != 'bank':
        return render_template('admin/login.html')

    print('======================In /deleteBranch=============================')
    # Creating DAO/VO objects for Branch
    branchVO = BranchVO()
    branchDAO = BranchDAO()

    branchVO.branchId = request.args.get('branchId')
    branchDAO.deleteBranch(branchVO)

    return redirect(url_for('viewBranch'))

# EDIT link url which fetches particular branchId and displays its information
@app.route('/editBranch', methods=['get'])
def editBranch():
    if session['loginRole'] != 'bank':
        return render_template('admin/login.html')

    print('======================In /editBranch=============================')
    # Creating DAO/VO objects for Branch
    branchVO = BranchVO()
    branchDAO = BranchDAO()
    cityDAO = CityDAO()
    cityDict = cityDAO.viewCity()
    areaDAO = AreaDAO()
    areaDict = areaDAO.viewArea()

    branchVO.branchId = request.args.get('branchId')
    branchDict = branchDAO.editBranch(branchVO)
    print(branchDict)
    return render_template('bank/editBranch.html', branchDict=branchDict, cityDict=cityDict, areaDict=areaDict)

@app.route('/updateBranch', methods=['post'])
def updateBranch():
    if session['loginRole'] != 'bank':
        return render_template('admin/login.html')

    print('======================In /updateBranch=============================')
    # Creating DAO/VO objects for Branch
    branchVO = BranchVO()
    branchDAO = BranchDAO()

    # Getting infromation from HTML form and storing it in VO objects
    branchVO.branchId = request.form['branchId']
    branchVO.branchName = request.form['branchName']
    branchVO.branchIFSCCode = request.form['branchIFSCCode']
    branchVO.branchContact = request.form['branchContact']
    branchVO.branchEmail = request.form['branchEmail']
    branchVO.branch_CityId = request.form['branch_CityId']
    branchVO.branch_AreaId = request.form['branch_AreaId']
    branchVO.branch_BankId = request.form['branch_BankId']

    print(branchVO.branchId)
    print(type(branchVO.branchId))

    print(branchVO.branchName)
    print(type(branchVO.branchName))

    print(branchVO.branchIFSCCode)
    print(type(branchVO.branchIFSCCode))

    print(branchVO.branchContact)
    print(type(branchVO.branchContact))

    print(branchVO.branchEmail)
    print(type(branchVO.branchEmail))

    print(branchVO.branch_CityId)
    print(type(branchVO.branch_CityId))

    print(branchVO.branch_AreaId)
    print(type(branchVO.branch_AreaId))

    print(branchVO.branch_BankId)
    print(type(branchVO.branch_BankId))

    # print(branchVO.branchName)
    # print(branchVO.branchIFSCCode)
    # print(branchVO.branchContact)
    # print(branchVO.branchEmail)
    # print(branchVO.branch_CityId)
    # print(branchVO.branch_AreaId)
    # print(branchVO.branch_BankId)

    print('fetching complete')

    branchDAO.updateBranch(branchVO)

    return redirect(url_for('viewBranch'))
