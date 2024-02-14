import json
import requests
import uuid
import jwt
from datetime import datetime, timedelta
from uuid import uuid4

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response

from vendor_management_system.settings import DB, PUBLIC_KEY
from utils import generate_url
from main_app.response import SuccessResponse, BadRequestResponse
from google.auth import jwt as gjwt


def landing_page(request):
	posts = [{},{},{},{}] #list(DB.blogs.find())
	return render(request, 'src/html/landing_page.html', {'posts': posts})

def login(request):

	return render(request, 'src/html/login.html', {})

@csrf_exempt
def google_callback(request):
	token = request.POST.get("credential")
	decoded_token = gjwt.decode(token, verify=False)
	
	name = decoded_token.get("name","")
	email = decoded_token.get("email","")
	
	user_doc = DB.users.find_one({"email":email})
	decoded_token['created_at'] = datetime.now()
	if not user_doc:
		DB.leads.insert_one(decoded_token)
		
	if user_doc and user_doc.get("is_verified"):

		req_id = str(uuid.uuid4())
		id = user_doc.get("id")
		mob = user_doc.get("mobile")
		email = user_doc.get("email","")
		otp_time = user_doc.get("otp_created")
		user_type = user_doc.get("type")
		company_id = user_doc.get("company_id")
		name = user_doc.get("name")
		user_id = user_doc.get("user_id")

		user_dict = {
				  "login_type": "google",
                  "id": id,
                  "email": email,
                  "user_type": user_type,
                  "user_id": user_id,
                  "username": name,
                  "mobile": mob,
                  "company_id": company_id
                }

		jwt_token = generate_token(user_dict)
		user_doc = DB.users.find_one_and_update({"email":email},{"$set":{"token":jwt_token, "token_valid":True,"req_id":req_id}})

		return redirect('/dashboard')
	
	return redirect('/inquiry')

def inquiry(request):
	
	return render(request,'src/html/inquiry.html')

def dashboard(request):

	# token = request.GET.get('t')
	# valid = False
	
	# if request.COOKIES.get('t'):
	# 	valid, data = verify_token(request.COOKIES['t'])

	# if token:
	# 	valid, data = verify_token(token)
		
	# if not valid:
	# 	return redirect('https://infinitybrands.co/login/')
	
	data = {}

	total_orders = 100
	total_employees = 50
	total_revenue = 100000

	response = render(request, "src/html/dashboard.html",{"data": {'total_employees': total_employees, 'total_revenue': total_revenue, 'total_orders': total_orders}})

	# if token and not request.COOKIES.get("t"):
	# 	response.set_cookie("t",token)

	return response


def questions(request):
	questions = list(DB.questions.find({}))
	que_count = 0
	user_id = 1
	temp_qp = DB.question_papers.find_one({'user_id': user_id, 'status': 'IN_QP'})
	if temp_qp:
		qp_temp_id = temp_qp.get('qp_temp_id')
		que_count = len(temp_qp.get('qp_items'))
	else:
		qp_temp_id = str(uuid4())
		que_count = 0
	return render(request, 'src/html/questions.html', {"questions": questions, 'que_count': que_count, 'qp_temp_id': qp_temp_id})

def questions_discovery(request):
	questions = list(DB.questions.find({}))
	que_count = 0
	user_id = 1
	temp_qp = DB.question_papers.find_one({'user_id': user_id, 'status': 'IN_QP'})
	if temp_qp:
		qp_temp_id = temp_qp.get('qp_temp_id')
		que_count = len(temp_qp.get('qp_items'))
	else:
		qp_temp_id = str(uuid4())
		que_count = 0
	return render(request, 'src/html/questions_discovery.html', {"questions": questions, 'que_count': que_count, 'qp_temp_id': qp_temp_id})


@csrf_exempt
def add_to_question_paper(request):
	requested_data = dict(request.POST.items())
	user_id = 1

	item_to_add = {
	}

	que = DB.questions.find_one({'qid': requested_data.get('qid')}, {'_id': 0})
	item_to_add.update(que)
	DB.question_papers.update_one(
    	{'qp_temp_id': requested_data.get('qp_temp_id')},
	    {
	        '$push': {'qp_items': item_to_add},  # Add item to the items array
	        '$set': {
	            'qp_temp_id': requested_data.get('qp_temp_id'),
	            'status': "IN_QP",
	            'insti_id': requested_data.get('insti_id'),
	            'user_id': user_id
	        }
	    },
	    upsert=True  # Create a new document if one doesn't exist
	)
	return JsonResponse({'message': "Successfully Updated"})



@csrf_exempt
def update_question_paper(request):

	requested_data = dict(request.POST.items())
	print(requested_data)
	qp_temp_id = requested_data.get('qp_temp_id')
	qid = requested_data.get('qid')
	insti_id = requested_data.get('insti_id')

	action = requested_data.get('action')
	if action == 'delete':
		DB.question_papers.update_one(
		    {'qp_temp_id': qp_temp_id},  # Match document by cart_id
		    {
		        '$pull': {'qp_items': {'qid': qid}}  # Remove item with matching pid from items array
		    }
		)

	return JsonResponse({'message': "Successfully Updated"})


