from project import app
from flask import render_template, redirect, request, url_for, session, flash
from project.com.vo.ComplaintVO import ComplaintVO
from project.com.dao.ComplaintDAO import ComplaintDAO
from project.com.dao.StaffDAO import StaffDAO
from project.com.vo.StaffVO import StaffVO
from project.com.dao.BranchDAO import BranchDAO
import datetime
from datetime import date
@app.route('/loadComplaint')
def loadComplaint():

    # if session['loginRole'] != 'admin':
    #     return render_template('admin/login.html')
    #
    # print('======================In /loadComplaint=============================')
    # return render_template('admin/viewbankComplaint.html')

    if session['loginRole'] == 'admin':
        print('======================In ADMIN /loadComplaint=============================')
        # complaintVO = ComplaintVO()
        complaintDAO = ComplaintDAO()
        complaintDict = complaintDAO.viewbankComplaint()

        return render_template('admin/viewbankComplaint.html', complaintDict = complaintDict)

    elif session['loginRole'] == 'bank':
        print('======================In BANK /loadComplaint=============================')
        complaintDAO = ComplaintDAO()
        complaintDict = complaintDAO.viewStaffComplaint()
        return render_template('bank/viewStaffComplaint.html', complaintDict = complaintDict)

    else:
        return render_template('admin/login.html')


@app.route('/postComplaint')
def postComplaint():

    if session['loginRole'] == 'bank':
        # branchDAO = BranchDAO()
        # branchDict = branchDAO.viewBranch()
        # print(branchDict)
        return render_template('bank/postComplaint.html')

    elif session['loginRole'] == 'cashier':
        # staffDAO = StaffDAO()
        # staffDict = staffDAO.viewStaff()

        return render_template('staff/postComplaint.html')

    else:
        return render_template('admin/login.html')


@app.route('/submitComplaint', methods=['post'])
def submitComplaint():

    # can be develop this code using if statement for complaintTO_LoginId
    if session['loginRole'] == 'bank':
        complaintVO = ComplaintVO()
        complaintDAO = ComplaintDAO()

        # complaintVO.complaintDate = str(datetime.datetime.now()) # Current Date & Time
        # print(complaintVO.complaintDate)
        complaintDate = date.today()

        # dd/mm/YY
        complaintVO.complaintDate = str(complaintDate.strftime("%Y/%m/%d"))

        complaintVO.complaintSubject = request.form['complaintSubject']
        complaintVO.complaintDescription = request.form['complaintDescription']
        adminLoginIds = complaintDAO.getAdminLoginID()

        # Ids = []
        # for i in range(len(adminLoginIds)):
        #     fetch = adminLoginIds[i]['loginId']
        #     Ids.append(fetch)
        # print(Ids)

        complaintVO.complaintTo_LoginId = str(adminLoginIds[0]['loginId'])  # Static because only one Admin ~~~~~~ BANK -->> ADMIN
        print(session['loginId'])
        complaintVO.complaintFrom_LoginId = str(session['loginId'])

        print(complaintVO)
        complaintDAO.insertComplaint(complaintVO)

        return redirect(url_for('postComplaint'))

    elif session['loginRole'] == 'cashier':
        complaintVO = ComplaintVO()
        complaintDAO = ComplaintDAO()
        complaintDate = date.today()

        # dd/mm/YY
        complaintVO.complaintDate = str(complaintDate.strftime("%Y/%m/%d"))

        complaintVO.complaintSubject = request.form['complaintSubject']
        complaintVO.complaintDescription = request.form['complaintDescription']

        staffDAO = StaffDAO()
        
        complaintVO.complaintTo_LoginId = str(session['bank_LoginId']) # need bank's loginId
        complaintVO.complaintFrom_LoginId = str(session['loginId'])

        print('Complaint to and from')
        print(complaintVO.complaintTo_LoginId)
        print(complaintVO.complaintFrom_LoginId)

        complaintDAO.insertComplaint(complaintVO)

        return redirect(url_for('postComplaint'))


    else:
        return render_template('admin/login.html')


@app.route('/viewComplaint')
def viewComplaint():
    complaintDAO = ComplaintDAO()
    complaintVO = ComplaintVO()
    complaintVO.complaintFrom_LoginId = str(session['loginId'])
    complaintDict = complaintDAO.viewComplaint(complaintVO)

    if session['loginRole'] == 'bank':
        return render_template('bank/viewComplaint.html',complaintDict = complaintDict)

    elif session['loginRole'] == 'cashier':
        return render_template('staff/viewComplaint.html',complaintDict = complaintDict)

    else:
        return render_template('admin/login.html')


