from project import app
from flask import render_template, redirect, request, url_for, session, flash
from project.com.dao.BankDAO import BankDAO
from project.com.vo.BankVO import BankVO
from project.com.dao.CityDAO import CityDAO  # For access of City
from project.com.dao.AreaDAO import AreaDAO  # For access of Area
from project.com.vo.AreaVO import AreaVO
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.LoginVO import LoginVO
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import json



@app.route('/loadBank')
def loadBank():
    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    print('======================In /loadBank=============================')
    cityDAO = CityDAO()
    cityDict = cityDAO.viewCity()
    # flash('message here')

    return render_template('admin/addBank.html', cityDict=cityDict, )  # Passing data of City & Area


@app.route('/insertBank', methods=['post'])
def insertBank():
    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    print('======================In /insertBank=============================')
    # Creating DAO/VO objects for Bank & Login
    bankVO = BankVO()
    bankDAO = BankDAO()
    loginVO = LoginVO()
    loginDAO = LoginDAO()

    print('DAO VO done')

    try:
        # Getting infromation from HTML form and storing it in VO objects
        bankVO.bankName = request.form['bankName']
        bankVO.bankCode = request.form['bankCode']
        bankVO.bankContact = request.form['bankContact']
        # bankVO.bankEmail = request.form['bankEmail']
        bankVO.bank_CityId = request.form['cityId']
        print('cityid done')
        bankVO.bank_AreaId = request.form['areaId']
        print('bankvo fetch done')

        loginVO.loginEmail = request.form['bankEmail']
        print("data=========", bankVO.bank_AreaId)


    except:
        print('in except')
        flash("Please enter appropriate details...!!!")
        return redirect(url_for('loadBank'))

    registerPassword = ''.join(
        (random.choice(string.ascii_letters + string.digits)) for x in range(8))  # Creating 8 Char dynamic Password
    # loginVO.loginEmail = request.form['bankEmail']
    loginVO.loginPassword = registerPassword
    loginVO.loginRole = 'bank'
    print("LoginVO Complete")

    print("registerPassword=" + registerPassword)

    try:
        fromaddr = "dummy814131@gmail.com"

        # testpy4321@gmail.com
        senderPassword = "ccs814131"
        toaddr = loginVO.loginEmail  # Bank Email here loginVO.loginEmail

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "PYTHON PASSWORD - BANK"
        message = 'Your password is: ' + registerPassword

        msg.attach(MIMEText(message, 'plain'))

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
        return redirect(url_for('loadBank'))

    loginDAO.insertLogin(loginVO)
    bank_LoginId = loginDAO.getLoginId()
    print("+++++++++bank_LoginId++++++++++")
    print(bank_LoginId)
    bankVO.bank_LoginId = str(bank_LoginId[0]['MAX(loginId)'])
    bankDAO.insertBank(bankVO)

    return redirect(url_for('loadBank'))


@app.route('/viewBank')
def viewBank():
    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    print('======================In /viewBank=============================')
    bankDAO = BankDAO()

    bankDict = bankDAO.viewBank()
    print(bankDict)

    return render_template('admin/viewBank.html', bankDict=bankDict)


@app.route('/deleteBank', methods=['get'])
def deleteBank():
    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    print('======================In /deleteBank=============================')
    # Creating DAO/VO objects for Bank
    bankVO = BankVO()
    bankDAO = BankDAO()

    bankVO.bankId = request.args.get('bankId')
    bankDAO.deleteBank(bankVO)

    return redirect(url_for('viewBank'))


# EDIT link url which fetches particular bankId and displays its information
@app.route('/editBank', methods=['get'])
def editBank():
    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    print('======================In /editBank=============================')
    # Creating DAO/VO objects for Bank, City, Area
    bankVO = BankVO()
    bankDAO = BankDAO()
    cityDAO = CityDAO()
    cityDict = cityDAO.viewCity()
    areaDAO = AreaDAO()
    areaDict = areaDAO.viewArea()

    bankVO.bankId = request.args.get('bankId')
    bankDict = bankDAO.editBank(bankVO)
    print(bankDict)

    return render_template('admin/editBank.html', bankDict=bankDict, cityDict=cityDict, areaDict=areaDict)


@app.route('/updateBank', methods=['post'])
def updateBank():
    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    print('======================In /updateBank=============================')
    # Creating DAO/VO objects for Bank, Login
    bankVO = BankVO()
    bankDAO = BankDAO()
    loginVO = LoginVO()
    loginDAO = LoginDAO()

    # Getting infromation from HTML form and storing it in VO objects
    bankVO.bankId = request.form['bankId']
    bankVO.bankName = request.form['bankName']
    bankVO.bankCode = request.form['bankCode']
    bankVO.bankContact = request.form['bankContact']
    # bankVO.bankEmail = request.form['loginEmail']
    bankVO.bank_CityId = request.form['bank_CityId']
    bankVO.bank_AreaId = request.form['bank_AreaId']

    loginVO.loginEmail = request.form['loginEmail']
    print('fetching complete')
    bankDAO.updateBank(bankVO, loginVO)

    return redirect(url_for('viewBank'))


@app.route('/ajaxLoadArea')
def ajaxLoadArea():
    print('load ajax')
    cityId = request.args.get('cityId')
    print(cityId)

    areaDAO = AreaDAO()
    areaVO = AreaVO()
    # print(cityId[1])

    areaVO.area_CityId = cityId
    # areaVO.area_CityId = str(cityId)

    areaDict = areaDAO.ajaxViewArea(areaVO)

    jsnAreaDict = json.dumps(areaDict)
    print('return json')
    print(jsnAreaDict)
    return jsnAreaDict

@app.route('/restrictDuplicateEmail')
def restrictDuplicateEmail():
    print('load loginemail ajax')
    loginEmail = request.args.get('loginEmail')
    print(loginEmail)

    loginDAO = LoginDAO()
    loginVO = LoginVO()
    # print(cityId[1])
    loginVO.loginEmail = loginEmail.strip()
    emailExistStatus = loginDAO.restrictDuplicateEmail(loginVO)
    print('emailExistStatus: {}'.format(emailExistStatus))

    # areaVO.area_CityId = str(cityId)

    # areaDict = areaDAO.ajaxViewArea(areaVO)

    jsnAreaDict = json.dumps(emailExistStatus)
    print('return json')
    print(jsnAreaDict)
    return jsnAreaDict