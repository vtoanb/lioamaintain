from django.shortcuts import render
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponse
import arrow
import json

from django_social_app.models import *
from django.utils import timezone
from datetime import datetime,timedelta

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

#for sort dictionary
import operator



def maintainlist(request):

    now = timezone.localtime(timezone.now())

    maintain_sch = maintain_schedule.objects.all()
    maintain_his             = maintain_history.objects.filter(maintain_approve=True).order_by('-maintain_approve_time')[:10]
    maintain_his_not_approve = maintain_history.objects.filter(maintain_approve=False).order_by('-maintain_raise_time')

    """ try to implement model to custome page """
    machines = machine.objects.all()
    default_machine = machine.objects.get(pk="1")
    staffs = staff.objects.all()
    maintains = maintain_schedule.objects.all()

    """ create list for maintain """
    maintain_machines = maintain_schedule.objects.all().prefetch_related('machine').order_by('machine__machine_name')
    x = []
    for m in maintain_machines:
        timedif = m.maintain_time - now
        timedif = timedif.days * 24 + timedif.seconds // 3600
        x.append((m.machine.machine_name,m.maintain_type,timedif))

    """ create list for production counter
        with data: machine_name date_range counter_size*5
        this list to generate header of table for all machines
        and use Jquery to complete details by user
    """



    return render(request, 'maintainlist.html',{
        'maintain_schedule' : maintain_sch,
        'maintain_history'  : maintain_his,
        'not_approve_history' : maintain_his_not_approve,
        'machines':machines,
        'staffs':staffs,
        'maintains':maintains,
        'time': now,
        'default_machine':default_machine,
        'x':x,
        })


def home(request):
    return render_to_response('home.html')


def logout(request):
    auth_logout(request)
    return redirect('/')

"""
class AnalyticsIndexView(TemplateView):
    template_name = 'jscharttoan.html'

    def get_context_data(self, **kwargs):
        context = super(AnalyticsIndexView, self).get_context_data(**kwargs)
        context['30_day_registrations'] = self.thirty_day_registrations()
        return context

    def thirty_day_registrations(self):
        final_data = []

        date = arrow.now()
        for day in range(1, 30):
            date = date.replace(days=-1)
            count = User.objects.filter(
                date_joined__gte=date.floor('day').datetime,
                date_joined__lte=date.ceil('day').datetime).count()
            final_data.append(count)

        return final_data
"""

def viewajaxtest(request):
    if request.method == 'POST':
        post_text = request.POST.get('ajax_test')
        response_data = {}

        #post = Post(text=post_text, author=request.user)
        #post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = 'num'
        response_data['text'] = post_text
        response_data['created'] = 'date'
        response_data['author'] = 'that is me'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def viewajaxupdate(request):
    response_data = {}
    now = timezone.localtime(timezone.now())

    if request.method == 'POST':
        post_text = request.POST.get('ajax_dat')
        response_data['server_time'] = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

    if request.method == 'GET':
        response_data = {}
        response_data['server_time'] = str(now.minute) + ":" + str(now.second)


    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

def getLatest30DaysEnergy(request):
    response_data = []
    now = timezone.localtime(timezone.now())

    if request.method == 'POST':
        machine = request.POST.get('ajax_machine_name')

        counter30Days = counter_history.objects.filter(machine__machine_name=machine).order_by('-pk')[:7]

        for counterDat in counter30Days:
            dictkey = str(counterDat.save_time.day)+"/"+\
                      str(counterDat.save_time.month)+"/"+\
                      str(counterDat.save_time.year)+":"+\
                      str(counterDat.energy)+":"+\
                      str(counterDat.counter)

            response_data.append(dictkey)

    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

def getPrevDay(request):
    response_data = []

    if request.method == 'POST':
        machine = request.POST.get('machine_name')
        date,month,year = request.POST.get('rDate'),request.POST.get('rMonth'),request.POST.get('rYear')
        qDate = datetime(int(year),int(month),int(date)) - timedelta(days=1)
        print(qDate.year)
        query = counter_history.objects.filter(machine__machine_name=machine,\
                                                save_time__year=qDate.year,\
                                                save_time__month=qDate.month,\
                                                save_time__day=qDate.day)

        for q in query:
            res = str(q.save_time.day) + ":" +\
                  str(q.save_time.month) + ":" +\
                  str(q.save_time.year) + ":" +\
                  str(q.energy) + ":" +\
                  str(q.counter)
            response_data.append(res)
            print(res)
        print(response_data)

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
        )

def getFirstMonth(request):
    response_data = []
    now = timezone.localtime(timezone.now())

    if request.method == 'POST':
        machine = request.POST.get('ajax_machine_name')
        year = request.POST.get('year')
        month = request.POST.get('month')

        counter30Days = counter_history.objects.filter(machine__machine_name=machine,\
                                                       save_time__year = year,\
                                                       save_time__month = month).order_by('-pk')[:15]

        for counterDat in counter30Days:
            dictkey = str(counterDat.save_time.day)+"/"+\
                      str(counterDat.save_time.month)+"/"+\
                      str(counterDat.save_time.year)+":"+\
                      str(counterDat.energy)+":"+\
                      str(counterDat.counter)

            response_data.append(dictkey)

    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

