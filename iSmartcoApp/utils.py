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




def getEmployees(Company):
    employees = User.objects.filter(Q(user_type=2) | Q(user_type=4), user_company=Company,)
    return employees


def Check_if_object_exists(objectList, valueToCheck) -> bool: #returns boolean
    #return true if valueToCheck is in objectList
    #return false if valueToCheck is not in objectList
    for object in objectList:
        if valueToCheck == object:
            return True
    return False

def list_of_countries():
    #create a tuple of countries orderd by Numbers and 3 letter codes
    #return a list of tuples
    countries = [('AF', 'Afghanistan'), ('AX', 'Aland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua And Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia And Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, Democratic Republic'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', 'Cote D\'Ivoire'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark')]

'''
def list_of_countries():
    countries = {
    1: "Afghanistan",
    2: "Albania",
    3: "Algeria",
    4: "Andorra",
    5: "Angola",
    6: "Antigua and Barbuda",
    7: "Argentina",
    8: "Armenia",
    9: "Australia",
    10: "Austria",
    1: "Azerbaijan",
    1: "The Bahamas",
    1: "Bahrain",
    1: "Bangladesh",
    1: "Barbados",
    1: "Belarus",
    1: "Belgium",
    1: "Belize",
    1: "Benin",
    1: "Bhutan",
    1: "Bolivia",
    1: "Bosnia and Herzegovina",
    1: "Botswana",
    1: "Brazil",
    1: "Brunei",
    1: "Bulgaria",
    1: "Burkina Faso",
    1: "Burundi",
    1: "Cabo Verde",
    1: "Cambodia",
    1: "Cameroon",
    1: "Canada",
    1: "Central African Republic",
    1: "Chad",
    1: "Chile",
    1: "China",
    1: "Colombia",
    1: "Comoros",
    1: "Congo, Democratic Republic of the",
    1: "Congo, Republic of the",
    1: "Costa Rica",
    1: "Côte d\'Ivoire",
    1: "Croatia",
    1: "Cuba",
    1: "Cyprus",
    1: "Czech Republic",
    1: "Denmark",
    1: "Djibouti",
    1: "Dominica",
    1: "Dominican Republic",
    1: "East Timor (Timor-Leste)",
    1: "Ecuador",
    1: "Egypt",
    1: "El Salvador",
    1: "Equatorial Guinea",
    1: "Eritrea",
    1: "Estonia",
    1: "Eswatini",
    1: "Ethiopia",
    1: "Fiji",
    1: "Finland",
    1: "France",
    1: "Gabon",
    1: "The Gambia",
    1: "Georgia",
    1: "Germany",
    1: "Ghana",
    1: "Greece",
    1: "Grenada",
    1: "Guatemala",
    1: "Guinea",
    1: "Guinea-Bissau",
    1: "Guyana",
    1: "Haiti",
    1: "Honduras",
    1: "Hungary",
    1: "Iceland",
    1: "India",
    1: "Indonesia",
    1: "Iran",
    1: "Iraq",
    1: "Ireland",
    1: "Israel",
    1: "Italy",
    1: "Jamaica",
    1: "Japan",
    1: "Jordan",
    1: "Kazakhstan",
    1: "Kenya",
    1: "Kiribati",
    1: "Korea, North",
    1: "Korea, South",
    1: "Kosovo",
    1: "Kuwait",
    1: "Kyrgyzstan",
    1: "Laos",
    1: "Latvia",
    1: "Lebanon",
    1: "Lesotho",
    1: "Liberia",
    1: "Libya",
    1: "Liechtenstein",
    1: "Lithuania",
    1: "Luxembourg",
    1: "Madagascar",
    1: "Malawi",
    1: "Malaysia",
    1: "Maldives",
    1: "Mali",
    1: "Malta",
    1: "Marshall Islands",
    1: "Mauritania",
    1: "Mauritius",
    1: "Mexico",
    1: "Micronesia, Federated States of",
    1: "Moldova",
    1: "Monaco",
    1: "Mongolia",
    1: "Montenegro",
    1: "Morocco",
    1: "Mozambique",
    1: "Myanmar (Burma)",
    1: "Namibia",
    1: "Nauru",
    1: "Nepal",
    1: "Netherlands",
    1: "New Zealand",
    1: "Nicaragua",
    1: "Niger",
    1: "Nigeria",
    1: "North Macedonia",
    1: "Norway",
    1: "Oman",
    1: "Pakistan",
    1: "Palau",
    1: "Panama",
    1: "Papua New Guinea",
    1: "Paraguay",
    1: "Peru",
    1: "Philippines",
    1: "Poland",
    1: "Portugal",
    1: "Qatar",
    1: "Romania",
    1: "Russia",
    1: "Rwanda",
    1: "Saint Kitts and Nevis",
    1: "Saint Lucia",
    1: "Saint Vincent and the Grena dines",
    1: "Samoa",
    1: "San Marino",
    1: "Sao Tome and Principe",
    1: "Saudi Arabia",
    1: "Senegal",
    1: "Serbia",
    1: "Seychelles",
    1: "Sierra Leone",
    1: "Singapore",
    1: "Slovakia",
    1: "Slovenia",
    1: "Solomon Islands",
    1: "Somalia",
    1: "South Africa",
    1: "Spain",
    1: "Sri Lanka",
    1: "Sudan",
    1: "Sudan, South",
    1: "Suriname",
    1: "Sweden",
    1: "Switzerland",
    1: "Syria",
    1: "Taiwan",
    1: "Tajikistan",
    1: "Tanzania",
    1: "Thailand",
    1: "Togo",
    1: "Tonga",
    1: "Trinidad and Tobago",
    1: "Tunisia",
    1: "Turkey",
    1: "Turkmenistan",
    1: "Tuvalu",
    1: "Uganda",
    1: "Ukraine",
    1: "United Arab Emirates",
    1: "United Kingdom",
    1: "United States",
    1: "Uruguay",
    1: "Uzbekistan",
    1: "Vanuatu",
    1: "Vatican City",
    1: "Venezuela",
    1: "Vietnam",
    1: "Yemen",
    1: "Zambia",
    1: "Zimbabwe",
    1:

'''