@app.route('/deleteComplaint')
def deleteComplaint():

    if session['loginRole'] == 'bank':

        complaintDAO = ComplaintDAO()
        complaintVO = ComplaintVO()
        complaintVO.complaintId = request.args.get('complaintId')
        complaintDAO.deleteComplaint(complaintVO)

        return redirect(url_for('viewComplaint'))

    elif session['loginRole'] == 'cashier':

        complaintDAO = ComplaintDAO()
        complaintVO = ComplaintVO()
        complaintVO.complaintId = request.args.get('complaintId')
        complaintDAO.deleteComplaint(complaintVO)

        return redirect(url_for('viewComplaint'))


#EDIT link url which fetches particular complaintId and displays its information

@app.route('/editComplaint', methods=['get'])
def editComplaint():

    if session['loginRole'] == 'bank':
        complaintDAO = ComplaintDAO()
        complaintVO = ComplaintVO()
        complaintVO.complaintId = request.args.get('complaintId')
        complaintDict = complaintDAO.editComplaint(complaintVO)
        return render_template('bank/editComplaint.html', complaintDict = complaintDict)

    elif session['loginRole'] == 'cashier':
        complaintDAO = ComplaintDAO()
        complaintVO = ComplaintVO()
        complaintVO.complaintId = request.args.get('complaintId')
        complaintDict = complaintDAO.editComplaint(complaintVO)
        return render_template('staff/editComplaint.html', complaintDict=complaintDict)

    else:
        return render_template('admin/login.html')


@app.route('/updateComplaint', methods=['post'])
def updateComplaint():

    ######################################################################
    #complaint status -->> Replied can't update it -->>> Implement Pending -->>DONE OPTION WONT't BE GIVEN IN HTML PAGE
    ######################################################################

    if session['loginRole'] == 'bank':

        complaintDAO = ComplaintDAO()
        complaintVO = ComplaintVO()
        print('DAO/VO done')
        # Here "RECEIVER" is only one -->> Admin it won't be change for all banks ??

        complaintVO.complaintId = request.form['complaintId']
        complaintVO.complaintSubject = request.form['complaintSubject']
        complaintVO.complaintDescription = request.form['complaintDescription']
        print('Vo fetch done')
        complaintDAO.updateComplaint(complaintVO)
        print("UPDATE CONTRoleER DONE")
        return redirect(url_for('viewComplaint'))

    elif session['loginRole'] == 'cashier':
        complaintDAO = ComplaintDAO()
        complaintVO = ComplaintVO()
        print('DAO/VO done')

        complaintVO.complaintId = request.form['complaintId']
        complaintVO.complaintSubject = request.form['complaintSubject']
        complaintVO.complaintDescription = request.form['complaintDescription']
        print('Vo fetch done')
        complaintDAO.updateComplaint(complaintVO)
        print("UPDATE CONTROLLER DONE")
        return redirect(url_for('viewComplaint'))

    else:
        return render_template('admin/login.html')

@app.route('/replyComplaint', methods=['get'])
def replyComplaint():

    if session['loginRole'] == 'admin':
        print('ADMIN WILL  HERE')
        complaintDAO = ComplaintDAO()
        complaintVO = ComplaintVO()
        complaintVO.complaintId = request.args.get('complaintId')
        complaintDict = complaintDAO.replyComplaint(complaintVO)
        print(complaintDict)
        return render_template('admin/replyComplaint.html', complaintDict = complaintDict)

    elif session['loginRole'] == 'bank':
        print('BANK WILL  HERE')
        complaintDAO = ComplaintDAO()
        complaintVO = ComplaintVO()
        complaintVO.complaintId = request.args.get('complaintId')
        complaintDict = complaintDAO.replyComplaint(complaintVO)
        print(complaintDict)
        return render_template('bank/replyComplaint.html', complaintDict=complaintDict)

    else:
        print("OTHER")
        return render_template('admin/login.html')


# To submit reply to lower authorities -->> Admin, bank
@app.route('/submitReply', methods=['post'])
def submitReply():

    if session['loginRole'] == 'admin' or session['loginRole'] == 'bank':
        complaintDAO = ComplaintDAO()
        complaintVO = ComplaintVO()

        complaintVO.complaintId = request.form['complaintId']
        complaintVO.complaintReply = request.form['complaintReply']
        complaintVO.complaintStatus = 'replied'

        print('complaint vo here')
        print(complaintVO)
        complaintDAO.submitReply(complaintVO)
        return redirect(url_for('loadComplaint'))

    else:
        return render_template('admin/login.html')





# To view replies by higher authorities regardning posted complaints -->> bank, Staff(Cashier)
@app.route('/viewReply', methods=['get'])
def viewReply():

    complaintDAO = ComplaintDAO()
    complaintVO = ComplaintVO()

    complaintVO.complaintId = request.args.get('complaintId')

    complaintDict = complaintDAO.editComplaint(complaintVO)  # Here editComplaint() called as it brings Dict for complaint

    if session['loginRole'] == 'bank':
        return render_template('bank/viewReply.html', complaintDict = complaintDict)

    elif session['loginRole'] == 'cashier':
        return render_template('staff/viewReply.html', complaintDict=complaintDict)

    else:
        return render_template('admin/login.html')

