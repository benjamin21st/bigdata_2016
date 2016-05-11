# bigdata_2016
## 1. Setup Flask
Make sure you are using `python 2.x`.

### Setup virtual environment
You can setup the virtual environment by typing: `virtualenv env`.

### Activate virtual environment
In the directory where you have a `env` folder, type:
`source env/bin/activate`.

### Install dependencies
Once you have activated your virtual environment, in the `server` directory, type:
`pip install -r requirements.txt`

### Create local configuration file
Under `server` directory, use the template `local_config.tpl` to create a python file called `local_config.py`. You may edit the information in this file for your system needs. Especially anything that concerns ***password***.


## 2. Setup Database
### Setup MySQL
Make sure you have mysql installed, to check that type in your command line: `mysql ` or `which mysql`;

### Setup database
Enter your MySQL command line to create the database we will use to connect to:
`mysql`
OR
`mysql -p`
Depends on your MySQL settings.

Then, type `show databases;` and check if you already have a database named `trip_fare`.

If not, type:
`create database trip_fare;`

Otherwise, proceed to next step of the setup.

### Connect to MySQL database
As long as your settings in 'local_config.py' is correct, your app should be automatically connected to the database at runtime.

### Database migration
Under `server`, if you don't have a folder named `migrations`, then run this command:
`python manage.py db init`
Once you have the folder `migrations`, run this command to make sure your database schema is updated:
`python manage.py db migrate`
`python manage.py db upgrade`

## 3. Update database schema
Database schema is updated through the 'models.py' file, NOT from inside MySQL. This provides a convenient way of keep tracking on our database changes over time, plus writing python code is more comfy.

Once you edited any class that has `__tablename__` and any of its attribute that has `Column` in it inside 'models.py', you need to wrong the migration command in the last section ***Database Migration***.


## 4. Develop
### Basic save operations to database
First you need to import the models.py module;

Then you can create an instance of a class in `models.py` by typing:
`foo = Foo()`

If this class has additional attributes, type in:
`foo = Foo(attr1=val1, attr2=val2)`

Then save this instance to database using:
`foo.save()`

You may want to put the saving operation inside a `try ... except ... ` block in case some data violates the rules of the schema setting.

A working example would be:
```python
foo = Foo(attr1=val1, attr2=val2)
try:
    foo.save()
except:
    # Roll back database transaction in case it blocks future operations
    session.rollback()
    print "Oops, something went terribly wrong"
```


### Basic routing and views
Run
`python views.py`
And open up [localhost:5000](localhost:5000), you should see a basic print out.

And if you head over to [localhost:5000/trips/count](localhost:5000/trips/count)

Note that currently it only supports serving from port 5000, this will be updated later.

## 5. API access
Once you have database and python dependencies set up. These are the endpoints you can request for data (Everywhere that has "yellow" can be replaced to "green" ):
 * /trips/count
 * /tripstats
  * /tripstats/yellow
   * /tripstats/yellow?count
   * /tripstats/yellow?interval=monthly
  * /tripstats/dist/yellow?range=year
  * /tripstats/passengers/yellow?range=year
   * /tripstats/passengers/yellow?range=month
   * /tripstats/passengers/yellow?range=day
 * /spatialstats
