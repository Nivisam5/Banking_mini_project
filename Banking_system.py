import typer
import json
import uuid
from pprint import pprint
from typing import Dict
import random
from datetime import date
import logging

# Create and configure logger
logging.basicConfig(filename='/Users/hakunamatata/Documents/Python_assignments/python-oo-practice/banking_system.log',
                    filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=' %m/%d/%Y %I: %M: %S %p')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


#Initializing date for logging the transactions#
today = date.today()

#JSON file content are written into a dictionary(data) for operations/reference#
data = None
with open('/Users/hakunamatata/Documents/Python_assignments/python-oo-practice/banking_system_data.json') as f:
    data = json.load(f)

#Initializing Typer() function for CLI interface#
bank = typer.Typer()

#Creates customer with input passed in CLI in the mentioned order#
@bank.command()
def create_customer(first_name, last_name, street_address, apt_suite_no, city, state, country, phone, email, sex, dob, credit_score):
    new_entry = Customer(None, first_name, last_name, street_address,
                         apt_suite_no, city, state, country, phone, email, sex, dob, credit_score)
    val_status = new_entry.validate()
    if val_status:
        return
    customer_id = new_entry.create()
    logger.info(
        f"Customer {first_name} {last_name} is created with id {customer_id} successfully")
    print(
        f"Customer {first_name} {last_name} is created with id {customer_id} successfully")


#Deletes Customer details for the given customer_id#
@bank.command()
def delete_customer_data(customer_id):
    status = Customer(customer_id).delete()
    if status:
        logger.info(f"Customer {customer_id} successfully deleted")
        print(f"Customer {customer_id} successfully deleted")
    else:
        logger.info(f"Customer {customer_id} not deleted. Unexpected error!")
        print(f"Customer {customer_id} not deleted. Unexpected error!")


#Displays the required entity details#
@bank.command()
def show_entity(entity_name):
    pprint(f"{data[entity_name]}")


#Displays the given entity , entity id details#
@bank.command()
def show_entities(entity_name, entity_id):
    pprint(f"{data[entity_name][entity_id]}")


#Updates the given entity field , entity value details for the mentioned entity id , entity name#
@bank.command()
def update_info(entity_name, entity_id: str, entity_field: str, entity_value: str):
    data[entity_name][entity_id][entity_field] = entity_value
    Entity(entity_name, entity_id).write_json(data)
    print(
        f"{entity_field} information for {entity_id} has been updated\nUpdated information is {data[entity_name][entity_id]}")
    logger.info(
        f"{entity_field} information for {entity_id} has been updated\nUpdated information is {data[entity_name][entity_id]}")


#Creates account for the mentioned customer id #
@bank.command()
def create_account(customer_id, account_type, parent_account, child_account):
    account_entry = Account(customer_id, None, account_type,
                            parent_account, child_account)
    val_status = account_entry.validate()
    if val_status:
        return
    account_id = account_entry.create()
    print(f"New account created for {customer_id} account no. : {account_id}")
    logger.info(
        f"New account created for {customer_id} account no. : {account_id}")
    print(
        f"Account Created for {customer_id}\nAccount type:{account_type}\nParent account:{parent_account}\nChild account:{child_account}")
    logger.info(
        f"Account Created for {customer_id}\nAccount type:{account_type}\nParent account:{parent_account}\nChild account:{child_account}")


#Deletes account for the provided account id#
@bank.command()
def delete_account_data(account_id):
    status = Account(None, account_id).delete()
    if status:
        print(f"Account {account_id} successfully deleted")
        logger.info(f"Account {account_id} successfully deleted")
    else:
        print(f"Account {account_id} not deleted. Unexpected error!")
        logger.info(f"Account {account_id} not deleted. Unexpected error!")


#Create employee for the provided details#
@bank.command()
def create_employee(first_name, last_name, street_address, apt_suite_no, city, state, country, phone, email, sex, dob, salary, start_date, end_date, work_authorization):
    new_entry = Employee(None, first_name, last_name, street_address,
                         apt_suite_no, city, state, country, phone, email, sex, dob, salary, start_date, end_date, work_authorization)
    val_status = new_entry.validate()
    if val_status:
        return
    employee_id = new_entry.create()
    print(f"Employee {employee_id} created successfully")
    logger.info(f"Employee {employee_id} created successfully")

