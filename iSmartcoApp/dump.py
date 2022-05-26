#A file to dump all code you dont need now, but might need it later

#First is methods you need when theres a need to do certain actions
'''
	def start_job(self, job_card_id):#only used once in a job card
		job_card = JobCard[job_card_id]
		job_card.job_card_status = 4
		job_card.job_card_started_at = datetime.datetime.now()
		job_card.save()
		return job_card

	def pause_job(self, job_card_id):
		job_card = JobCard[job_card_id]
		job_card.job_card_status = 5
		job_card.job_card_last_pause = datetime.datetime.now()		
		job_card.save()
		return job_card

	def continue_job(self, job_card_id):
		job_card = JobCard[job_card_id]
		job_card.job_card_status = 4
		job_card.job_card_nva_time += datetime.datetime.now() - job_card.job_card_last_pause
		job_card.save()
		return job_card

	def complete_job(self, job_card_id):
		job_card = JobCard[job_card_id]
		job_card.job_card_status = 6
		job_card.job_card_completed_at = datetime.datetime.now()
		job_card.save()
		return job_card
	
	def cancel_job(self, job_card_id):
		job_card = JobCard[job_card_id]
		job_card.job_card_status = 7
		job_card.save()
		return job_card
'''