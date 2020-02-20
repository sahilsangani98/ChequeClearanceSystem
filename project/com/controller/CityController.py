from project import app
from flask import render_template, redirect, request, url_for, session
from project.com.dao.CityDAO import CityDAO
from project.com.vo.CityVO import CityVO
from flask import jsonify

@app.route('/')
def loadAdminIndex():

    return render_template('admin/login.html')
    # return render_template('admin/index.html')



@app.route('/loadCity')
def loadCity():

    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    return render_template('admin/addCity.html')


@app.route('/insertCity', methods=['POST'])
def insertCity():

    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    # Creating objects of CityVO and CityDAO
    cityDAO = CityDAO()
    cityVO = CityVO()

    #Getting infromation from HTML form and storing it in VO objects
    cityName = request.form['cityName'].strip()
    cityDescription = request.form['cityDescription'].strip()

    cityVO.cityName = cityName
    cityVO.cityDescription = cityDescription

    #After VO validation pass VO object to DAO
    cityDAO.insertCity(cityVO)

    return redirect(url_for('loadCity'))


@app.route('/viewCity')
def viewCity():

    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    # Creating object of CityDAO
    cityDAO = CityDAO()

    cityDict = cityDAO.viewCity()

    print(cityDict)

    return render_template('admin/viewCity.html',cityDict=cityDict)


@app.route('/deleteCity', methods=['get'])
def deleteCity():

    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    print('Delete City')
    # Creating objects of CityVO and CityDAO
    cityDAO = CityDAO()
    cityVO = CityVO()

    cityVO.cityId = request.args.get('cityId')
    cityDict =cityDAO.deleteCity(cityVO)
    return redirect(url_for('viewCity'))



#EDIT link url which fetches particular cityId and displays its information

@app.route('/editCity', methods=['get'])
def editCity():

    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    # Creating objects of CityVO and CityDAO
    cityDAO = CityDAO()

    cityVO = CityVO()

    cityVO.cityId = request.args.get('cityId')

    cityDict = cityDAO.editCity(cityVO)

    return render_template('admin/editCity.html', cityDict=cityDict)


#After changing in 'editCity.html' it will updates database

@app.route('/updateCity', methods=['post'])
def updateCity():

    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')

    # Creating objects of CityVO and CityDAO
    cityDAO = CityDAO()
    cityVO = CityVO()

    cityName = request.form['cityName']

    cityDescription = request.form['cityDescription'].strip()

    cityId = request.form['cityId']

    cityVO.cityName = cityName
    cityVO.cityDescription = cityDescription
    cityVO.cityId = cityId

    cityDAO.updateCity(cityVO)
    print('update FINISH')

    return redirect(url_for('viewCity'))

# @app.route('/change_area_according_to_city', methods=['post'])
# def change_area_according_to_city():
#
#    selected_city = request.form['selected_city'].strip()
#
#    cityVO = CityVO()
#    cityDAO = CityDAO()
#
#    cityVO.cityName = selected_city
#    newAreaDict =  cityDAO.change_area_according_to_city(cityVO)
#
#    # print(newAreaDict)
#    # print(type(newAreaDict))
#
#    return jsonify({"newAreaDict": newAreaDict})


