from rest_framework import serializers

from iSmartcoApp.models import JobCard

'''
class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('companyId',
                  'companyName',
                  'streetAddress',
                  'vatNum',
                  'email',
                  'createdBy')

class CustomUsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password',
                  'user_type',
                  'company')
'''


class JobCardSerializers(serializers.ModelSerializer):
    class Meta:
        model = JobCard
        fields = ('id',
                  'job_card_number',
                  'job_card_client',
                  'job_card_requester',
                  'job_card_reference',
                  'job_card_location',
                  'job_card_created_at',
                  'job_card_started_at',
                  'job_card_completed_at',
                  'job_card_technician',
                  'job_card_type',
                  'job_card_status',
                  'job_card_description',
                  'job_card_priority',
                  'job_card_resolution',
                  'job_card_completion_description',
                  'job_card_nva_time',)

