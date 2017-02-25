===========================
          URLS
===========================

# url to home/landing page
    url(r'^$', 'mysite.views.home', name='home'),


# include urls from other apps
    url(r'^students/',include('students.urls')),

# include urls based on condition 
    from django.conf import settings

    ''' check if settings has attribute and if the attribute value is true
    if hasattr(settings, "MY_SETTINGS") and MY_SETTINGS:
        urlpatterns += patterns(
             url(r'^teachers/', include('library.urls')),
             url(r'^logout/$', 'teachers.views.logout',
        )
    else:
        # include some other urls

# pass view name in pattern 

    ''' all urls in this pattern point to students.views, removes redundancy of appname.viewname for each and every   url '''
    urlpatterns = patterns('students.views',
                           url(r'^$', 'get_student_name', name='student_name'),
    )

# using slug and regex pattern

    '''  accepts username/user_uuid, only letters lowercase and uppercase, numbers and hiphen are accepted '''
    url(r'^change_username/(?P<user_uuid>[a-zA-Z0-9\-]+)/$',
                                'update_username', name='update_username'),
    ''' corresponding view that accepts user_uuid '''                            
    def update_username(request, user_uuid=None):

# pass template name in url. This exmaple also shows how to use django auth login url
     url(r'^login/$', 'django.contrib.auth.views.login',
            {'template_name': 'login.html'}, name='login'),
        )



=========================================
        Django settings
=========================================

# to import local settings into main settings file
# override any settings values in local settings file
try:
    from <main_appname>.localsettings import *
except ImportError:
    print("WARNING: localsettings.py not detected! these settings are only suitable for local dev!")


# to import settings into any python module in a django app
from django.conf import settings
usage - print(settings.XXXXX)


# logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(request_id)s %(levelname)-8s %(asctime)s %(lineno)s %(name)s] %(message)s'
        },
        'simple': {
            'format': '[%(request_id)s %(levelname)-8s] %(message)s'
        },
    },
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'verbose'
        },
        'myprojectlogfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filters': ['request_id'],
            'formatter': 'verbose',
            'filename': 'myproject.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['console', 'myproject_logfile'],
            'level': 'INFO',
        },
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'analysis',
        'USER': 'root',
        'PASSWORD': 'xxxxxx',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


==============================================
               Migrations
==============================================

# fixtures, data to be loaded into db. usually json
fixtures should be placed under folder "fixtures" under the each app directory 
python manage.py dumpdata > db.json (to create a fixture)
fixture can be create for a specifig app as well


# to load db data from json file
python manage.py loaddata <json file>

# to create a migration file based on models.py
python manage.py makemigrations

# to create an empty migration file
python manage.py makemigrations --empty yourappname
(creates an empty migration file under the app's migrations folder)

# example migration file and load data from migrations

from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings
import country

# apps, schema_editor are mandatory parameters 
def load_stores_from_fixture(apps, schema_editor):
    from django.core.management import call_command
    if 'test' in country.argv:
        pass
    elif settings.ENVIRONMENT == 'DEV':
        # invoke a Django command. loaddata in this case
        # finds a file with the name in the current app
        call_command("loaddata", "locations_dev")
    elif settings.ENVIRONMENT == 'PROD':
        call_command("loaddata", "locations_prod")


class Migration(migrations.Migration):
    # dependcies, app name and name of previous migration file
    dependencies = [
        ('broker', '0002_auto_20160829_1007'),
    ]
    # operations, the functions that need to be executed when this migration file is run
    operations = [
        # create a database table, create model class with same name in models to query like a class object
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.ForeignKey(to='.Location')),
                ('subject_name', models.CharField(help_text=b'subject name', null=True, max_length=255)),
                ('gender', models.CharField(help_text=b'gender', null=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        # run a python function from migrations
        migrations.RunPython(load_stores_from_fixture),
        # run a sql query from migration 
        # requires pip install sqlparse==0.2.2 (not sure)
        migrations.RunSQL("INSERT INTO studentdb_student(name) VALUES ('asdsa');"),
        # rename a model
        # old name, new name
        migrations.RenameModel('OldModelName', 'NewModelName'),
        # rename a column 
        # model name, old column name, new column name
        migrations.RenameField('ModelName', 'old_field_name', 'new_field_name'),
        # add field to a model
        migrations.AddField(
            model_name='model_name',
            name='field_name',
            field=models.ForeignKey(to='studentdb.ParentInfo'),
            preserve_default=True,
        ),
        # combination uniqueness of columns
        # combination will be unique, not individual columns
        migrations.AlterUniqueTogether(
            name='model_name',
            unique_together=set([('field_one', 'field_two')]),
        ),
        # alter existing column
        migrations.AlterField(
            model_name='modelname',
            name='column_name',
            field=models.CharField(help_text=b'this is help text. is it helpful?', max_length=50),
            preserve_default=True,
        ),
        # delete existing column
        migrations.RemoveField(
            model_name='model_name',
            name='column_name/field_name',
        ),
    ]

# cleanup data from old tables and create new tables and new columns in existing tables

def old_data_cleanup(apps, schema_editor):
    help_text = """
    This migration will delete all the old data and create new schema with updated tables and columns
    Choose yes to continue migrations. Database will be updated.
    Choose no to exit migrations. No changes will be made and database will remain in current state
    """
    print("Running this migration will delete all the data from tables belonging to xyz app")
    choice = None
    while not choice:
        choice = raw_input("Type 'yes to continue or 'no' to exit migrations. Type 'help' for more details. ")
        if choice == "yes" or choice == "no":
            break
        elif choice == "help":
            print(help_text)
        choice = None
    if choice == "yes":
        # gets old models from  app 
        all_models = apps.all_models.get("xyz")
        for name, model_class in all_models.items():
            obj = model_class
            # deletes all the data from tables corresponding to models 
            obj.objects.all().delete()
    elif choice == "no":
        print("exiting migrations....")
        raise Exception("exiting migrations")


class Migration(migrations.Migration):

    dependencies = [
        ('xyz', '0024_auto_20150730_1744'),
    ]

    operations = [
        migrations.RunPython(old_data_cleanup)
    ]

# to insert data into tables using models from migrations

from django.db import models, migrations


def insert_person_names(apps, schema_editor):
    Person = apps.get_model("app_name", "Person")
    person_one = Person(name="Teja")
    person_one.save()
    person_two = Person(name="Pranith")
    person_two.save()

# squash migrations to combine multiple migrations into one 
# as of Django 1.7, we can only squash migrations from first migration to a particular migration
# learn more about squashing

 
===============================================
  creating cutom executable django commands
===============================================

# custom commands should be placed under management/commands directory under individual app
polls/
    __init__.py
    models.py
    management/
        __init__.py
        commands/
            __init__.py
            _private.py
            closepoll.py
    tests.py
    views.py


closepoll.py    
=======
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    '''Command'''
    def handle(self, *args, **options):
        try:
            # these functions are not declared in the same class(Command)
            function_one()
            function_two()

        except Exception as exception:
            log.exception(exception)


def function_one():
    # function logic
    pass

def function_two():
    #function logic
    pass

# executing custom commands
python manage.py <module name containing command> <paramenters separated by space>
eg: if we want to create a "command insert_data_into_table", create a module "command insert_data_into_table.py" under commands directory. This module should contain Command class implementation


============================================
                 MODELS     
============================================

# getting objects by primary key
all_locations = Location.objects.get(pk__in=location_id_set)
all_locations = Location.objects.get(pk=location_id)

# django models filtering results 
class Person(modles.Model):
    
persons = Person.objects.filter(last_name="xyz")\


# create a model and foreign keys relationships
class Student(models.Model):
    location = models.ForeignKey('Location')
    gender = models.CharField(null=True, max_length=255, unique=False)
    first_name = models.CharField(null=True, max_length=255, help_text="this is blah blah!")
    last_naame = models.CharField(null=True, max_length=255)


class Location(models.Model):
    country = models.IntegerField(null=True, max_length=4)
    state = models.IntegerField(null=True, max_length=4)
    city = models.IntegerField(null=True, max_length=4)

    class Meta:
        ordering = ['country']
        unique_together = (('country', 'state', 'city'),)

    def __unicode__(self):
        """String representation."""
        return u"country: {0:s}  state: {1:s} city: {2:s}".format(self.country, self.state, self.city)
                                                                         

# filtering by foreign key values, using "in"
students = Student.objects.filter(location__country=country, location__state=state,
                                            location__city__in=[city, 0], eqp_protocol_aiu=eqp_protocol_aiu,
                                            gender__in=['F', 'M'],
                                            age__in=headends)
                                            
 # using contains to filter                                           
 students = Student.objects.filter(name__contains='XYZ{0}ABC'.format(name)) 

 # referencing foreign key attributes
 for student in students:
     country = student.location.country          

==========================================
                 PIP
==========================================
# install one requirement
pip install requirement_name==version
pip install requests==2.4.1

# install from a remote location
pip install -e svn+https://xyz.lol.rofl.net/projects/my_project/trunk/sadath@147732#egg=sadath


# pip install from file
pip install -r requirements.txt
=====
requirements.txt
=====
spyne==2.11.0
sqlparse==0.2.2
suds==0.4
-e svn+https://xyz.lol.rofl.net/projects/my_project/trunk/sadath@147732#egg=tds_proxyauth


=================================
     DATABASE CONNECTIONS
=================================

Oracle
------
import cx_Oracle

query = ""
with cx_Oracle.connect('username/password@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=127.0.0.1)'
                                     '(PORT=1533))(CONNECT_DATA=(SERVICE_NAME = service name)))') as conn:
cursor = conn.cursor()
cursor.execute(query, kwargs)
desc = [d[0] for d in cur.description]
results = [dict(zip(desc, row)) for row in cur]
return results


Oracle Singleton
----------------
class OracleClient:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class OracleClientSingleton(OracleClient):
    def __init__(self):
        OracleClient.__init__(self)
        if not self.__dict__.get("cursor"):
            # print("creating new cursor...")
            conn = cx_Oracle.connect('conn details')
            cursor = conn.cursor()
            # print("cursor id when created "+str(id(cursor)))
            self.__dict__["cursor"] = cursor
            self.__dict__["connection"] = conn

    def dict_query(self, query, **kwargs):
        cur = self.__dict__.get("cursor")
        try:
            cur.execute(query, kwargs)
            desc = [d[0] for d in cur.description]
            results = [dict(zip(desc, row)) for row in cur]

            return results
        except Exception as e:
            print("error while executing query")
            print(e)

    def close_cursor(self):
        self.__dict__.get("cursor").close()
        self.__dict__.get("connection").close()
        self.__dict__.clear()
        # print("closed and removed oracle cursor and connection from cache")
        try:
            self.__dict__["cursor"]
        except KeyError:
            pass
            # print("could not find the cursor. Implies - closed ")


=====================
        AUTH
=====================

############ basic auth #############
#have url for login to return login page
# name attribute should be set so that reverse url lookup can be done using name


---- in urls ----
url(r'^login/$', TemplateView.as_view(template_name='login.html'), name='login')

--- in views ----
from django.shortcuts import (render, reverse, HttpResponseRedirect)
from django.contrib.auth.decorators import login_required

''' method one - use is_authenticated '''
# use reverse for reverse usl lookup by name
def home(request):
    if request.user.is_authenticated():
        return render(request, "home.html", {})
    else:
        return HttpResponseRedirect(reverse("login"))


''' method two - use login required decorator'''
# by default looks for LOGIN_URL attribute in settings.py
@login_required
def home(request):
    return render(request, "home.html", {})
    
    
    
--- in settings.py ---
# using reverse instead of reverse_lazy causes an exception since the apps are not loaded at the point of executing settings
#    raise AppRegistryNotReady("Apps aren't loaded yet.")
# django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.

from django.urls import reverse_lazy
LOGIN_URL = reverse_lazy('login')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]

AUTH_USER_MODEL = 'auth.User'
# redirects to this url when successfully authenticated
LOGIN_REDIRECT_URL = ''



####### end basic auth  ##############


# auth for home page 
# decorator login required redirects if user is not logged in 
@login_required()
def home(request):
    template_name = "welcome.html"
    context = dict()
    user_uuid = request.user.user_uuid
     if isinstance(user, User):
        if ('mysession_key' not in request.session.keys() or 
             request.session['mysession_key'] == None):
             request.session['myseesion_key'] = 'my session key'
             return render(request, template_name, context)
     else:
         return render(request, 'usernotfound.html')


# logout 
# exempts csrf token since logging out
@csrf_exempt
def logout(request):
    response = HttpResponseRedirect(settings.LOGOUT_URL)
    response.delete_cookie(key="OldCookie")
    return response 


===============================================
        TEMPLATES AND STATIC FILES
===============================================        

# settings in settings.py. 
''' We can add more template folder locations in the tuple  '''
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),)

STATIC_ROOT = ''
STATIC_URL = '/static/'
''' We can add more static file dirs to the tuple '''
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'staticfiles'),)

# template folder structure. Create folder for templates belonging to specific app

templates
  app1_templates_folder
     app1_file1.html
     app1_file2.html
  app2_templates_folder
     app2_file1.html
     app2_file2.html
  common_template_file1.html
  common_template_file2.html

# find template in views.py. Add additional folder layers of exists 

app_specific_template = 'app1_templates_folder/app1_file1.html'
common_template = 'common_template_file1.html'

# static files folder structure

staticfiles
    js
    css
    images

# adding static files in templates 
<script type="text/javascript" src="{% get_static_prefix %}js/app.js"></script>
<link type="text/css" href="{% get_static_prefix %}css/bootstrap.min.css" rel="Stylesheet"/>


# base template 

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="viewport" content="width=device-width,initial-scale=1"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <title>{% block title %}  {% endblock %}</title>

{% load static %}
    
    <link type="text/css" href="{% get_static_prefix %}css/bootstrap.min.css" rel="Stylesheet"/>
    <link type="text/css" href="{% get_static_prefix %}css/datatables/dataTables.bootstrap.css" rel="Stylesheet"/>
   
    {% block extra_media %}
    <!-- additional media files go here -->
    {% endblock %}

</head>

<body>
{% block body %}
<div id="wrap">


{% block header %}

    <header>

    </header>

{% endblock %}

    <div class="page-container">

{% block base %} 

{% endblock %}

    </div> <!-- end page-container -->

{% block footer %}

  <footer class="residential">
   
  </footer>

{% endblock %}

<!-- end wrap -->
</div> 
{% endblock %}

</body>
</html>


# extending base template

{% extends 'base.html' %}
{% load url from future %}
{% load static %}

{% block base %}

{% endblock %}

# get url based on url name
<a class="{% block navbar_class-mngusr1 %}{% endblock %}" href="{% url 'students' %}">My Link</a>

# using if condition


                {% if user.is_authenticated %}
                    <li><a href="{% url 'logout' %}">Logout</a></li>
                {% else %}
                    <li> </li>
                {% endif %}


=========================
        HEADERS
=========================

# setting headers in request

django replaces all the letters with capital case letters and all hiphens with underscores and prefixes with "HTTP_" 

headers with other special characters will be ignores. only hiphens!!!

eg: MY_HEADER = "xyz"  will be ignores and cannot be found in the request
    MY_HEADER = "xyz" can be found as HTTP_MY_HEADER



===============================
        APACHE CONF
===============================


<Directory {{projectroot}}>
        Order deny,allow
        Deny from all
</Directory>

<VirtualHost *:80>
        ServerName {{ip address}}
        LogFormat "%t \"%{Host}i\" %h %u %l \"%r\" %>s %b %T %{pid}P" vhost_combined
        CustomLog {{django root | root folder created by running django-admin.py startproject}}/logs/access_log vhost_combined
        ErrorLog {{django root}}/logs/error_log
        DocumentRoot {{django root}}
        Alias /static/ {{django root}}/static/
        <Directory {{django root}}/static>
                Order deny,allow
                Allow from all
                Require all granted
        </Directory>
        Alias /robots.txt {{django root}}/static/robots.txt
        Alias /favicon.ico {{django root}}/static/favicon.ico

        WSGIDaemonProcess {{dummy daemon name | can be any name }} user=apache display-name={{any name}} python-path={{django root}}:{{virtual env root}}/lib/python2.7/site-packages
        WSGIScriptAlias / {{django root}}/{{django folder with settings.py and wsgi.py}}/wsgi.py
        <Directory {{django root}}/{{django folder with settings.py and wsgi.py}}/>
                WSGIProcessGroup {{dummy daemon name}}
                <Files wsgi.py>
                        Order deny,allow
                        Allow from all
                        Require all granted
                </Files>
        </Directory>

        LoadModule headers_module /etc/httpd/modules/mod_headers.so
        
        RequestHeader set NEW_HEADER tds.net early

        <IfModule mod_headers.c>
            RequestHeader set NEW_HEADER "beeeeebeeebeee" early
        </IfModule>
</VirtualHost>