def review_qp(request, qp_temp_id):

	# temp_id = request.GET.get('temp_id')
	# if temp_id:
	# 	order_data = DB.cart_templates.find_one({'temp_id': temp_id}, {'_id': 0})
	# 	cart_id = str(uuid4())
	# 	order_data['cart_id'] = cart_id
	# 	order_data['status'] = 'IN_CART'
	# 	DB.partner_orders.insert_one(order_data)

	temp_qp = DB.question_papers.find_one({'qp_temp_id': qp_temp_id, 'status': 'IN_QP'})


	return render(request, 'src/html/review_qp.html', {'insti_id': temp_qp.get('insti_id'), 'temp_qp': temp_qp, 'que_count': len(temp_qp.get('qp_items')), 'qp_temp_id': temp_qp.get('qp_temp_id')})


def question_papers(request):
	question_papers = list(DB.question_papers.find({'status': {'$ne': 'IN_QP'}}).sort('_id', -1))
	return render(request, "src/html/question_papers.html", {"question_papers":question_papers,"items_count":len(question_papers)})


@csrf_exempt
def set_question_paper(request):
	qp_temp_id = request.POST.get('qp_temp_id')
	qp_id = 'QP{}'.format(str(int(datetime.now().timestamp())))
	created_at = datetime.now()
	DB.question_papers.update_one({'qp_temp_id': qp_temp_id}, {'$set': {'status': 'READY_FOR_EXAM', 'qp_id': qp_id, 'created_at': created_at}})
	return JsonResponse({})

@csrf_exempt
def add_question(request):
	if request.method == 'POST':
		content = request.POST.get('content')
		qid = str(uuid4())
		source = 'form'
		if content:
			source = 'quill'
		DB.questions.insert_one({'que': content, 'qid': qid, 'source': source})
		return JsonResponse({})
	return render(request, "src/html/add_question.html", {})

@csrf_exempt
def students(request):

	if request.method == 'POST':
		student_data = dict(request.POST.items())
		print(student_data)
		student_id = student_data.get('student_id')
		if not student_id:
			student_id = str(uuid4())
		student_data['student_id'] = student_id
		DB.students.update_one({'student_id': student_id}, {'$set': student_data}, upsert=True)
		print(student_data)
		return JsonResponse({'data': student_data})
	students_data = list(DB.students.find({}).sort('_id', -1))
	return render(request, 'src/html/students.html', {'students_data': students_data})

@csrf_exempt
def get_student(request, student_id):
	student_data = DB.students.find_one({'student_id': student_id}, {'_id': 0})
	return JsonResponse({'data': student_data})

@csrf_exempt
def delete_student(request, student_id):
	if request.method == 'DELETE':
		student_data = DB.students.delete_one({'student_id': student_id})
		return JsonResponse({})

def generate_token(user_dict):

    user_dict = {"login_type": "google",
                  "id": 2,
                  "email": "nk@infinitybrands.co",
                  "user_type": "partner",
                  "user_id": "USER12345",
                  "username": "GRASSLAND CORPORATION",
                  "mobile": "9540025266",
                  "company_id": "ABC123"
                }
    token = jwt.encode({"exp": datetime.now() + timedelta(days=7) , **user_dict}, PUBLIC_KEY, algorithm="HS256")

    return token

# print(generate_token({}))


def verify_token(token):
    
    decoded_token = {}  
    if token:
        try:
            auth_token  = token.split(" ")[-1] if "Bearer" in token else token
            decoded_token = jwt.decode(auth_token, PUBLIC_KEY, algorithms="HS256", options={"verify_exp": False})

        except Exception as e:
            return False, {}

        user_doc = DB.users.find_one({"id": decoded_token["id"]}) or {}
        if not user_doc.get('token_valid'):
            return False, {}
    
    else:
        return False, {}
    
    return True, decoded_token





def logout(request):
    del request.session['user_id']
    del request.session['role']
    return redirect('login')




def employees_attendance(request):
    
	# token = request.COOKIES.get('t')
	# st, data = verify_token(token)
	# if not st:
	# 	return redirect('https://infinitybrands.co/login/')

	# company_id = data.get('company_id')
	# print(company_id)
    
	if request.method == 'POST':
		requested_data = dict(request.POST.items())
		
		requested_data['company_id'] = company_id
		requested_data['emp_id'] = 'EMP' + str(int(datetime.now().timestamp()))
		requested_data['is_employee'] = False if requested_data.get('role') == 'admin' else True
		DB.users.insert_one(requested_data)

	employees = list(DB.users.find({'company_id': company_id}, {'_id': 0}).sort('_id', -1))
	return render(request, 'src/html/employees_attendance.html', {'employees': employees})
    
