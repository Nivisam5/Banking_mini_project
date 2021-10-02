# Banking_mini_project
Mini project Banking systems

Banking system mini project code is designed as mentioned below.

Super class - Entity : This performs funtions 
  1. ID Creation
  2. Remove the Entity for mentioned Entity ID
  3. Writes the Data Dictionary to JSON file
 
Below are the breakdown entities sub class 
  1. Customer entity
      a. Validates if the new customer entry is already present
  2. Account entity
      a. Validates if the new account entry is already present for the mentioned customer ID
  3. Employee entity
      a. Validates if the employee is already present
      b. Creates new employee ID
  4. Service entity
      a. Validates the service request , if credit scroe is more than 650 & if the service is already present for the mentioned account ID
  5. Transaction entity
      a. Makes transactions between mentioned accounts if the amount mentioned is below the account balance
  

Command Examples :
Banking_system.py --help
  Commands:
  add-transaction
  create-account
  create-customer
  create-employee
  create-service
  delete-account-data
  delete-customer-data
  delete-employee-data
  delete-service-data
  show-entities
  show-entity
  update-info
  
 Customer Creation:
 -------------------
  Banking_system.py create-customer <first_name> <last_name> <street_address> <apt_suite_no> <city> <state> <country> <phone> <email> <sex> <dob> <credit_score>
  Banking_system.py create-customer Angel Master MesaLn 3737 SantaClara CA USA 408 gmail F 01012022 350
  Customer Angel Master is created with id 25a1eb3e-36ea-44c9-9214-8de3edf07397 successfully
  
Account Creation:
------------------
  Banking_system.py create-account <customer_id> <account_type> <parent_account> <child_account>
  Banking_system.py create-account 25a1eb3e-36ea-44c9-9214-8de3edf07397 S N/A N/A
  New account created for 25a1eb3e-36ea-44c9-9214-8de3edf07397 account no. : 318c6649-95ce-42d4-a5fb-6b0cfed5a7b7
  Account Created for 25a1eb3e-36ea-44c9-9214-8de3edf07397
  Account type:S
  Parent account:N/A
  Child account:N/A
  
 Employee Creation:
--------------------
  
  Banking_system.py create-employee <first_name> <last_name> <street_address> <apt_suite_no> <city> <state> <country> <phone> <email> <sex> <dob> <salary>      <start_date> <end_date> <work_authorization>
  Banking_system.py create-employee "Ross" "Geller" "Jameston rd" "215" "Hayward" "CA" "USA" "555" "ymail" "M" "02031997" "100000" "02022018" "01019999" "US-C"
  Employee 4ab5459f created successfully
  
Service Creation:
-------------------
  Banking_system.py create-service <service_type> <customer_id> <account_id>
  Banking_system.py create-service Creditcard 25a1eb3e-36ea-44c9-9214-8de3edf07397 25a1eb3e-36ea-44c9-9214-8de3edf07397
  Employee : 6bf0e07b is verifying the request
  Account_id 25a1eb3e-36ea-44c9-9214-8de3edf07397 is not present for customer_id 25a1eb3e-36ea-44c9-9214-8de3edf07397

Add Transaction:
------------------
  
  Banking_system.py add-transaction <customer_id> <account_id> <transaction_type> <transaction_description> <from_account> <to_account> <amount>
  Banking_system.py add-transaction "e61784ec-21c9-4a7d-a205-65b2a833f526" "9e9be8ca-b56e-4f33-8436-bc92f8701ea5" "withdrawal" "resend" "9e9be8ca-b56e-4f33-8436-   bc92f8701ea5" "cbe97a07-f8f3-4b8e-a4b4-9bf27a2eb1d8" "500"
  
  Banking_system.py delete-account-data <account_id>
  Banking_system.py delete-customer-data <customer_id>
  Banking_system.py delete-employee-data <employee_id>
  Banking_system.py delete-service-data <service_id>
  
Display Entity id details:
------------------------
  
  Banking_system.py show-entities <entity_name> <entity_id>
  Banking_system.py show-entities Employees 4ab5459f
("{'Employee id': '4ab5459f', 'First Name': 'Ross', 'Last Name': 'Geller', "
 "'Street Address': 'Jameston rd', 'Apt/Suite No': '215', 'City': 'Hayward', "
 "'State': 'CA', 'Country': 'USA', 'phone': '555', 'email': 'ymail', 'DOB': "
 "'02031997', 'Sex': 'M', 'salary': '100000', 'start date': '02022018', 'end "
 "data': '01019999', 'Work authorization': 'US-C'}")

  Display Entity details:
------------------------
  Banking_system.py show-entity <entity_name>
  Banking_system.py show-entity Accounts
("{'cbe97a07-f8f3-4b8e-a4b4-9bf27a2eb1d8': {'customer_id': "
 "'1cbc60f-c6ae-4a4a-a77f-a48060dea272', 'account_id': "
 "'cbe97a07-f8f3-4b8e-a4b4-9bf27a2eb1d8', 'account_type': 'S', 'transactions': "
 "['2217743e-a6bd-47e7-94e8-1cb8d8b0e37e', "
 "'0002f1dd-6f0b-486d-9ae0-35326f13a35a', "
 "'f058e1d0-50d2-4f5a-b7b3-e805fc08c6f3'], 'balance': 500, 'service_ids': [], "
 "'parent_account': 'NA', 'child_account': 'NA'}, "
 "'9e9be8ca-b56e-4f33-8436-bc92f8701ea5': {'customer_id': "
 "'e61784ec-21c9-4a7d-a205-65b2a833f526', 'account_id': "
 "'9e9be8ca-b56e-4f33-8436-bc92f8701ea5', 'account_type': 'S', 'transactions': "
 "['bb097e16-dc0b-4414-ba7e-5cef8dcd9b9a', "
 "'b50a4924-c50f-44a7-a7f7-c355cebf1907', "
 "'a84e4dfc-35a0-44db-9910-73d22e2c81fd'], 'balance': 200, 'service_ids': "
 "['0f21fdc5-994d-46d0-90c4-64aa15733dbb'], 'parent_account': 'NA', "
 "'child_account': 'NA'}, '318c6649-95ce-42d4-a5fb-6b0cfed5a7b7': "
 "{'customer_id': '25a1eb3e-36ea-44c9-9214-8de3edf07397', 'account_id': "
 "'318c6649-95ce-42d4-a5fb-6b0cfed5a7b7', 'account_type': 'S', 'transactions': "
 "[], 'balance': 0, 'service_ids': [], 'parent_account': 'N/A', "
 "'child_account': 'N/A'}}")

  Banking_system.py update-info <entity_name> <entity_id: str> <entity_field: str> <entity_value: str>
  
