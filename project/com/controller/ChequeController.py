import io
import json
import os

import cv2
from flask import render_template, session, request, url_for, redirect
from google.cloud import vision
from google.cloud.translate_v2 import Client
from google.cloud.vision import types

from project import app
from project.com.dao.BankDAO import BankDAO
from project.com.vo.BankVO import BankVO

from project.com.vo.ChequeVO import ChequeVO
from project.com.dao.ChequeDAO import ChequeDAO

from werkzeug.utils import secure_filename
import os
import shutil

from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt


# as requested in comment


def get_cropped_images_of_SBI(chequeName):
    print('In get_cropped_images_of_SBI()')

    img = cv2.imread(
        "/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/{}".format(
            chequeName))

    # img = cv2.imread("finaltest9.jpg")

    image = img[301:460, 301:2857]
    crop_name = image_resize(image, height=25, width=500)
    # cv2.imshow("cropped", crop_name)

    image = img[481:625, 570:3569]
    crop_ammout_in_words = image_resize(image, height=278, width=706)
    # cv2.imshow("cropped", crop_ammout_in_words)

    image = img[621:769, 2829:3561]
    crop_ammout_in_digit = image_resize(image, height=51, width=260)
    # cv2.imshow("cropped", crop_ammout_in_digit)

    image = img[141:233, 2809:3561]
    crop_date = image_resize(image, height=37, width=274)
    # cv2.imshow("cropped", crop_date)

    image = img[825:965, 345:1481]
    crop_account_number = image_resize(image, height=278, width=706)
    # cv2.imshow("cropped", crop_account_number)

    image = img[233:277, 1941:2193]
    crop_IFS_code = image_resize(image, height=278, width=706)
    # cv2.imshow("cropped", crop_IFS_code)

    image = img[1437:1689, 845:2761]
    crop_cheque_number = image_resize(image, height=278, width=706)
    # cv2.imshow("cropped", crop_cheque_number)

    image = img[950:1177, 2573:3461]
    crop_signature = image_resize(image, height=278, width=706)
    # cv2.imshow("cropped", crop_signature)

    cropped_images = [crop_name, crop_ammout_in_words, crop_ammout_in_digit,
                      crop_date, crop_account_number, crop_IFS_code, crop_cheque_number, crop_signature]
    print('done get_cropped_images_of_SBI()')

    return cropped_images


def get_cropped_images_of_BOB(chequeName):
    # img = cv2.imread("finaltest9.jpg")

    img = cv2.imread(
        "/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/{}".format(
            chequeName))

    # img = cv2.imread("sangani_cheque.jpg")

    image = img[389:541, 333:3529]
    crop_name = image_resize(image, height=25, width=500)
    # cv2.imshow("cropped", crop_name)
    # cv2.waitKey(0)

    image = img[549:697, 617:3417]
    crop_ammout_in_words = image_resize(image, height=278, width=706)
    # cv2.imshow("cropped", crop_ammout_in_words)
    # cv2.waitKey(0)

    image = img[721:865, 3117:3813]
    crop_ammout_in_digit = image_resize(image, height=51, width=260)
    # cv2.imshow("cropped", crop_ammout_in_digit)
    # cv2.waitKey(0)

    image = img[188:331, 3058:3846]
    crop_date = image_resize(image, height=37, width=274)
    # cv2.imshow("cropped", crop_date)
    # cv2.waitKey(0)

    image = img[925:1049, 553:1529]
    crop_account_number = image_resize(image, height=278, width=706)
    # cv2.imshow("cropped", crop_account_number)

    image = img[213:269, 1761:2117]
    crop_IFS_code = image_resize(image, height=278, width=706)
    # cv2.imshow("cropped", crop_IFS_code)

    image = img[1589:1773, 845:3089]
    crop_cheque_number = image_resize(image, height=278, width=706)
    # cv2.imshow("cropped", crop_cheque_number)

    image = img[917:1297, 2989:3841]
    crop_signature = image_resize(image, height=278, width=706)
    # cv2.imshow("cropped", crop_signature)
    # cv2.waitKey(0)

    cropped_images = [crop_name, crop_ammout_in_words, crop_ammout_in_digit,
                      crop_date, crop_account_number, crop_IFS_code, crop_cheque_number, crop_signature]

    return cropped_images


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def detect_text(path):
    a = []
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)

    texts = response.text_annotations

    for text in texts:
        a.append("{}".format(text.description))

    try:

        return a[0]

    except:

        return None


# f = open('userdetails.txt', mode='w+')

