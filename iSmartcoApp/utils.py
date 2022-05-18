from iSmartcoApp.models import JobCard,  Company, User, MaterialUsed, JobCardCategory, ClientUser
from iSmartcoApp.constants import GENERAL_COMPANY
from django.db.models import Q
''' for circular import error use this although with ready(). You'll read up more info on that
from django.apps import apps
JobCard = apps.get_model('iSmartcoApp', 'JobCard')
User = apps.get_model('iSmartcoApp', 'User')
'''

#function for creating job card number
def generateNextJobCardNumber(company_id):
    nextNum = JobCard.objects.filter(job_card_company=company_id).count()#find a much more effective way. lets say there's 10 job. and [5] gets deleted. this thing will count 9 jobs and make a job number 10. therefore, theres no uniqueness.  
    nextNum += 1
    return nextNum

'''
def generateNextClientNumber(company_id):
    nextNum = Client.objects.filter(client_company=company_id).count()#find a much more effective way. lets say there's 10 job. and [5] gets deleted. this thing will count 9 jobs and make a job number 10. therefore, theres no uniqueness.
    nextNum += 1
    return nextNum


def generateNextEmployeeNumber(company_id):
    nextNum = Employee.objects.filter(employee_company=company_id).count()#find a much more effective way. lets say there's 10 job. and [5] gets deleted. this thing will count 9 jobs and make a job number 10. therefore, theres no uniqueness.
    nextNum +=1
    return nextNum

'''

def getJobCardCategories(UserCompany):
    categories = JobCardCategory.objects.filter(Q(company_owner=GENERAL_COMPANY) | Q(company_owner=UserCompany))
    #categories = Q(JobCardCategory__company_owner=GENERAL_COMPANY) | Q(JobCardCategory__company_owner=UserCompany)
    #categories.append(JobCardCategory.objects.filter(company_owner=GENERAL_COMPANY))
    return categories

def getClients(UserType,UserCompany, user_id):
    #returning clients that certain users are allowed to access

    #clients = User.objects.none() #initializing clients with a User object

    if UserType == 1:#companyadmin should be able to see all clients regardless of the company
        clients = User.objects.all(user_type=3)# not finish. See later
    elif UserType == 2 or UserType ==4: #Company admin or employee should bee able to see all company clients
        clients = User.objects.filter(user_company=UserCompany, user_type=3)
    elif UserType == 3: #client
        clients = User.objects.filter(id=user_id)#only able to see themselves
    
    return clients

def getClientUsers(Client):
    clientUsers = ClientUser.objects.filter(works_for=Client)
    return clientUsers


def Check_if_object_exists(objectList, valueToCheck): #returns boolean
    #return true if valueToCheck is in objectList
    #return false if valueToCheck is not in objectList
    for object in objectList:
        if valueToCheck == object:
            return True
    return False


def listOfCountries():
    #returning a Dict of countries with autonumbered keys
    countries = {
        1: 'Afghanistan',
        2: 'Albania',
        3: 'Algeria',
        4: 'Andorra',
        5: 'Angola',
        6: 'Antigua and Barbuda',
        7: 'Argentina',
        8: 'Armenia',
        9: 'Australia',
        10: 'Austria',
        11: 'Azerbaijan',
        12: 'Bahamas',
        13: 'Bahrain',
        14: 'Bangladesh',
        15: 'Barbados',
        16: 'Belarus',
        17: 'Belgium',
        18: 'Belize',
        19: 'Benin',
        20: 'Bhutan',
        21: 'Bolivia',
        22: 'Bosnia and Herzegovina',
        23: 'Botswana',
        24: 'Brazil',
        25: 'Brunei',
        26: 'Bulgaria',
        27: 'Burkina Faso',
        28: 'Burundi',
        29: 'Cambodia',
        30: 'Cameroon',
        31: 'Canada',
        32: 'Cape Verde',
        33: 'Central African Republic',
        34: 'Chad',
        35: 'Chile',
        36: 'China',
        37: 'Colombia',
        38: 'Comoros',
        39: 'Congo',
        40: 'Costa Rica',
        41: 'Côte d\'Ivoire',
        42: 'Croatia',
        43: 'Cuba',
        44: 'Cyprus',
        45: 'Czech Republic',
        46: 'Denmark',
        47: 'Djibouti',
        48: 'Dominica', 
        49: 'Dominican Republic',
        50: 'East Timor',
        51: 'Ecuador',
        52: 'Egypt',
        53: 'El Salvador',
        54: 'Equatorial Guinea',
        55: 'Eritrea',
        56: 'Estonia',
        57: 'Ethiopia',
        58: 'Fiji',
        59: 'Finland',
        60: 'France',
        61: 'Gabon',
        62: 'Gambia',
        63: 'Georgia',
        64: 'Germany',
        65: 'Ghana',
        66: 'Greece',
        67: 'Grenada',
        68: 'Guatemala',
        69: 'Guinea',
        70: 'Guinea-Bissau',
        71: 'Guyana',
        72: 'Haiti',
        73: 'Honduras',
        74: 'Hungary',
        75: 'Iceland',
        76: 'India',
        77: 'Indonesia',
        78: 'Iran',
        79: 'Iraq',
        80: 'Ireland',
        81: 'Israel',
        82: 'Italy'
    }

    return countries