def attendance_details(request, emp_id):

	# token = request.COOKIES.get('t')
	# st, data = verify_token(token)
	# if not st:
	# 	return redirect('https://infinitybrands.co/login/')

	# company_id = data.get('company_id')

	if request.method == 'POST':
		requested_data = dict(request.POST.items())
		print(requested_data)
	emp_name = DB.users.find_one({'emp_id': emp_id})
	emp_attendance = list(DB['attendance_{0}'.format(company_id)].find({'emp_id': emp_id}, {'_id': 0}).sort('_id', -1))
	return render(request, 'src/html/attendance_details.html', {'emp_id': emp_id, 'emp_name': emp_name.get('name'), 'emp_history': emp_attendance})


@csrf_exempt
def mark_attendance(request):
    # token = request.COOKIES.get('t')
    # st, data = verify_token(token)
    # if not st:
    #     return redirect('https://infinitybrands.co/login/')

    # company_id = data.get("company_id")
    emp_id = request.POST.get('emp_id')
    action = request.POST.get('action')

    if not emp_id or not action or not company_id:
        return JsonResponse({})

    emp_docs = DB['attendance_{}'.format(company_id)].find_one({"emp_id":emp_id, "date":str(datetime.now().date())})

    if emp_docs:

        if action in emp_docs:
            return JsonResponse({})

        elif action == 'out':
            if emp_docs.get('in'):
                in_at = emp_docs['in']['created_at']
                working_hrs = datetime.now() - in_at

                hours, remainder = divmod(working_hrs.seconds, 3600)
                minutes, _ = divmod(remainder, 60)

                DB['attendance_{}'.format(company_id)].update_one({"emp_id":emp_id, "date":str(datetime.now().date()),},{"$set":{ 'out.action':action, 'out.created_at':datetime.now(), 'work_hrs':f'{hours} hr, {minutes} min' }}, upsert=True)

        return JsonResponse({})
    DB['attendance_{}'.format(company_id)].update_one({"emp_id":emp_id, "date":str(datetime.now().date())},{"$set":{"in.created_at":datetime.now(), 'in.action':action, "status":'present'}}, upsert=True)

    return JsonResponse({})


def profile(request):
    return render(request, 'src/html/profile.html')


@csrf_exempt
def employees(request):
	
	# token = request.COOKIES.get('t')
	# st, data = verify_token(token)
	# if not st:
	# 	return redirect('https://infinitybrands.co/login/')

	company_id = data.get('company_id')
    
	if request.method == 'POST':
		requested_data = dict(request.POST.items())
		
		requested_data['company_id'] = company_id
		requested_data['emp_id'] = 'EMP' + str(int(datetime.now().timestamp()))
		requested_data['is_employee'] = False if requested_data.get('role') == 'admin' else True
		DB.users.insert_one(requested_data)

	employees = list(DB.users.find({'company_id': company_id}, {'_id': 0}).sort('_id', -1))
	return render(request, 'src/html/employees.html', {'employees': employees})


def take_exam(request):
	qp_id = request.GET.get('qp_id')
	que_paper = DB.question_papers.find_one({'qp_id': qp_id}, {'_id': 0, 'guideline': 1, 'qp_id': 1})
	return render(request, 'src/html/exam.html', {'qp_id': que_paper.get('qp_id'), 'question_paper': que_paper})


def start_exam(request):
	qp_id = request.GET.get('qp_id')
	que_number = int(request.GET.get('que_num')) - 1 if request.GET.get('que_num') else 0
	question = list(DB.question_papers.aggregate([{'$match': {'qp_id': qp_id}}, {
        '$project': {
            'qp_items_length': {'$size': '$qp_items'},
            'question': {'$arrayElemAt': ['$qp_items', que_number]}  # Retrieve the first question from qp_items array
        }
    }]))
	if question:
		qp_items_length = list(range(1, question[0]['qp_items_length'] + 1))
		question = question[0]['question']
		
	next_btn = None
	prev_btn = None
	if len(qp_items_length) == que_number + 1:
		next_btn = 'disable'
	if que_number == 0:
		prev_btn = 'disable'

	return render(request, 'src/html/exam_questions.html', {'prev_btn': prev_btn, 'next_btn': next_btn, 'qp_id': qp_id, 'question': question, 'qp_items_length': qp_items_length, 'que_label': que_number + 1})


@csrf_exempt
def account(request):

	# token = request.COOKIES.get('t')
	# st, data = verify_token(token)
	# if not st:
	# 	return redirect('https://infinitybrands.co/login/')
	if request.method == 'POST':
		requested_data = dict(request.POST.items())
		insti_id = 'IN{}'.format(str(int(datetime.now().timestamp())))
		requested_data['insti_id'] = insti_id
		DB.institutes.insert_one(requested_data)
	return render(request, 'src/html/account.html', {'account': account})