""" function for maintaining """
@login_required
def getDoMaintain(request):
    response_data = {}
    response_data["status"] = "fail"
    if request.method == "POST":
        machine_name = request.POST.get("machine_name")
        maintain_type = request.POST.get("maintain_type")
        user_name = request.POST.get("user_name")
        ajax_comment = request.POST.get("comment")
        print("---->",user_name, ajax_comment)
        #check if maintain request exist
        maintain_items = maintain_schedule.objects.filter(machine__machine_name = machine_name,\
                                                         maintain_type = maintain_type,\
                                                        )
        for maintain in maintain_items:
            print(maintain.machine.machine_name)

        if maintain_items:
            for maintain_item in maintain_items:
                #check this item exist in maintain_history
                exist_item = maintain_history.objects.filter(machine__machine_name = maintain_item.machine.machine_name,\
                                                             maintain_type = maintain_item.maintain_type,\
                                                             maintain_time = maintain_item.maintain_time,\
                                                             maintain_approve = False,)
                if exist_item:
                    response_data["status"] = "exist"
                else:
                    response_data["status"] = "saved"
                    machine_obj = machine.objects.get(machine_name=machine_name)

                    b = maintain_history(machine = machine_obj,\
                                         maintain_type = maintain_type,\
                                         maintainer = user_name,\
                                         maintain_time = maintain_item.maintain_time,\
                                         comment = ajax_comment,\
                                         maintain_raise_time = timezone.localtime(timezone.now()),\
                        )
                    b.save()

    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
@login_required
def updateMaintain(request):
    response_data = "fail"
    if request.method == "POST":
        command = request.POST.get("command")
        if command == "approve":
            machine_name = request.POST.get("machine_name")
            maintain_type = request.POST.get("type")
            user_name = request.POST.get("user_name")
            approver = request.POST.get("approver")

            #check approver is manager or not
            auth = staff.objects.get(username = user_name,manager = True)
            if auth:
                # check exist in database
                item = maintain_history.objects.get(machine__machine_name = machine_name,\
                                                    maintain_type = maintain_type,\
                                                    maintainer = user_name,\
                                                    maintain_approve = False)

                if item:
                    maintain_history.objects.filter(pk=item.pk).update(
                                                    approver = approver,\
                                                    maintain_approve = True,\
                                                    maintain_approve_time = timezone.localtime(timezone.now()),\
                                                    )
                    #update maintain schedule
                    schedule = maintain_schedule.objects.get(machine__machine_name = machine_name,\
                                                             maintain_type = maintain_type,
                                                            )
                    new_maintain_time = timezone.localtime(timezone.now()) + timedelta(hours=int(maintain_type))
                    maintain_schedule.objects.filter(pk=schedule.pk).update(maintain_time=new_maintain_time,\
                                                                            maintain_time_remain=maintain_type)

                    response_data = "success"
            else:
                response_data = "auth_fail"

        elif command == "delete":
            machine_name = request.POST.get("machine_name")
            maintain_type = request.POST.get("type")
            user_name = request.POST.get("user_name")
            delete_user = request.POST.get("delete_user")

            #check if delete user create this
            maintain_history.objects.get(machine__machine_name = machine_name,\
                                                maintain_type = maintain_type,\
                                                maintainer = delete_user,\
                                                maintain_approve = False).delete()



            response_data = "success"

    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def updateTable(request):
    response_data = []

    if request.method == 'POST':
        maintainer = request.POST.get('maintainer_filter')
        machine = request.POST.get('machine_filter')
        maintain_type = request.POST.get('type_filter')
        approver = request.POST.get('approver_filter')
        items = request.POST.get('items_filter')


        qs = maintain_history.objects.filter(
                                            maintain_approve = True,\
                                            machine__machine_name__icontains = str(machine),\
                                            approver__icontains = str(approver),\
                                            maintainer__icontains = str(maintainer),\
                                            maintain_type__icontains = maintain_type,\
                                             ).order_by('-maintain_approve_time')[:int(items)]

        for q in qs:
            i = [q.maintainer,q.machine.machine_name,q.maintain_type,q.approver,q.comment,str(q.maintain_time),str(q.maintain_raise_time),str(q.maintain_approve_time)]
            response_data.append(i)

    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

def ajaxloginview(request):
    response_data = []

    request.session.set_test_cookie()

    if request.method == 'POST':
        user_name = request.POST.get('user')
        password = request.POST.get('password')

        user = authenticate(username=user_name,password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                response_data.append("logged in")
            else:
                # return a disabled account
                response_data.append("disabled")
        else:
            response_data.append("error")


    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
