#***(1)Returns all Students from Students table
Students = Students.objects.all()

#(2)Returns first Students in table
firstStudent = Students.objects.first()

#(3)Returns last Students in table
lastCustomer = Students.objects.last()

#(4)Returns single Students by name
StudentsByName = Students.objects.get(name='Nurtaj')

#***(5)Returns single Students by name
StudentsById = Students.objects.get(id=1)
# print(StudentsById)
#***(6)Returns all orders related to Students (firstStudents variable set above)
firstStudent.order_set.all()

#(7)***Returns orders Students name: (Query parent model values)
order = Order.objects.first() 
parentName = order.Students.name

#(8)***Returns Courses from Courses table with value of "English" in category attribute
Courses = Courses.objects.filter(category="english")


#(9)***Order/Sort Objects by id
leastToGreatest = Courses.objects.all().order_by('id') 
greatestToLeast = Courses.objects.all().order_by('-id') 


#(10) Returns all Courses with typecast of "summer": (Query Many to Many Fields)
#CoursesFiltered = Courses.objects.filter(typecast__name="summer")

#>>> from accounts.models import *
#>>> Coursess = Courses.objects.filter(typecast__name="spring")
#>>> print(Coursess)
#<QuerySet [<Courses: Web Design>, <Courses: English  basic learning>, <Courses: calculations>]>

#>>> orders=firstStudent.order_set.all()
#>>> print(orders)

#>>> orders=Order.objects.first()
#>>> print(orders.Students.age)