os.environ[
    'GOOGLE_APPLICATION_CREDENTIALS'] = r'/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/jsonfile.json'

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'jsonfile.json'

bq_client = Client()


@app.route('/chequeDetection')
def detect():
    chequeName = request.args.get('chequeName')
    cheque_BankId = request.args.get('bankId')

    print('cheque Name is: {}'.format(chequeName))
    print('cheque_BankId is: {}'.format(cheque_BankId))

    bankVO = BankVO()
    bankDAO = BankDAO()

    bankVO.bankId = str(cheque_BankId)

    bankNameDict = bankDAO.getBankName(bankVO)
    bankName = bankNameDict[0]['bankName'].strip()
    print('bank name is: {}'.format(bankName))

    if bankName == 'BOB':
        cropped_images = get_cropped_images_of_BOB(chequeName)
        # path = r'/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/chequeimages/BOB/'

    elif bankName == 'SBI':
        cropped_images = get_cropped_images_of_SBI(chequeName)
        # path = r'/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/chequeimages/SBI/'

    userdetails = []
    userdetails_dict = {}

    path = r'/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/chequeimages/'
    # path = r'/Users/sahil/PycharmProjects/Final_AI-2/chequeimages/'
    # path = r'C:\Users\User\PycharmProjects\Final_AI\chequeimages'

    cropped_images_name = ["crop_name", "crop_ammout_in_words", "crop_ammout_in_digit",
                           "crop_date", "crop_account_number", "crop_IFS_code", "crop_cheque_number", "crop_signature"]

    f = open('userdetails.txt', mode='w+')

    for image, image_name in zip(cropped_images, cropped_images_name):

        cv2.imwrite(os.path.join(path, '{}.jpg'.format(image_name)), image)

        if image_name != "crop_signature":
            ocr_path = path + '/' + image_name

            userdetail = detect_text(r"{}.jpg".format(ocr_path))

            userdetails.append(userdetail)

    userdetails_dict = {"{}".format(cropped_images_name[0]): userdetails[0],
                        "{}".format(cropped_images_name[1]): userdetails[1],
                        "{}".format(cropped_images_name[2]): userdetails[2],
                        "{}".format(cropped_images_name[3]): userdetails[3],
                        "{}".format(cropped_images_name[4]): userdetails[4],
                        "{}".format(cropped_images_name[5]): userdetails[5],
                        "{}".format(cropped_images_name[6]): userdetails[6]}

    f.write(json.dumps(userdetails_dict))

    f.close()

    print('file closed')

    with open("userdetails.txt", "r") as fobject:
        content = fobject.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    readData = []

    userdetails_dict = json.loads(content[0])

    # Findinf only PaytoAccountNumber
    s1 = userdetails_dict['crop_name']
    s2 = 'A/C No.'
    s3 = s1[s1.index(s2) + len(s2):]
    # print(s3.strip())
    chequePayTo = s3.replace(' ', '')
    print('A/C No.')
    print(chequePayTo.strip())

    readData.append(chequePayTo.strip())

    print('Name')
    accName = s1 = s1[:s1.rfind("A/C No")]
    print(accName)
    # crop_name = userdetails_dict['crop_name']
    # print(crop_name)
    readData.append(accName.strip())

    print('Amount in words')
    crop_ammout_in_words = userdetails_dict['crop_ammout_in_words']
    print(crop_ammout_in_words)
    readData.append(crop_ammout_in_words.strip())

    print('Amount in digit')
    crop_ammout_in_digit = userdetails_dict['crop_ammout_in_digit']
    print(crop_ammout_in_digit)
    readData.append(crop_ammout_in_digit)

    print('Date')
    cd = userdetails_dict['crop_date']
    s1 = cd.replace(' ', '')
    # crop_date = userdetails_dict['crop_date']
    # print(crop_date)
    print(s1)
    # ans = stringToDate(cd2)

    print('date format')
    chequeDate1 = s1[:2] + '-' + s1[2:4] + '-' + s1[4:]
    newDate = chequeDate1.split('-')
    chequeDate = str(newDate[2]) + '-' + str(newDate[1]) + '-' + str(newDate[0])
    # s2 = s1[:-1] + '-' + s1[-3:-5] + '-' + s1[:-3]
    print(chequeDate)
    readData.append(chequeDate.strip())

    print('Account Number')
    chequePayFrom = userdetails_dict['crop_account_number']
    print(chequePayFrom)
    readData.append(chequePayFrom.strip())

    print('IFS code')
    chequeIFSCCode = userdetails_dict['crop_IFS_code']
    print(chequeIFSCCode)
    readData.append(chequeIFSCCode.strip())

    print('Cheque Number')
    chequeNumber = userdetails_dict['crop_cheque_number']
    print(chequeNumber)
    readKey = ['chequePayTo', 'accName', 'crop_ammout_in_words', 'crop_ammout_in_digit', 'chequeDate', 'chequePayFrom',
               'chequeIFSCCode', 'chequeNumber', 'SignImage']
    readData.append(chequeNumber)
    # readData.append(cropped_images[7])

    # if bankName == 'BOB':
    #
    #     readData.append('BOB/crop_signature.jpg')
    #     # readData.append('/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/chequeimages/BOB/crop_signature.jpg')
    #
    # elif bankName == 'SBI':
    #     readData.append('SBI/crop_signature.jpg')
    # readData.append('/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/chequeimages/SBI/crop_signature.jpg')

    readData.append('crop_signature.jpg')

    readDict = dict(zip(readKey, readData))
    print('readDict: {}'.format(readDict))
    print('readDataList: {}'.format(readData))
    # return "readData : {}".format(readData)

    # return "readDict : {}".format(readDict)

    # readSignImage = {'SignImage' : 'crop_signature'}

    jsnreadDict = json.dumps(readDict)

    print('jsnreadDict: {}'.format(jsnreadDict))
    return jsnreadDict


