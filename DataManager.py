# Libraries :
# Already installed on virtual environments.
import os
import sys
import time
import csv
# Need to be installed on virtual environments.
import requests
import bs4


# -------------------------------------------------------------------------------
# Functions :
#

# 1. Handle the folders and files creation.
def pathtofolder():
    """
    Return the current path to ScrapBookin.py.

    :return: The path of current working directory.
    :rtype: str

    :Example:

    >>> pathtofolder()
    "C:\\Folder\\ProjectFolder"

    .. note:: os.path.realpath(sys.argv[0]) work also, but only on IDE.
    """
    return os.getcwd()

def createdatafolder(name):
    """
    Create the <name> folder at the root of ScrapBookin.py.

    :param name: Name of the folder that need to be created
    :type name: str

    :Example:

    >>> createdatafolder("folder1")
    #Will create <folder1> in the current working directory.
    """
    folder = os.path.join(pathtofolder(),name)
    os.makedirs(folder)
    pass

def datafolderexist(name):
    """
    Check if the folder <name> exists at the root and return True or False.

    :param name: Name of the folder checked
    :type name: str
    :return: A boolean : If the folder <name> exists.
    :rtype: bool

    :Example:

    >>> datafolderexist("folder1")
    True
    >>> datafolderexist("folder2")
    False
    """
    folderpath = os.path.join(pathtofolder(), name)
    return os.path.exists(folderpath)

def checkfolderdata(folder = 'datas'):
    """
    Strong verification of the folder data existence.
    Check if the <folder> exist. While not, it tries to create it.
    Then, by recurrence, check again.
    Return True when <folder> exist.

    :param folder: The folder that WILL BE created
    :type folder: str
    :return: Return True only if <folder> folder exist.
    :rtype: bool

    :Example:

    >>> checkfolderdata("folder1")
    #Will Create <folder1> if it doesn't exist yet.
    True

    .. warning:: May cause RunTimeError : maximum depth exceeded...
    """
    if datafolderexist(folder):
        return True
    else:
        createdatafolder(folder)
        checkfolderdata(folder)

def datafileexist(filename):
    """
    Check if the file <filename> in /datas exists and return True or False.

    :param filename: Name of the file that will be checked
    :type filename: str
    :return: If the file <filename>.csv exist in .././datas/
    :rtype: bool

    :Example:

    >>> datafileexist("Default")
    True
    >>> datafileexist("Laws")
    False

    .. warning:: Only check the "datas" folder
    """
    filePath = os.path.join(pathtofolder(), "datas", filename)
    fileFormat = '.csv'
    return os.path.exists(f'{filePath+fileFormat}')

def eraseDatas(folderToRemove='datas'):
    """
    Erase all the content from a folder. Then erase the folder.

    :param folderToRemove: the folder removed
    :type folderToRemove: str
    """
    directoryToRemove = os.path.join(pathtofolder(), folderToRemove)
    for i in os.listdir(directoryToRemove):
        os.remove(os.path.join(directoryToRemove, i))
    os.rmdir(directoryToRemove) # Now the folder is empty of files
    pass

def listFolders(folderRoot):
    """
    Return a list of folders in the <folderRoot> folder.

    :param folderRoot: folder's path where other directories exist.
    :type folderRoot: str
    :return: list of directories
    :rtype: list (str)
    """
    return os.listdir(folderRoot)

def erasePictures(folderPicture='pictures'):
    """
    Function that erases the /pictures folder.

    :param folderPictures: name of the folder that contains pictures.
    :type folderPictures: str
    """
    pathToPictures = os.path.join(pathtofolder(), folderPicture)
    folderList = listFolders(pathToPictures)

    for category in folderList:
        erasePath = os.path.join(folderPicture, category)
        eraseDatas(erasePath)

    eraseDatas(pathToPictures) # Now /pictures is empty of files/folders
    pass

def eraseAll():
    """Erase /pictures and /datas from the working directory."""
    user = input("Would you like to erase all data? (Y/N)")

    if 'y' in user.lower() and not 'n' in user.lower():
        if checkfolderdata():
            eraseDatas()
            print("/datas folder erased.")
        if checkfolderdata('pictures'):
            erasePictures()
            print("/pictures folder erased.")
        print("Datas are erased.")
    else:
        print("Datas not erased : Be sure they're not corrupted.")
    pass


# 2. Manage the .csv
def excelExport(choice):
    """
    A modification to .csv - add a sep definition, helping the reading in
    Excel.
    :param choice: 'excel' if you want a better reading in excel
    :type choice: str
    :return: Return the informations to add on .csv files at the first line
    :rtype: str

    .. warning::
    """
    if "excel" in choice:
        return 'sep=|\n'
    else:
        return ''

def createcsv(fileName):
    """
    Create or rewrite the csv file of each category.

    :param fileName: Name of the .csv file that'll be created in .././datas/
    :type fileName: str

    .. note:: If it exists, will erase the current <filename>.csv and write the
              informations wrote bellow.
    """
    fileName = os.path.join(pathtofolder(), 'datas', fileName)
    fileFormat = '.csv'
    file = f'{fileName + fileFormat}'

    csvKeys = ["product_page_url", "universal_product_code", "title",
               "price_including_tax", "price_excluding_tax", "number_available",
               "product_description", "category", "review_rating", "image_url"]

    addon = excelExport('excel')

    with open(file, 'w', newline="", encoding='utf-8') as csvFile:
        csvFile.write(addon) # Define the separator as <">.
        resultWriter = csv.writer(csvFile, delimiter = '|', dialect = "excel")
        resultWriter.writerow(csvKeys)
    pass

def addcsv(data, fileName):
    """
    Add new <data> on the <filename> .csv file. (at ./datas/)

    :param data: datas scraped
    :param fileName: Name of the .csv edited
    :type data: str
    :type fileName: str
    """
    fileName = os.path.join(pathtofolder(), 'datas', fileName)
    fileFormat = '.csv'
    file = f'{fileName+fileFormat}'

    with open(file, 'a', newline="", encoding='utf-8') as csvFile:
        resultWriter = csv.writer(csvFile, delimiter = '|', dialect = "excel")
        resultWriter.writerow(data)

    pass


# 3. Gestion des images
def downloadpic(url, name, path):
    """
    Download .jpg from the %url%, and name it %name% at the path : %path%.

    :param url: Url of the picture
    :param name: Name of the .jpg created
    :param path: The path where the .jpg will be placed
    :type url: str
    :type name: str
    :type path: str
    """
    a = requests.get(url)

    checkfolderdata("pictures")
    folderPath = os.path.join("pictures", path)

    checkfolderdata(folderPath)

    filePath = os.path.join(folderPath, name)
    fileFormat = '.jpg'
    file = f'{filePath + fileFormat}'

    with open(file, "wb") as pic:
        pic.write(a.content)
    pass


def managecsv(data):
    """
    Write datas in the category .csv respective.

    Keywords arguments:
    :param data: dataset of books
    :type data: list
    """

    checkfolderdata()
    if not datafileexist(data[7]):
        createcsv(data[7])
        managecsv(data)
    else:
        addcsv(data, data[7])