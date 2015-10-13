##################IMPORTS######################
import webapp2
import jinja2
import os
import urllib
import logging
import json
import csv
from google.appengine.api import users
from google.appengine.ext import ndb
##################################################


###################JINJA TEMPLATING###############
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
##################################################


##################MODELS FOR DATABASE###################
class User(ndb.Model):
	email=ndb.StringProperty(indexed=True)
	first_name=ndb.StringProperty(indexed=True)
	last_name=ndb.StringProperty(indexed=True)
	phone_number=ndb.StringProperty(indexed=True)
	date=ndb.DateTimeProperty(auto_now_add=True)
class Thesis(ndb.Model):
	author_id = ndb.StringProperty(indexed=True)
	thesis_title=ndb.StringProperty(indexed=True)
	thesis_adviser=ndb.StringProperty(indexed=True)
	thesis_abstract=ndb.TextProperty()
	thesis_university=ndb.StringProperty(indexed=True)
	thesis_college=ndb.StringProperty(indexed=True)
	thesis_department=ndb.StringProperty(indexed=True)
	thesis_member1=ndb.StringProperty(indexed=True)
	thesis_member2=ndb.StringProperty(indexed=True)
	thesis_member3=ndb.StringProperty(indexed=True)
	thesis_member4=ndb.StringProperty(indexed=True)
	thesis_member5=ndb.StringProperty(indexed=True)
	yearlist=ndb.StringProperty(indexed=True)
	section=ndb.StringProperty(indexed=True)
	thesis_filter=ndb.StringProperty(indexed=True)
	thesis_filter_year=ndb.StringProperty(indexed=True)
	date=ndb.DateTimeProperty(auto_now_add=True)
class Faculty(ndb.Model):
	title=ndb.StringProperty(indexed=True)
	first_name=ndb.StringProperty(indexed=True)
	last_name=ndb.StringProperty(indexed=True)
	email=ndb.StringProperty(indexed=True)
	phone_number=ndb.StringProperty(indexed=True)
	birthdate=ndb.StringProperty(indexed=True)
	picture=ndb.StringProperty(indexed=True)
	department_key=ndb.StringProperty(indexed=True)
	date=ndb.DateTimeProperty(auto_now_add=True)
class Student(ndb.Model):
	first_name=ndb.StringProperty(indexed=True)
	last_name=ndb.StringProperty(indexed=True)
	email=ndb.StringProperty(indexed=True)
	phone_number=ndb.StringProperty(indexed=True)
	student_number=ndb.StringProperty(indexed=True)
	birthdate=ndb.StringProperty(indexed=True)
	picture=ndb.StringProperty(indexed=True)
	year_graduated=ndb.StringProperty(indexed=True)
	department_key=ndb.StringProperty(indexed=True)
	date=ndb.DateTimeProperty(auto_now_add=True)	
class Filter(ndb.Model):
	thesis_filter_year=ndb.StringProperty(indexed=False)
	date=ndb.DateTimeProperty(auto_now_add=True)	
class University(ndb.Model):
	name=ndb.StringProperty(indexed=True)
	address=ndb.StringProperty(indexed=True)
	initial=ndb.StringProperty(indexed=True)
	date=ndb.DateTimeProperty(auto_now_add=True)	
class College(ndb.Model):
	university_key=ndb.StringProperty(indexed=True)
	name=ndb.StringProperty(indexed=True)
	departments=ndb.StringProperty(indexed=True)
	date=ndb.DateTimeProperty(auto_now_add=True)	
class Department(ndb.Model):
	college_key=ndb.StringProperty(indexed=True)
	name=ndb.StringProperty(indexed=True)
	chairperson=ndb.StringProperty(indexed=True)
	date=ndb.DateTimeProperty(auto_now_add=True)	
#################################################


##################WEB PAGES###################
class HomePage(webapp2.RequestHandler):
	def get(self):
		template=JINJA_ENVIRONMENT.get_template('homepage.html')
		self.response.write(template.render())

class RegisterPage(webapp2.RequestHandler):
	def get(self):
		template=JINJA_ENVIRONMENT.get_template('registerpage.html')
		self.response.write(template.render())

	def post(self):
		user=User()
		user.email=self.request.get('email')
		user.first_name=self.request.get('first_name')
		user.last_name=self.request.get('last_name')
		user.phone_number=self.request.get('phone_number')
		user.put()
		self.redirect('/signupdone')
