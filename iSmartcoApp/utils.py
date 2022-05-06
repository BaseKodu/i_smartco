from iSmartcoApp.models import JobCard, Employee, Company, Client, User, MaterialUsed, JobCardCategory



#function for creating job card number
def generateNextJobCardNumber(company_id):
    nextNum = JobCard.objects.filter(job_card_company=company_id).count()#find a much more effective way. lets say there's 10 job. and [5] gets deleted. this thing will count 9 jobs and make a job number 10. therefore, theres no uniqueness.  
    nextNum += 1
    return nextNum

def generateNextClientNumber(company_id):
    nextNum = Client.objects.filter(client_company=company_id).count()#find a much more effective way. lets say there's 10 job. and [5] gets deleted. this thing will count 9 jobs and make a job number 10. therefore, theres no uniqueness.
    nextNum += 1
    return nextNum


def generateNextEmployeeNumber(company_id):
    nextNum = Employee.objects.filter(employee_company=company_id).count()#find a much more effective way. lets say there's 10 job. and [5] gets deleted. this thing will count 9 jobs and make a job number 10. therefore, theres no uniqueness.
    nextNum +=1
    return nextNum



def getClients(UserType,UserCompany):
    #returning clients that certain users are allowed to access

    clients = User.objects.all()  #initializing clients with a User object

    if UserType == 1:#companyadmin should be able to see all clients regardless of the company
        clients = User.objects.all()
    elif UserType == 2 or UserType ==4: #Company admin or employee should bee able to see all company clients
        clients = User.objects.filter(user_company=UserCompany, user_type=3)
    elif UserType == 3:
        clients = User.objects.get(user_id=UserCompany.id)#only able to see themselves
    
    return clients
