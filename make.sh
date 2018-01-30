#!/bin/bash
echo "###################################################"
echo "#  Python and Django project template generator.  #"
echo "###################################################"

echo "" 

echo "Python version:" 
python3 -c "import sys; print(sys.version)"

echo "" 

echo "Django version:"
python3 -c "import django; print(django.get_version())"

echo "" 

read -p "Project name:" project_name

django-admin startproject $project_name

read -p "Enter application name:" app_name

cd $project_name

python3 manage.py startapp $app_name

cd ..
 
echo "Modifying and linking the site with the application..."
echo ""

python3 make.py $project_name $app_name

echo "Finished."
echo ""

read -p "Do you want to create a python environment? (y/n)" crenv
if [ $crenv == "y" ]; then
	cd $project_name
	BASEDIR=$(dirname "$0")
	echo $BASEDIR
	python3 -m venv "$BASEDIR"
	source bin/activate
	pip install --upgrade pip
	pip install Django
	pip install faker
	pip install django-meta
	pip install pythonql3
	read -p "Run migrations? (y/n)" migrate
	if [ $migrate == "y" ]; then
		python3 manage.py makemigrations
		python3 manage.py migrate
		read -p "Create superuser? (y/n)" csu
		if [ $csu == "y" ]; then
			python3 manage.py createsuperuser
		fi
	fi
fi

cd ..

echo ""
echo "Done."
