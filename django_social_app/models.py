from django.db import models
from django.utils import timezone
from django.utils.timezone import utc
from django.core.signals import request_finished
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import timedelta
from django.contrib.auth.models import User

class time_variable(models.Model):
	last_update_maintain = models.DateTimeField(default=timezone.localtime(timezone.now()))

class machine(models.Model):
	machine_name = models.CharField(max_length=30)
	created_date = models.DateTimeField('created date')
	# total power of machine in present day
	#energy_today = models.IntegerField(default=0)

	counter_size = models.IntegerField(default=0)
	counter_size_2 = models.IntegerField(default=0)
	counter_size_3 = models.IntegerField(default=0)
	counter_size_4 = models.IntegerField(default=0)
	counter_size_5 = models.IntegerField(default=0)

	def __str__(self):
		return self.machine_name

	class meta:
		ordering = ['machine_name']




class energy_history(models.Model):
	machine = models.ForeignKey(machine, on_delete=models.CASCADE)
	energy = models.IntegerField()
	save_time = models.DateTimeField('energy save time')




class counter_history(models.Model):
	machine = models.ForeignKey(machine, on_delete=models.CASCADE)
	counter = models.IntegerField(default=0)
	counter_2 = models.IntegerField(default=0)
	counter_3 = models.IntegerField(default=0)
	counter_4 = models.IntegerField(default=0)
	counter_5 = models.IntegerField(default=0)
	energy = models.IntegerField()
	save_time = models.DateTimeField('counter save time')

	def __str__(self):
		return str(self.save_time)

class staff(models.Model):
	username = models.CharField(max_length = 30)
	manager = models.BooleanField()
	email = models.CharField(max_length=50)
	phone = models.CharField(max_length=15)


class maintain_history(models.Model):
	machine = models.ForeignKey(machine, on_delete=models.CASCADE)
	maintain_type = models.IntegerField()
	maintainer = models.CharField(max_length=30, default="")
	approver = models.CharField(max_length = 30,default="")
	maintain_approve_time = models.DateTimeField(default=timezone.localtime(timezone.now()))
	maintain_raise_time = models.DateTimeField(default=timezone.localtime(timezone.now()))
	maintain_time = models.DateTimeField(default=timezone.localtime(timezone.now()))
	comment = models.CharField(max_length=80,default="no comment")
	maintain_approve = models.BooleanField(default=False)

class maintain_schedule(models.Model):
	"manage maintain of all machines"
	machine = models.ForeignKey(machine, on_delete=models.CASCADE)
	maintain_time = models.DateTimeField(default=timezone.localtime(timezone.now()))
	maintain_type = models.IntegerField()
	maintain_time_remain = models.IntegerField(default=100)

	def updateTimeRemainning():
		now = timezone.localtime(timezone.now())
		maintains = maintain_schedule.objects.all()
		for maintain in maintains:
			timeremain = (maintain.maintain_time - now)
			maintain_remain_hours = timeremain.days*24 + timeremain.seconds//3600
			maintain_schedule.objects.filter(pk=maintain.id).update(maintain_time_remain=maintain_remain_hours)
			#print(maintain.machine.machine_name)

	class meta:
		ordering = ["machine"]



@receiver(pre_save, sender = staff, dispatch_uid="toanuidstaff")
def my_handlerStaff(sender ,instance , **kwargs):
	if instance.id:
		oldName = staff.objects.get(pk=instance.id)
		print("staff:   " + oldName.first_name)


@receiver(pre_save, sender = machine, dispatch_uid="toanuidmachine")
def my_handlerMachine(sender ,instance ,**kwargs):
	print("_____pre_save handler machine______")

@receiver(post_save, sender = maintain_schedule, dispatch_uid="toanuidmaintainschedule")
def my_handlerMaintainSchedule(sender, instance, **kwargs):
	if instance.id:
		now = timezone.localtime(timezone.now())
		getmaintaintype = maintain_schedule.objects.get(pk=instance.id)
		maintain_schedule.objects.filter(pk=instance.id).update(maintain_time_remain = getmaintaintype.maintain_type,
			                                                    maintain_time = now + timedelta(hours=getmaintaintype.maintain_type) )
		#get maintain_time of smallest maintain_type
		name = instance.machine.machine_name
		maintain_objs = maintain_schedule.objects.filter(machine__machine_name=name).order_by('maintain_type')
		for maintain_obj in maintain_objs:
			print(maintain_obj.maintain_type)

"""
@receiver(post_save, sender = staff, dispatch_uid="savestaffasuser")
def my_handerstaffuser(sender, instance, **kwargs):
	if instance.id:
		new_staff_member = staff.objects.get(pk=instance.id)
		user = User.objects.create_user(username=new_staff_member.username,\
										email = new_staff_member.email,\
										password)"""
