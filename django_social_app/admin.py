from django.contrib import admin
from django_social_app.models import staff, machine, maintain_schedule, energy_history, counter_history, maintain_history

class staffAdmin(admin.ModelAdmin):
	fields = ['username' ,'email','phone','manager']
	list_display = ('username','email','phone','manager')


class maintain_scheduleAdmin(admin.TabularInline):
	fields = ['maintain_type']
	model = maintain_schedule
	extra = 3

class machineAdmin(admin.ModelAdmin):
	fields = ['machine_name','created_date']
	list_display = ('machine_name','created_date')
	inlines = [maintain_scheduleAdmin]

class energy_historyAdmin(admin.ModelAdmin):
	fields = ['machine','save_time','energy']
	model = energy_history

class counter_historyAdmin(admin.ModelAdmin):
	fields = ['machine','save_time','counter','energy']
	model = counter_history

class maintain_historyAdmin(admin.ModelAdmin):
	fields = ['machine','comment','maintainer']
	model = maintain_history

admin.site.register(staff,staffAdmin)
admin.site.register(machine,machineAdmin)
admin.site.register(energy_history,energy_historyAdmin)
admin.site.register(counter_history,counter_historyAdmin)
admin.site.register(maintain_history,maintain_historyAdmin)