#Deletes employee details for mentioned employee id#
@bank.command()
def delete_employee_data(employee_id):
    status = Employee(employee_id).delete()
    if status:
        print(f"Employee {employee_id} successfully deleted")
        logger.info(f"Employee {employee_id} successfully deleted")
    else:
        print(f"Employee {employee_id} not deleted. Unexpected error!")
        logger.info(f"Employee {employee_id} not deleted. Unexpected error!")

# Creates mentioned service for the mentioned customer id , account id#
@bank.command()
# loan amount / creditcard limit
def create_service(service_type, customer_id, account_id):
    new_service = Service(None, service_type, customer_id, account_id)
    employee = new_service.assigned_employee()
    print(f"Employee : {employee} is verifying the request")
    logger.info(f"Employee : {employee} is verifying the request")
    val_status = new_service.validate()
    if val_status:
        return
    service_id = new_service.create()
    data["Accounts"][account_id]["service_ids"].append(service_id)
    Entity("Accounts", account_id).write_json(data)
    print(f"Service {service_id} enabled successfully")
    logger.info(f"Service {service_id} enabled successfully")

# Deletes service for the mentioned service id#
@bank.command()
# check if the balance is 0 for the service
def delete_service_data(service_id):
    status = Service(service_id).delete()
    if status:
        print(f"Service {service_id} successfully deleted")
        logger.info(f"Service {service_id} successfully deleted")
    else:
        print(f"Service {service_id} not deleted. Unexpected error!")
        logger.info(f"Service {service_id} not deleted. Unexpected error!")

#Makes transaction between mentioned accounts for amount#
@bank.command()
def add_transaction(customer_id, account_id, transaction_type, transaction_description, from_account, to_account, amount):
    transaction = Transaction(None, customer_id, account_id, transaction_type,
                              transaction_description, from_account, to_account, amount, None)
    tran_status = transaction.make_transaction()
    if tran_status:
        if data["Accounts"][to_account]:
            data["Accounts"][to_account]["balance"] = int(
                data["Accounts"][to_account]["balance"])+int(amount)
        transaction_id = transaction.create()
        data["Accounts"][account_id]["transactions"].append(transaction_id)
        Entity("Accounts", account_id).write_json(data)
        print(
            f"Transaction {transaction_id} from {from_account} to {to_account} successfully done")
        logger.info(
            f"Transaction {transaction_id} from {from_account} to {to_account} successfully done")

##Super class which is referred across all entites#


class Entity:
    def __init__(self, entity_name, entity_id=None):
        self.entity_name = entity_name
        self.entity_id = entity_id
        self.properties = []

    def get_entity_in_dict(self):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError

# Creates id for the entity
    def create(self):
        if not data or self.entity_name not in data:
            data[self.entity_name] = {}
        self.entity_id = str(uuid.uuid4())
        data[self.entity_name][self.entity_id] = self.get_entity_in_dict()
        self.write_json(data)
        return self.entity_id

# Removes the entity for the mentioned entity id
    def delete(self):
        if data and self.entity_id in data[self.entity_name].keys():
            del data[self.entity_name][self.entity_id]
            self.write_json(data)
            return True
        else:
            return False

#Writes the data dictionary to json file#
    def write_json(self, data, filename='/Users/hakunamatata/Documents/Python_assignments/python-oo-practice/banking_system_data.json'):
        with open(filename, 'r+') as file:
            file.truncate(0)
            # convert back to json.
            json.dump(data, file, indent=4)


#Customer entity class#

