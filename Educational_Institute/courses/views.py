from django.shortcuts import render, HttpResponse, redirect
from courses.models import Course, Video, Payment, UserCourse
from courses.forms import RegistrationForm , LoginForm
from django.views import View
from django.contrib.auth import logout
from time import time
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    courses = Course.objects.all()
    print(courses)
    return render(request, 'home.html', {'courses': courses})

def coursePage(request, slug):
    course = Course.objects.get(slug = slug)
    serial_number = request.GET.get('lecture')
    videos = course.video_set.all().order_by("serial_number")
    if serial_number is None:
        serial_number = 1

    video = Video.objects.get(serial_number = serial_number , course = course)
   
    if (video.is_preview is False):
        if request.user.is_authenticated is False:
            return redirect("login")
        else:
            user = request.user 
            try:
                user_course = UserCourse.objects.get(user = user , course = course)
            except:
                return redirect("checkout", slug = course.slug )


    context = {
         "course": course ,
         "video" : video ,
         "videos" : videos
    }
    return render(request, 'course_page.html', context )


class SignupView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "signup.html" , {'form' : form})

    def post(self, request):
        form = RegistrationForm(request.POST)

        if(form.is_valid()):
            user = form.save()
            if(user is not None):
                return redirect("login")

        return render(request, "signup.html" , {'form' : form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = { "form" : form }

        return render(request, "login.html", context)

    def post(self, request):
        form = LoginForm( request = request, data = request.POST)
        context = { "form" : form }
        if(form.is_valid()):
            return redirect("home")

        return render(request, "login.html" , context)


def signout(request):
    logout(request)
    return redirect("home")

from Educational_Institute.settings import KEY_ID , KEY_SECRET

import razorpay
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


def checkout(request, slug):
    course = Course.objects.get(slug = slug)
    user = None

    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    action = request.GET.get('action')
    order = None
    payment = None
    error = None

    if action == 'create_payment':
        try:
            user_course = UserCourse.objects.get(user = user , course = course)
            error = "You are already inrolled in course!"
        except:
            pass

        if error is None:
            amount = int((course.price) * 100)
            currency = "INR"
            notes = { 
            "email" : user.email
            }
            receipt = f"MyInstitute-{int(time())}"
            order = client.order.create({'receipt' : receipt , 'notes': notes , 'amount' : amount , 'currency' :  currency})

            payment = Payment()
            payment.user = user
            payment.course = course
            payment.order_id = order.get('id')
            payment.save()

    context = {
         "course" : course ,
         "order" : order ,
         "payment" : payment ,
         "user" : user ,
         "error" : error ,
    }
    return render(request, 'check_out.html', context)

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = request.POST
        context = {}
        print(data)
        try:    
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            userCourse = UserCourse(user = payment.user , course = payment.course)
            userCourse.save()

            print("Usercourse" , userCourse.id)

            payment.user_course = userCourse
            payment.save()

            return render(request, "my_courses.html", context)

        except:
            return HttpResponse("Invalid Payment Details")


@login_required(login_url="login")
def mycourses(request):
    user = request.user 
    user_courses = UserCourse.objects.filter(user = user)
    context = {
        'user_courses' : user_courses

    }
    return render(request, "my_courses.html" , context)
