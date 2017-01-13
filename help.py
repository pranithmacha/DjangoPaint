=========================================
        Django settings
=========================================

# to import local settings into main settings file
# override any settings values in local settings file
try:
    from <appname>.localsettings import *
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
            django models     
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


