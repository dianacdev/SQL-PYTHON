'''Python Program to Populate 10 customers'''
import os
import mysql.connector
# pip install python-dotenv or update the password field to your root password.
from dotenv import load_dotenv

load_dotenv()

# Logging into mySQl Workbench as specified user
db = mysql.connector.connect(
    host="localhost",
    user="tom",
    passwd=os.getenv('MYSQLWORKBENCH'),
    database="lab13_db"
)

cursor = db.cursor()  # Initating cursor

'''mySQL QUERIES'''
# Adding a customer to the customer db
ADD_CUSTOMER = "INSERT INTO customer (firstname, lastname, phone_number) VALUES(%s, %s, %s)"

# Deleting a customer from the customer db using the employee_id
DELETE_CUSTOMER = "DELETE FROM customer WHERE employee_id = %s"

# Getting the customer table
CUSTOMER_QUERY = "SELECT * FROM customer"

# Update a customers phone_number
UPDATE_PHONE = "UPDATE customer SET phone_number = %s WHERE employee_id = %s ;"

CREATE_AUDIT = "INSERT INTO customer_audit(employee_id) VALUES((SELECT employee_id FROM customer WHERE employee_id=%s));"

AUDIT_QUERY = "SELECT customer_audit.employee_id, customer.firstname, customer.lastname, customer_audit.change_on FROM customer_audit INNER JOIN customer ON customer_audit.employee_id = customer.employee_id"

# Ten customers data, could put in an array or list but for speed will add this way on initalization
# customer_1 = ("Zephyr ", "Thunderstrike", "882-472-0842")
# customer_2 = ("Isabella", "Aldina", "768-805-3863")
# customer_3 = ("Madison", "Evergreen", "338-343-8852")
# customer_4 = ("Sebastian", "Frost", "626-419-6695")
# customer_5 = ("Olivia ", "Sterling", "375-792-6684")
# customer_6 = ("Xavier ", "Moonstone", "506-698-6220")
# customer_7 = ("Isabella ", "Silverwood", "897-709-3695")
# customer_8 = ("Elijah", "Storm", "595-637-9994")
# customer_9 = ("Scarlett ", "Ravenwood", "953-219-3113")
# customer_10 = ("Jackson", "Ember", "728-368-6600")

# # Executing the insert of the 10 employees
# cursor.execute(ADD_CUSTOMER, customer_1)
# cursor.execute(ADD_CUSTOMER, customer_2)
# cursor.execute(ADD_CUSTOMER, customer_3)
# cursor.execute(ADD_CUSTOMER, customer_4)
# cursor.execute(ADD_CUSTOMER, customer_5)
# cursor.execute(ADD_CUSTOMER, customer_6)
# cursor.execute(ADD_CUSTOMER, customer_7)
# cursor.execute(ADD_CUSTOMER, customer_8)
# cursor.execute(ADD_CUSTOMER, customer_9)
# cursor.execute(ADD_CUSTOMER, customer_10)
# db.commit()


def insert_customer():
    '''Used to add a customer to the customer table'''
    firstname = input("Enter a customer's first name: ")
    lastname = input("Enter a customer's last name: ")
    phone = input("Enter a customer's phone number (15 character max): ")
    check = input(
        "Does the info look correct, before commiting to db? (Y/N): ")[0]
    values = (firstname, lastname, phone)
    if check == 'Y' or check == 'y':
        cursor.execute(ADD_CUSTOMER, values)
        db.commit()
    else:
        print("\nLets try this again!")
        insert_customer()


def del_customer():
    '''Used to delete a customer by there employee_id'''
    employeeid = int(input('Enter an Employee ID to DELETE: '))
    check = input("Are you sure you want to delete? (Y/N): ")
    if check == 'Y'or check =='y':
        values = (employeeid, )
        cursor.execute(DELETE_CUSTOMER, values)
        db.commit()
    else:
        print("DELETE CANCELLED!\n")


def customer_db():
    '''Selecting all the customers in the customer table'''
    print()
    print("Customer Table Results".center(80, "_"))
    print()
    print("{:<12}  {:<20}  {:<20} {:<20}".format(
        "Employee_ID", "First Name", "Last Name", "Phone Number"))
    cursor.execute(CUSTOMER_QUERY)
    for (employee_id, firstname, lastname, phone_number) in cursor:
        print("{:<12}  {:<20}  {:<20} {:<20}".format(
            employee_id, firstname, lastname, phone_number))
    print()


def audit_customer():
    '''Updating the users phone number and Adding the audit'''
    employee_id = int(input('Enter the id: '))
    phone_number = input('Enter the customers new phone number: ')
    values = (phone_number, employee_id)
    audit = (employee_id,)
    cursor.execute(UPDATE_PHONE, values)
    db.commit()
    cursor.execute(CREATE_AUDIT, audit)
    db.commit()


def audit_db():
    '''Shows the employees that have updated there phone number'''
    print()
    print("Customer Audit Table Results".center(80,"_"))
    print()
    print("{:<12}  {:<20}  {:<20}  {:<20}".format(
        "Employee_ID", "First Name", "Last Name", "Change_On",))
    cursor.execute(AUDIT_QUERY)
    for (employee_id, firstname, lastname, change_on) in cursor:
        print("{:<12}  {:<20}  {:<20}  {:%d %b %Y}".format(
            employee_id, firstname, lastname, change_on))
    print()


def print_menu():
    '''The Menu/Options the user can do'''
    print(" Menu ".center(40, '#'))
    print("Add a Customer: 0".center(40, ' '))
    print("Delete a Customer: 1".center(40, ' '))
    print("Query Customer table: 2".center(40, ' '))
    print("Update a Customer: 3".center(40, ' '))
    print("Query Audit Table: 4".center(40, ' '))
    print("Exit Program: 9".center(40, ' '))
    print("\n")


def menu(selection):
    '''The menu for the program'''
    match selection:
        case 0:
            # Add a customer
            insert_customer()
            selection = int(input('What would you like to do?: '))
            menu(selection)
        case 1:
            # Delete a customer using employee_id
            del_customer()
            selection = int(input('What would you like to do?: '))
            menu(selection)
        case 2:
            # Query the customer table
            customer_db()
            selection = int(input('What would you like to do?: '))
            menu(selection)
        case 3:
            # Update a customer, I'm assuming they give a valid employee_id
            audit_customer()
            audit_db()
            db.commit()
            selection = int(input('What would you like to do?: '))
            menu(selection)
        case 4:
            # Showing the audit_db table
            audit_db()
            selection = int(input('What would you like to do?: '))
            menu(selection)
        case 9:
            # Closing the cursor, the db connection, and quitting the program
            cursor.close()
            db.close()
            return 0
        case default:
            print(f"{selection} is not a valid option, please try again!\n")
            selection = int(input('What would you like to do?: '))
            menu(selection)


def main():
    '''Main Program'''
    print_menu()
    selection = int(input('What would you like to do?: '))
    menu(selection)


if __name__ == '__main__':
    main()
