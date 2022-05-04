from iSmartcoApp.models import JobCard, Employee, Company, Client, User, MaterialUsed, JobCardCategory



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