class Customer(Entity):

    # init method or constructor #
    def __init__(self, customer_id=None, first_name=None, last_name=None, street_address=None, apt_suite_no=None, city=None, state=None, country=None, phone=None, email=None, sex=None, dob=None, credit_score=None):
        super().__init__("Customers", customer_id)
        self.first_name = first_name
        self.last_name = last_name
        self.street_address = street_address
        self.apt_suite_no = apt_suite_no
        self.city = city
        self.state = state
        self.country = country
        self.phone = phone
        self.email = email
        self.sex = sex
        self.dob = dob
        self.credit_score = credit_score

    #Returns dictionary with customer details#
    def get_entity_in_dict(self):
        return {"First Name": self.first_name, "Last Name": self.last_name, "Street Address": self.street_address, "Apt/Suite No": self.apt_suite_no, "City": self.city, "State": self.state, "Country": self.country, "phone": self.phone, "email": self.email, "DOB": self.dob, "Sex": self.sex, "customer id": self.entity_id, "credit score": self.credit_score}

    #Validates if customer is already present#
    def validate(self):
        if not data or "Customers" not in data:
            return False

        for entity_id, entity in data[self.entity_name].items():
            if (entity["First Name"] == self.first_name and
                entity["Last Name"] == self.last_name and
                entity["Sex"] == self.sex and
                entity["DOB"] == self.dob
                ):
                print(f"{self.entity_name} is already present with ID: {entity_id}")
                logger.info(
                    f"{self.entity_name} is already present with ID: {entity_id}")
                return True
        return False

#Account entity class#


class Account(Entity):

    # init method or constructor #
    def __init__(self, customer_id=None, account_id=None, account_type=None, parent_account=None, child_account=None):
        super().__init__("Accounts", account_id)
        self.customer_id = customer_id
        self.account_type = account_type
        self.parent_account = parent_account
        self.child_account = child_account
        self.transactions = []
        self.balance = 0
        self.service_ids = []

    #Returns dictionary with account details#
    def get_entity_in_dict(self):
        return {"customer_id": self.customer_id, "account_id": self.entity_id, "account_type": self.account_type, "transactions": self.transactions, "balance": self.balance, "service_ids": self.service_ids, "parent_account": self.parent_account, "child_account": self.child_account}

    #Validates if account is already present for the customer id#
    def validate(self):
        if not data or "Accounts" not in data:
            return False

        for entity_id, entity in data[self.entity_name].items():
            if(entity["customer_id"] == self.customer_id and
                entity["account_id"] is not None and
                entity["account_type"] == self.account_type
               ):
                print(
                    f"{self.entity_name} is already present with ID: {entity_id} for customer {self.customer_id}")
                logger.info(
                    f"{self.entity_name} is already present with ID: {entity_id} for customer {self.customer_id}")
                return True
        return False

#Employee entity class#


class Employee(Entity):

    # init method or constructor #
    def __init__(self, employee_id=None, first_name=None, last_name=None, street_address=None, apt_suite_no=None, city=None, state=None, country=None, phone=None, email=None, sex=None, dob=None, salary=None, start_date=None, end_date=None, work_authorization=None):
        super().__init__("Employees", employee_id)
        self.first_name = first_name
        self.last_name = last_name
        self.street_address = street_address
        self.apt_suite_no = apt_suite_no
        self.city = city
        self.state = state
        self.country = country
        self.phone = phone
        self.email = email
        self.sex = sex
        self.dob = dob
        self.salary = salary
        self.start_date = start_date
        self.end_date = end_date
        self.work_authorization = work_authorization

    #Returns dictionary with employee details#
    def get_entity_in_dict(self):
        return {"Employee id": self.entity_id, "First Name": self.first_name, "Last Name": self.last_name, "Street Address": self.street_address, "Apt/Suite No": self.apt_suite_no, "City": self.city, "State": self.state, "Country": self.country, "phone": self.phone, "email": self.email, "DOB": self.dob, "Sex": self.sex, "salary": self.salary, "start date": self.start_date, "end data": self.end_date, "Work authorization": self.work_authorization}

    #Validates if employee is already present#
    def validate(self):
        if not data or "Employees" not in data:
            return False

        for entity_id, entity in data[self.entity_name].items():
            if (entity["First Name"] == self.first_name and
                entity["Last Name"] == self.last_name and
                entity["Sex"] == self.sex and
                entity["DOB"] == self.dob
                ):
                print(
                    f"Employee {self.first_name} {self.last_name} is already present with ID: {entity_id}")
                logger.info(
                    f"Employee {self.first_name} {self.last_name} is already present with ID: {entity_id}")
                return True
        return False

    #Creates employee id#
    def create(self):
        if not data or self.entity_name not in data:
            data[self.entity_name] = {}
        self.entity_id = str(uuid.uuid4().hex[:8])
        data[self.entity_name][self.entity_id] = self.get_entity_in_dict()
        self.write_json(data)
        return self.entity_id