@app.route('/loadCheques')
def loadCheques():
    if session['loginRole'] != 'cashier':
        return render_template('admin/login.html')

    print('======================In /loadCheques=============================')
    bankDAO = BankDAO()
    bankDict = bankDAO.viewBank()

    return render_template('staff/uploadCheque.html', bankDict=bankDict)


@app.route('/uploadChequeDetails', methods=['post'])
def uploadChequeDetails():
    if session['loginRole'] != 'cashier':
        return render_template('admin/login.html')
    print('======================In /uploadChequeDetails=============================')
    chequeVO = ChequeVO()
    chequeDAO = ChequeDAO()

    chequeVO.cheque_FromBankId = request.form['cheque_FromBankId']
    chequeVO.cheque_ToBankId = str(session['staff_BankId'])
    chequeVO.cheque_StaffId = str(session['staffId'])
    chequeVO.chequeNumber = request.form['chequeNumber']
    chequeVO.chequeDate = request.form['chequeDate']
    chequeVO.chequePayTo = request.form['chequePayTo']
    chequeVO.chequePayFrom = request.form['chequePayFrom']
    chequeVO.chequeAmount = request.form['chequeAmount']
    chequeVO.chequeIFSCCode = request.form['chequeIFSCCode']

    print('cheque_FromBankId: {}'.format(chequeVO.cheque_FromBankId))
    print('cheque_ToBankId: {}'.format(chequeVO.cheque_ToBankId))
    print('cheque_StaffId: {}'.format(chequeVO.cheque_StaffId))
    print('chequeNumber: {}'.format(chequeVO.chequeNumber))
    print('chequeDate: {}'.format(chequeVO.chequeDate))
    print('chequePayTo: {}'.format(chequeVO.chequePayTo))
    print('chequePayFrom: {}'.format(chequeVO.chequePayFrom))
    print('chequeAmount: {}'.format(chequeVO.chequeAmount))
    print('chequeIFSCCode: {}'.format(chequeVO.chequeIFSCCode))

    filename = request.form['SignImageName']

    filepath = "/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/chequeimages/"

    print(filename)

    print('file signimage done')

    print('Cheque  Fetching Done')

    chequeVO.chequeSignImageName = filename
    chequeVO.chequeSignImagePath = filepath

    chequeDAO.insertChequeDetails(chequeVO)
    print('Cheque insert done')

    lastchequeIdDict = chequeDAO.lastChequeId()
    lastchequeId = lastchequeIdDict[0]['MAX(chequeId)']
    print('lastchequeId: {}'.format(lastchequeId))

    # ===================================================================================================================
    # ===================================================================================================================

    # Cheque Sign Upload into admin folder

    source_fileName = "/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/chequeimages/crop_signature.jpg"

    destination_fileName = r'/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/adminResources/chequeSigns/'

    filename = str(lastchequeId)

    shutil.copy(source_fileName, destination_fileName)

    # changing sign image name

    print('filename rename done')

    # changing sign image name
    old_file = "/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/adminResources/chequeSigns/crop_signature.jpg"
    new_file = os.path.join(
        "/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/adminResources/chequeSigns/",
        str(lastchequeId) + '.jpg')

    os.rename(old_file, new_file)

    # Deleting all files which are fetched in staff side

    folder = '/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/chequeimages'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    # ===================================================================================================================
    # ===================================================================================================================


    return redirect(url_for('loadCheques'))


