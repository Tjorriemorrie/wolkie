#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import cgi
import jinja2
from faker import Factory
import random
import math
import MySQLdb
from google.appengine.api import taskqueue
import json
import time

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
fake = Factory.create('en_US')


class MainHandler(webapp2.RequestHandler):
    def get(self):
        #output the template. no values for now. just the plain html
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.out.write(template.render())


class GenerateTransactions(webapp2.RequestHandler):
    def post(self):
        #Get form params
        numCustomers = int(self.request.get('numCustomer'))
        minTransactions = int(self.request.get('minTransactions'))
        maxTransactions = int(self.request.get('maxTransactions'))

        #execute a task queue
        for i in range(math.ceil(numCustomers / 10000)):
            taskqueue.add(url='/worker', params={
                'numCustomer': numCustomers,
                'minTransactions': minTransactions,
                'maxTransactions': maxTransactions,
                'id': id
            })

        template_values = {
            'numCustomers': self.request.get('numCustomer'),
        }

        template = JINJA_ENVIRONMENT.get_template('process.html')
        self.response.write(template.render(template_values))


class TransactionWorker(webapp2.RequestHandler):
    def post(self):
        #Get form params
        id = int(self.request.get('id'))
        numCustomers = int(self.request.get('numCustomer'))
        minTransactions = int(self.request.get('minTransactions'))
        maxTransactions = int(self.request.get('maxTransactions'))

        #Connect to MySQL
        if (os.getenv('SERVER_SOFTWARE') and
                os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
            db = MySQLdb.connect(unix_socket='/cloudsql/modus-kyc:cutsomer', user='root', passwd='M0du5Gr0up', db='kyc')
        else:
            db = MySQLdb.connect(host='localhost', user='root', db='kyc')

        db.autocommit(False)

        # clearTables(db)

        for i in range(10000):
            id += i
            customer = genCustomer(id)
            insertIntoTable(db, 'customer', customer)
            print "Customer Generated. ID: " + str(id)

            #random number of transactions
            numTransactions = random.randint(minTransactions, maxTransactions)
            for x in range(numTransactions):
                transaction = genTransaction(id)
                insertIntoTable(db, 'transactions', transaction)

            #random number of docs
            numDocuments = random.randint(1, 7)
            for y in range(numDocuments):
                document = genDocument(id)
                insertIntoTable(db, 'documents', document)

        db.commit()


class Preview(webapp2.RequestHandler):
    def get(self):
        customer = genCustomer(1)
        transaction = genTransaction(1, 1)
        document = genDocument(1, 1)

        template_values = {
            'customer': customer,
            'transaction': transaction,
            'document': document,
        }

        template = JINJA_ENVIRONMENT.get_template('preview.html')
        self.response.write(template.render(template_values))


class Poll(webapp2.RequestHandler):
    def get(self):

        #Connect to MySQL
        if (os.getenv('SERVER_SOFTWARE') and
                os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
            db = MySQLdb.connect(unix_socket='/cloudsql/modus-kyc:cutsomer', user='root', passwd='M0du5Gr0up', db='kyc')
        else:
            db = MySQLdb.connect(host='localhost', user='root', db='kyc')

        cursor = db.cursor()
        query = "SELECT COUNT(id) FROM customer"
        cursor.execute(query)
        pollNum = cursor.fetchone()
        self.response.write(json.dumps(pollNum))


def insertIntoTable(db, table, data):
    #Insert a result
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = "INSERT into %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)
    cursor = db.cursor()
    try:
        cursor.execute(sql, data.values())
    except Exception, e:
        print e
        print cursor._last_executed


def clearTables(db):
    cursor = db.cursor()
    cursor.execute('truncate table customer')
    cursor.execute('truncate table transactions')
    cursor.execute('truncate table documents')
    db.commit()


def genCustomer(id):
    maritalStatus = ['married', 'single', 'divorced']
    gender = ['male', 'female']

    customer = {
        'name': fake.name(),
        'id': id,
        'marital_status': random.choice(maritalStatus),
        'gender': random.choice(gender),
        'dob': fake.date_time_this_century(),
        'email': fake.company_email(),
        'phone': fake.phone_number(),
        'country_of_residence': 'US',
        'title': fake.prefix(),
        'name_first': fake.first_name(),
        'name_last': fake.last_name(),
        'lat': fake.latitude(),
        'lon': fake.longitude(),
        'address': fake.address(),
        'city': fake.city_prefix() + ' ' + fake.city_suffix(),
        'state': fake.state(),
        'zipcode': fake.postcode(),
        'job_title': fake.job(),
        'employer': fake.company(),
        'credit': random.choice([True, False]),
        'savings': random.choice([True, False]),
        'cheque': random.choice([True, False]),
        'mortgage': random.choice([True, False]),
        'completeness': random.choice([True, False]),
        'credit_score': random.randint(400, 600),
        'lifetime_value': random.randint(1, 1000),
        'customer_since': fake.date_time_between(start_date="-30y", end_date="now"),
    }

    return customer


def genTransaction(id):
    accounts = ['Checking', 'Credit Card', 'Savings']
    type = ['Wire Transfer', 'Credit Card', 'Internal Transfer', 'ACH Transfer']
    amount = random.randrange(-99999, 9999)
    country = None if random.random() < 0.10 else fake.country()
    transaction = {
        'transaction_date': fake.date_time(),
        'transaction_customer_id': int(id),
        'account': random.choice(accounts),
        'type': random.choice(type),
        'title': fake.company(),
        'amount_in': None if amount <= 0 else abs(amount),
        'amount_out': None if amount > 0 else abs(amount),
        'amount': abs(amount),
        'country': country,
        'international': True if country else False,
    }
    return transaction


def genDocument(id):
    titles = ['Photo ID', 'Proof of Address', 'Signature Card']
    title = random.choice(titles)
    document = {
        'customer_id': int(id),
        'title': title,
        'image_url': '/assets/doc/' + str(id) + '/' + title + '.jpg',
        'upload_date': fake.date_time(),
    }
    return document


app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/generate', GenerateTransactions),
                                  ('/preview', Preview),
                                  ('/worker', TransactionWorker),
                                  ('/poll', Poll),
                              ], debug=True)