#Service entity class#


class Service(Entity):
    # init method or constructor #
    def __init__(self, service_id=None, service_type=None, customer_id=None, account_id=None):
        super().__init__("Services", service_id)
        self.service_type = service_type
        self.balance = 0
        self.customer_id = customer_id
        self.account_id = account_id
        self.employee_id = random.choice(list(data["Employees"].keys()))
    #Returns dictionary with service details#

    def get_entity_in_dict(self):
        return {"customer id": self.customer_id, "service id": self.entity_id, "service type": self.service_type, "balance": self.balance, "account id": self.account_id, "Employee id": self.employee_id}

    #Returns the employee id who is working on the request#
    def assigned_employee(self):
        return self.employee_id

    #Validated the service request#
    def validate(self):
        if "Services" not in data.keys() and "Customers" in data.keys() and "Accounts" in data.keys():
            for entity_id, entity in data["Customers"].items():
                for entity_id_acc, entity_acc in data["Accounts"].items():
                    if entity["customer id"] == self.customer_id and entity["credit score"] >= 650 and (entity_acc["account_id"] == self.account_id and entity_acc["customer_id"] == self.customer_id):
                        print("Request processing")
                        logger.info("Request processing")
                        return False
        else:
            for entity_id, entity in data[self.entity_name].items():
                for entity_id_acc, entity_acc in data["Accounts"].items():
                    if entity["service type"] == self.service_type and entity["account id"] == self.account_id:
                        print(
                            f"{self.entity_name} - {self.service_type} is already present for account ID: {self.account_id}")
                        logger.info(
                            f"{self.entity_name} - {self.service_type} is already present for account ID: {self.account_id}")
                        return True
                    elif entity_acc["account_id"] != self.account_id or entity_acc["customer_id"] != self.customer_id:
                        print(
                            f"Account_id {self.account_id} is not present for customer_id {self.customer_id}")
                        logger.info(
                            f"Account_id {self.account_id} is not present for customer_id {self.customer_id}")
                        return True
                    else:
                        return False
                    

#Transaction class entity#


class Transaction(Entity):
    # init method or constructor #
    def __init__(self, transaction_id=None, customer_id=None, account_id=None, transaction_type=None, transaction_description=None, from_account=None, to_account=None, amount=None, date=None):
        super().__init__("Transactions", transaction_id)
        self.customer_id = customer_id
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.transaction_description = transaction_description
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

    #Returns dictionary with transaction details#
    def get_entity_in_dict(self):
        return {"Transaction id": self.entity_id, "customer id": self.customer_id, "Transaction type": self.transaction_type, "Account id": self.account_id, "Transaction description": self.transaction_description, "From account": self.from_account, "To account": self.to_account, "Amount": self.amount, "Date": today.strftime("%b-%d-%Y")}

    #Makes transaction between the mentioned accounts#
    def make_transaction(self):
        for entity_id, entity in data["Accounts"].items():
            if entity["customer_id"] == self.customer_id and entity["account_id"] == self.from_account and (int(entity["balance"]) == 0 or int(entity["balance"]) < int(self.amount)):
                print("Insufficient Balance ")
                return False
            elif entity["customer_id"] == self.customer_id and entity["account_id"] == self.from_account and int(entity["balance"]) > int(self.amount):
                entity["balance"] = int(entity["balance"]) - int(self.amount)
                return True


if __name__ == '__main__':
    bank()
