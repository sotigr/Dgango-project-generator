import sys 
import os
import os.path
def add_line(file, search, newline):
	with open(file, "r") as in_file:
		buf = in_file.readlines()

	with open(file, "w") as out_file:
		for line in buf:
			if line == search+"\n":
				line = line + newline +	"\n"
			out_file.write(line)	

def add(file, search, newline):
	with open(file, "r") as in_file:
		buf = in_file.readlines()

	with open(file, "w") as out_file:
		for line in buf: 
			if line == search + "\n":
				line = line[:-1] + newline + "\n"
			out_file.write(line)	

def create_file(file, text):
		with open(file, "w") as out_file:
			out_file.write(text)

def append_file(file, text):
	with open(file, "a") as out_file:
   		out_file.write(text)

def preppend_file(file, text):
	with open(file, 'r') as original: data = original.read()
	with open(file, "w") as out_file:
   		out_file.write(text + "\n" + data)

#####################################
# View creation script
#####################################


target_controller = input("Enter target controller name: ")
view_name = input("Enter view name: ")

print("Configuring controller")
controller_path =  app_name + "/controllers/" + target_controller + ".py"
if not os.path.isfile(controller_path):
	make_controller = input("The specified controller does not exist. Create a new one?(y/n)")
	if make_controller != "y":
		exit()
	else:
		create_file(controller_path, """
from django.http import HttpResponse
from django.shortcuts import render
		""")
else:
	pass

print("Creating view html file")
os.makedirs(app_name + "/templates/partial/" + target_controller)
view_path = app_name + "/templates/partial/" + target_controller + "/" + view_name + ".html"
create_file(view_path, """
{% extends 'shared/layout.html' %}

{% block content %}

<p>"""+view_name+"""</p>

{% endblock %}
""")

print("Creating controller action")
append_file(controller_path, """
def """+view_name+"""(request):
	return render(request, 'partial/"""+target_controller+"""/"""+view_name+""".html')
""")

print("Registering action in router")
urls_file_path = app_name + "/urls.py"
action_url = target_controller + "/" + view_name
add(urls_file_path, "urlpatterns = [", "\n	path('"+action_url+"', "+target_controller+"."+view_name+", name='"+ target_controller + "_" + view_name+"'),")
preppend_file(urls_file_path, "from .controllers import " + target_controller)

print("Done.")