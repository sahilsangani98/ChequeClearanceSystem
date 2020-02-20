from project import app
from flask import render_template, redirect, request, url_for, session
from project.com.dao.CityDAO import CityDAO
from project.com.dao.AreaDAO import AreaDAO
from project.com.vo.AreaVO import AreaVO
import json

@app.route('/loadArea')
def loadArea():

    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    cityDAO = CityDAO()
    cityDict = cityDAO.viewCity()

    return render_template('admin/addArea.html', cityDict = cityDict)


@app.route('/insertArea', methods=['post'])
def insertArea():

    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    # Creating objects of AreaVO and AreaDAO
    areaDAO = AreaDAO()
    areaVO = AreaVO()
    #Fetching details from the html page
    areaVO.area_CityId = request.form['cityId']
    print('cityId')
    areaVO.areaName = request.form['areaName'].strip()
    print('areaname')
    areaVO.areaDescription = request.form['areaDescription'].strip()
    print('area description')
    areaDAO.insertArea(areaVO)

    return redirect(url_for('loadArea'))


@app.route('/viewArea')
def viewArea():

    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    #Creating object of areaDAO to fetch data from the areamaster table
    areaDAO = AreaDAO()
    areaDict = areaDAO.viewArea()
    print(areaDict)
    return render_template('admin/viewArea.html', areaDict = areaDict)


@app.route('/deleteArea',methods=['get'])
def deleteArea():

    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    print("Routing /deletearea")

    areaDAO = AreaDAO()
    areaVO = AreaVO()

    areaVO.areaId = request.args.get('areaId')

    areaDAO.deleteArea(areaVO)

    return redirect(url_for('viewArea'))


@app.route('/editArea',methods=['get'])
def editArea():

    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    print('==========Route in Edit Area=============')
    # Creating objects of AreaVO and AreaDAO
    areaDAO = AreaDAO()
    areaVO = AreaVO()
    cityDAO =CityDAO()

    # Fetching details from the html page
    areaVO.areaId = request.args.get('areaId')

    cityDict = cityDAO.viewCity() # Retrives City names and passes it to editArea.html
    areaDict = areaDAO.editArea(areaVO)
    return render_template('admin/editArea.html', cityDict=cityDict, areaDict=areaDict)


@app.route('/updateArea', methods=['post'])
def updateArea():

    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    print("Routing /updateArea")

    areaDAO = AreaDAO()
    areaVO = AreaVO()
    print("Objects Created")

    areaVO.area_CityId = request.form['cityId']
    areaVO.areaName = request.form['areaName'].strip()
    areaVO.areaDescription = request.form['areaDescription'].strip()
    areaVO.areaId = request.form['areaId']
    print("VO Done")
    areaDAO.updateArea(areaVO)
    print('Routing Update Area Complete')
    return redirect(url_for('viewArea'))