class RegisterCompleted(webapp2.RequestHandler):
	def get(self):
		template=JINJA_ENVIRONMENT.get_template('registercompleted.html')
		self.response.write(template.render())

class LoginPage(webapp2.RequestHandler):
	def get(self):
		user=users.get_current_user()

		if user:
			logout_url=users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template=JINJA_ENVIRONMENT.get_template('mainpage.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))

class MainPage(webapp2.RequestHandler):
	def get(self):
		user=users.get_current_user()

		if user:
			logout_url=users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template=JINJA_ENVIRONMENT.get_template('mainpage.html')
			self.response.write(template.render(template_values))

class ThesisImportCSV(webapp2.RequestHandler):	
	def get(self):
		f=csv.reader(open('thes_list.csv','r'),skipinitialspace=True)
		for row in f:
			thesis = Thesis()
			thesis.thesis_university = row[0]
			thesis.thesis_college = row[1]
			thesis.thesis_department = row[2]
			thesis.yearlist = row[3]
			thesis.thesis_title = row[4]
			thesis.thesis_abstract = row[5]
			thesis.section = row[6]
			thesis.thesis_adviser = row[7]
			thesis.thesis_member1 = row[8]
			thesis.thesis_member2 = row[9]
			thesis.thesis_member3 = row[10]
			thesis.thesis_member4 = row[11]
			thesis.thesis_member5 = row[12]
			thesis.put()
		template = JINJA_ENVIRONMENT.get_template('importCompleted.html')
		self.response.write(template.render())
class ThesisPage(webapp2.RequestHandler):
	def get(self):
		user=users.get_current_user()

		if user:
			logout_url=users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template=JINJA_ENVIRONMENT.get_template('thesispage.html')
			self.response.write(template.render(template_values))
	
	def post(self):
		thesis=Thesis()
		thesis.author_id=self.request.get('author_id')
		thesis.thesis_title=self.request.get('thesis_title')
		thesis.thesis_adviser=self.request.get('thesis_adviser')
		thesis.thesis_abstract=self.request.get('thesis_abstract')
		thesis.thesis_university=self.request.get('thesis_university')
		thesis.thesis_college=self.request.get('thesis_college')
		thesis.thesis_department=self.request.get('thesis_department')
		thesis.thesis_member1=self.request.get('thesis_member1')
		thesis.thesis_member2=self.request.get('thesis_member2')
		thesis.thesis_member3=self.request.get('thesis_member3')
		thesis.thesis_member4=self.request.get('thesis_member4')
		thesis.thesis_member5=self.request.get('thesis_member5')
		thesis.yearlist=self.request.get('yearlist')
		thesis.section=self.request.get('section')
		thesis.thesis_filter.request.get('thesis_filter')
		thesis.put()
class ThesisListPage(webapp2.RequestHandler):
	def get(self):
		thesis=Thesis.query().order(-Thesis.date).fetch()
		logging.info(thesis)
		template_data={
			'thesis_list':thesis
		}
		template = JINJA_ENVIRONMENT.get_template('thesis_list_page.html')
		self.response.write(template.render(template_data))
class ThesisCreated(webapp2.RequestHandler):
	def get(self):
		template=JINJA_ENVIRONMENT.get_template('thesiscompleted.html')
		self.response.write(template.render())
class ThesisInformation(webapp2.RequestHandler):
	def get(self,thesis_id):
		thesis = Thesis.get_by_id(int(thesis_id))
		template_data = {
		'thesis_list': thesis
		}
		template = JINJA_ENVIRONMENT.get_template('thesisinfo.html')
		self.response.write(template.render(template_data))
class ThesisFilter(webapp2.RequestHandler):
	def get(self):
		# filterr=Filter.query().order(-Filter.date).fetch()
		# logging.info(filterr)
		# template_data={
		# 	'thesis_filter_year':filterr
		# }
		template=JINJA_ENVIRONMENT.get_template('thesis_filter.html')
		self.response.write(template.render())

	# def post(self):
	# 	filter_thesis=Filter()
	# 	filter_thesis.thesis_filter=self.request.get('thesis_filter')
	# 	filter_thesis.put()
	# 	year=self.request.get('thesis_filter_year')
	# 	thesis=Thesis.query()
	# 	thesis_year_query=thesis.filter(Thesis.yearlist==year)
	# 	# if filter_thesis.thesis_filter=='All':
	# 	# 	self.redirect('/thesis/list/all')
	# 	# elif filter_thesis.thesis_filter=='Year' :
	# 	# 	self.redirect('/thesis/list/{{year}}')
	# 	# self.redirect('/thesis/filter')
class ThesisFilterYear(webapp2.RequestHandler):
	def get(self):
		filtering=Filter.query().order(-Filter.date).fetch()
		logging.info(filtering)
		template_data={
			'filter_list':filtering
		}
		template=JINJA_ENVIRONMENT.get_template('thesis_filter_year.html')
		self.response.write(template.render(template_data))
	def post(self):
		filter_year=Filter()
		filter_year.thesis_filter_year=self.request.get('thesis_filter_year')
		filter_year.put()
		self.redirect('/thesis/year')
class ThesisListPage2012(webapp2.RequestHandler):
	def get(self,yearlist):
		thesis=Thesis.query().order(-Faculty.date).fetch()
		year='2012'
		query_year=thesis.filter(Thesis.yearlist==year)
		# year=self.request.get('thesis_filter_year')
		template = JINJA_ENVIRONMENT.get_template('thesis_list_page_2012.html')
		self.response.write(template.render())

class FacultyInformation(webapp2.RequestHandler):
	def get(self,faculty_id):
		faculty = Faculty.get_by_id(int(faculty_id))
		template_data = {
		'faculty_list': faculty
		}
		template = JINJA_ENVIRONMENT.get_template('facultyinfo.html')
		self.response.write(template.render(template_data))
class FacultyPage(webapp2.RequestHandler):
	def get(self):
		user=users.get_current_user()

		if user:
			logout_url=users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template=JINJA_ENVIRONMENT.get_template('facultypage.html')
			self.response.write(template.render(template_values))

	def post(self):
		faculty=Faculty()
		faculty.title=self.request.get('title')
		faculty.first_name=self.request.get('first_name')
		faculty.last_name=self.request.get('last_name')
		faculty.email=self.request.get('email')
		faculty.phone_number=self.request.get('phone_number')
		faculty.birthdate=self.request.get('birthdate')
		faculty.picture=self.request.get('picture')
		faculty.put()
		self.redirect('/faculty/create/completed')
class FacultyCreated(webapp2.RequestHandler):
	def get(self):
		template=JINJA_ENVIRONMENT.get_template('facultycompleted.html')
		self.response.write(template.render())
class FacultyListPage(webapp2.RequestHandler):
	def get(self):
		faculty=Faculty.query().order(-Faculty.date).fetch()
		logging.info(faculty)
		template_data={
			'faculty_list':faculty
		}
		template = JINJA_ENVIRONMENT.get_template('facultylist.html')
		self.response.write(template.render(template_data))
class FacultyInformation(webapp2.RequestHandler):
	def get(self,faculty_id):
		faculty = Faculty.get_by_id(int(faculty_id))
		template_data = {
		'faculty_list': faculty
		}
		template = JINJA_ENVIRONMENT.get_template('facultyinfo.html')
		self.response.write(template.render(template_data))

class StudentPage(webapp2.RequestHandler):
	def get(self):
		user=users.get_current_user()

		if user:
			logout_url=users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template=JINJA_ENVIRONMENT.get_template('studentpage.html')
			self.response.write(template.render(template_values))

	def post(self):
		student=Student()
		student.first_name=self.request.get('first_name')
		student.last_name=self.request.get('last_name')
		student.email=self.request.get('email')
		student.phone_number=self.request.get('phone_number')
		student.student_number=self.request.get('student_number')
		student.birthdate=self.request.get('birthdate')
		student.picture=self.request.get('picture')
		student.year_graduated=self.request.get('year_graduated')
		student.put()
		self.redirect('/student/create/completed')
class StudentCreated(webapp2.RequestHandler):
	def get(self):
		template=JINJA_ENVIRONMENT.get_template('studentcompleted.html')
		self.response.write(template.render())
class StudentListPage(webapp2.RequestHandler):
	def get(self):
		students=Student.query().order(-Student.date).fetch()
		logging.info(students)
		template_data={
			'student_list':students
		}
		template = JINJA_ENVIRONMENT.get_template('student_list_page.html')
		self.response.write(template.render(template_data))
class StudentInformation(webapp2.RequestHandler):
	def get(self,student_id):
		students = Student.get_by_id(int(student_id))
		template_data = {
		'student_list': students
		}
		template = JINJA_ENVIRONMENT.get_template('studentinfo.html')
		self.response.write(template.render(template_data))

class UniversityPage(webapp2.RequestHandler):
	def get(self):
		user=users.get_current_user()

		if user:
			logout_url=users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template=JINJA_ENVIRONMENT.get_template('universitypage.html')
			self.response.write(template.render(template_values))
	def post(self):
		university=University()
		university.name=self.request.get('name')
		university.address=self.request.get('address')
		university.initial=self.request.get('initial')
		university.put()
		self.redirect('/university/create/completed')
class UniversityCreated(webapp2.RequestHandler):
	def get(self):
		template=JINJA_ENVIRONMENT.get_template('universitycompleted.html')
		self.response.write(template.render())
class UniversityListPage(webapp2.RequestHandler):
	def get(self):
		university=University.query().order(-University.date).fetch()
		logging.info(university)
		template_data={
			'university_list':university
		}
		template = JINJA_ENVIRONMENT.get_template('university_list_page.html')
		self.response.write(template.render(template_data))
class UniversityInformation(webapp2.RequestHandler):
	def get(self,university_id):
		university = University.get_by_id(int(university_id))
		template_data = {
		'university_list': university
		}
		template = JINJA_ENVIRONMENT.get_template('universityinfo.html')
		self.response.write(template.render(template_data))

class CollegePage(webapp2.RequestHandler):
	def get(self):
		user=users.get_current_user()

		if user:
			logout_url=users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template=JINJA_ENVIRONMENT.get_template('collegepage.html')
			self.response.write(template.render(template_values))
	def post(self):
		college=College()
		college.name=self.request.get('name')
		college.departments=self.request.get('departments')
		college.put()
		self.redirect('/college/create/completed')
class CollegeCreated(webapp2.RequestHandler):
	def get(self):
		template=JINJA_ENVIRONMENT.get_template('collegecompleted.html')
		self.response.write(template.render())
class CollegeListPage(webapp2.RequestHandler):
	def get(self):
		college=College.query().order(-College.date).fetch()
		logging.info(college)
		template_data={
			'college_list':college
		}
		template = JINJA_ENVIRONMENT.get_template('college_list_page.html')
		self.response.write(template.render(template_data))
class CollegeInformation(webapp2.RequestHandler):
	def get(self,college_id):
		college = College.get_by_id(int(college_id))
		template_data = {
		'college_list': college
		}
		template = JINJA_ENVIRONMENT.get_template('collegeinfo.html')
		self.response.write(template.render(template_data))

class DepartmentPage(webapp2.RequestHandler):
	def get(self):
		user=users.get_current_user()

		if user:
			logout_url=users.create_logout_url('/')
			template_values = {
				'logout_url': logout_url
			}
			template=JINJA_ENVIRONMENT.get_template('department.html')
			self.response.write(template.render(template_values))

class SearchPage(webapp2.RequestHandler):
	def get(self):
		thesis=Thesis.query().order(-Thesis.date).fetch()
		logging.info(thesis)
		template_data={
			'thesis_list':thesis
		}
		template = JINJA_ENVIRONMENT.get_template('searchpage.html')
		self.response.write(template.render(template_data))
##################################################


######################LINKS#######################
app = webapp2.WSGIApplication([
	('/', HomePage),
	('/signup', RegisterPage),
	('/signupdone', RegisterCompleted),
	('/login', LoginPage),
	('/mainpage', MainPage),
	('/thesis/import/completed',ThesisImportCSV),
	('/thesis/create', ThesisPage),
	('/thesis/create/completed', ThesisCreated),
	('/thesis/filter',ThesisFilter),
	('/thesis/year',ThesisFilterYear),
	# ('/thesis/list(.*)', ThesisFilterInformation),
	('/thesis/list/all', ThesisListPage),
	('/thesis/list/2012', ThesisListPage2012),
	('/thesis/(.*)', ThesisInformation),
	('/faculty/create', FacultyPage),
	('/faculty/create/completed', FacultyCreated),
	('/faculty/list', FacultyListPage),
	('/faculty/(.*)', FacultyInformation),
	('/student/create', StudentPage),
	('/student/create/completed', StudentCreated),
	('/student/list', StudentListPage),
	('/student/(.*)', StudentInformation),
	('/university/create', UniversityPage),
	('/university/create/completed', UniversityCreated),
	('/university/list', UniversityListPage),
	('/university/(.*)', UniversityInformation),
	('/college/create', CollegePage),
	('/college/create/completed', CollegeCreated),
	('/college/list', CollegeListPage),
	('/college/(.*)', CollegeInformation),
	('/department/create', DepartmentPage),
	('/search', SearchPage),

], debug = True)
##################################################