@app.route('/viewCheques')
def viewCheques():
    if session['loginRole'] == 'admin':
        print('======================In /viewCheques  FOR ADMIN=============================')

        chequeDAO = ChequeDAO()
        chequeDict = chequeDAO.viewChequeAdmin()
        return render_template('admin/viewCheque.html', chequeDict=chequeDict)

    if session['loginRole'] == 'cashier':
        print('======================In /viewCheques FOR CASHIER=============================')
        chequeVO = ChequeVO()
        chequeDAO = ChequeDAO()
        chequeVO.cheque_StaffId = str(session['staffId'])
        chequeDict = chequeDAO.viewCheque(chequeVO)
        return render_template('staff/viewCheque.html', chequeDict=chequeDict)

    else:
        return render_template('admin/login.html')


@app.route('/chequeValidate')
def chequeValidate():
    if session['loginRole'] != 'admin':
        return render_template('admin/login.html')
    print('======================In /chequeValidate=============================')
    chequeVO = ChequeVO()
    chequeDAO = ChequeDAO()
    chequeId = request.args.get('chequeId')

    chequeVO.chequeId = chequeId
    print('chequeid fetch')
    chequeDict = chequeDAO.viewChequeDetailsAdmin(chequeVO)
    print(chequeDict)

    chequePayFrom = chequeDict[0]['chequePayFrom']
    print('chequePayFrom: {}'.format(chequePayFrom))


    # chequeSignImagePath = str(chequeDict[0]['chequeSignImagePath']) + str(chequeDict[0]['chequeSignImageName'])

    chequeSignImagePath = "/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/adminResources/chequeSigns/" + str(chequeId) + str(".jpg")
    print('chequeSignImagePath: {}'.format(chequeSignImagePath))

    s = sign_compare(chequePayFrom, chequeSignImagePath)  # Sign compare logic

    print(s)
    print('sign_compare done')
    if s > 0.3:
        chequeVO.chequeStatus = 'Approved'
        chequeDAO.chequeValidateStatus(chequeVO)
    else:
        chequeVO.chequeStatus = 'Rejected'
        chequeDAO.chequeValidateStatus(chequeVO)

    return redirect(url_for('viewCheques'))


def sign_compare(chequePayFrom, chequeSignImagePath):
    signature_mataching_accuracy = []

    signature_datasetPath = "/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/"
    signature_dataset = []
    for i in range(1, 5):
        signature_dataset.append(signature_datasetPath + str(chequePayFrom) + str('/') + str(i) + '.jpg')
    print(signature_dataset)

    # signature_dataset = ["signature_dataset/account_number_30091456699/1.jpg",
    #                      "signature_dataset/account_number_30091456699/2.jpg",
    #                      "signature_dataset/account_number_30091456699/3.jpg",
    #                      "signature_dataset/account_number_30091456699/4.jpg"]

    path = chequeSignImagePath
    print(chequeSignImagePath)
    # path = r'/Users/sahil/PycharmProjects/ChequeClearanceSystem/project/static/staffResources/chequeDataset/chequeimages/'
    # print('path: {}'.format(path))

    for signature_image in signature_dataset:
        # comparison_path = path + '/' + "crop_signature.jpg"

        comparison_path = path
        image = cv2.imread(comparison_path)
        crop_signature = cv2.resize(image, (900, 250))

        img2 = cv2.imread(signature_image)

        original = crop_signature
        # print('original: {}'.format(original))

        stored = cv2.resize(img2, (900, 250))
        original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        stored = cv2.cvtColor(stored, cv2.COLOR_BGR2GRAY)

        signature_mataching_accuracy.append(compare_images(original, stored, "Original vs. stored"))

    accruacy = max(signature_mataching_accuracy)
    print('accruacy: {}'.format(accruacy))

    # return "accruacy : {}".format(accruacy)

    return accruacy


def compare_images(imageA, imageB, title):
    # -------- Compare tow signature imgaes --------
    # compute the mean squared error and structural similarity
    # index for the images

    s = ssim(imageA, imageB)
    # MSE: % .2
    # f,

    # setup the figure
    fig = plt.figure(title)
    plt.suptitle(" SSIM: %.2f" % (s))

    # show first image
    ax = fig.add_subplot(1, 2, 1)
    # plt.imshow(imageA, cmap=plt.cm.gray)
    plt.axis("off")

    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    # plt.imshow(imageB, cmap=plt.cm.gray)
    plt.axis("off")

    # show the images
    # plt.show()
    return s
