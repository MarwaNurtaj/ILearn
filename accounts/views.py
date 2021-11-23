from django.shortcuts import render,redirect

from django.http import HttpResponse 
from django.forms import inlineformset_factory 
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate,login,logout


from django.contrib import messages


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from django.core.checks import messages
from django.shortcuts import render, redirect

from django.http import HttpResponse,JsonResponse

# Create your views here.
from .models import*
from .forms import OrderForm, CreateUserForm, StudentForm
from .filters import OrderFilter
from .decorators import  unauthenticated_user,allowed_users,admin_only


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form=CreateUserForm()
		if request.method =='POST':

			form=CreateUserForm(request.POST)
			if form.is_valid():
				user= form.save()
				username= form.cleaned_data.get('username')
					

				#messages.success(request,'Account was created for ' + username)

				return redirect('login')


		context={'form':form}
		return render(request,'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
	if request.method =='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')

		user=authenticate(request,username=username,password=password)

		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.info(request,'Username OR password is incorrect')
	context = {}
	return render(request,'accounts/login.html', context)

@unauthenticated_user
def homepage(request):
	context = {}
	return render(request,'accounts/homepage.html',context)



def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	order=Order.objects.all()
	students=Students.objects.all()
	courses= Courses.objects.all()

	total_Students=students.count()
	total_order=order.count()


	delivered=order.filter(status='Deliverd').count()
	pending=order.filter(status='Pending').count()



	context = {'order':order, 'students':students,'courses':courses,
				'total_order':total_order,'delivered':delivered,
				'pending':pending
	}

	return render(request,'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def userPage(request):
	order = request.user.students.order_set.all()
	total_order=order.count()


	delivered=order.filter(status='Deliverd').count()
	pending=order.filter(status='Pending').count()
	print('ORDER:', order)
	context={'order':order,'total_order':total_order,'delivered':delivered,
				'pending':pending}
	return render(request,'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def accountSettings(request):
	students = request.user.students
	form = StudentForm(instance=students)

	if request.method =='POST':
		form = StudentForm(request.POST, request.FILES,instance=students)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)

def teacherSettings(request):
	teacher = request.user.teacher 
	form = TeacherForm(instance=teacher)

	if request.method =='POST':
		form = TeacherForm(request.POST, request.FILES,instance=teacher)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/teacher_setting.html', context)	

@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def courses(request):

	courses=Courses.objects.all()

	return render(request,'accounts/courses.html',{'courses':courses})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def students(request, pk_test):

	student =Students.objects.get(id=pk_test)

	order = student.order_set.all()

	order_count=order.count()

	myFilter = OrderFilter(request.GET,queryset=order)
	order=myFilter.qs


	context = {'students':student, 'order':order,'order_count':order_count,'myFilter':myFilter}

	return render(request,'accounts/students.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
	OrderFormSet = inlineformset_factory(Students, Order, fields=('Courses', 'status'),extra=5)
	students=Students.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=students)

	#form = OrderForm(initial={'students':Students})
	if request.method =='POST':
		#print('Printing Post:',request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=students)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context={'formset':formset}
	return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):

	order= Order.objects.get(id=pk)

	form=OrderForm(instance=order)

	if request.method =='POST':
		#print('Printing Post:',request.POST)
		form = OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')


	context={'form':form}
	return render(request,'accounts/update.html',context)
	#return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
	order= Order.objects.get(id=pk)

	if request.method =='POST':
		order.delete()
		return redirect('/')


	context={'item':order}
	return render(request,'accounts/delete.html',context)

def chathome(request):
    return render(request, 'accounts/chathome.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)

    return render(request, 'accounts/room.html', {
        'username': username,
        'room' : room,
        'room_details' : room_details
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']     

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)    


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Massage.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')
     
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Massage.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})


def index(request):
	context={}
	return render(request,'accounts/index.html', context)  
def login2(request):
	context={}
	return render(request,'accounts/register2.html', context)  	   

@login_required(login_url='login')

def webdesign(request):
	courses=Courses.objects.all()
	return render(request,'accounts/web_design.html',{'courses':courses})	

@login_required(login_url='login')

def electric(request):
	courses=Courses.objects.all()
	return render(request,'accounts/electronic _circuits.html',{'courses':courses})	

@login_required(login_url='login')

def english(request):
	courses=Courses.objects.all()
	return render(request,'accounts/english.html',{'courses':courses})	

@login_required(login_url='login')

def calculations(request):
	courses=Courses.objects.all()
	return render(request,'accounts/calculations.html',{'courses':courses})	



def aboutus(request):
	return render(request,'accounts/aboutus.html')


def support(request):
	return render(request,'accounts/suport.html')		