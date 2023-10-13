#-------------------------------------------------------------------------------
# Name:        Employee Database
#
# Created:     13 10 2023
#
# Lead Dev:    Meit Sant
# Copyright:   (c) MS Productions
#
# Time Spent:  34 mins
#-------------------------------------------------------------------------------

# For Anushka

from sys import exit
from sqlite3 import connect

option = input(
"""
Welcome to Employee management system !
Made by Anushka Mishra XII F

Please Choose your option :
    (1) Upload data of a new employee
    (2) Check data of an employee
    (3) Remove data of an employee

--> """
)

# Attempting connection to database and creating table if not exists
print('\n[INFO] Initializing database')
try:
    connector = connect('EmployeeDB.db')
    connector.execute("""CREATE TABLE IF NOT EXISTS Empl(
Emp_ID  varchar(5) PRIMARY KEY,
Emp_Name varchar(30) NOT NULL,
Emp_Phone int(10) NOT NULL,
Emp_Age int(2) NOT NULL,
Emp_Dept varchar(30) NOT NULL,
Emp_Salary float(10) NOT NULL
);""")
    connector.commit()
except:
    print('\n[ERROR] Connection to the database failed.')
    connector.close()
    exit()

# If option is 1, then the program will ask to enter employee data
if option == '1':
    # Getting data for database insertion
    while True: # A loop is added in case a user mistypes details
        name = input("\nPlease enter Employee Name\n--> ")
        phone = int(input("Please enter Employee's Phone number\n--> "))
        age = int(input("Please enter Employee's age\n--> "))
        dept = input("Please enter Employee's new department\n--> ")
        salary = float(input("Please enter Employee's salary\n--> "))
        option = input('\nAre you okay with the above details ? (Yes/No)\n--> ')

        if option in ('Yes','yes','Y','y'):
            break # Exits loop
        if option not in ('No','no','N','n'):
            print('\n[ERROR] Invalid response recevied please try again')
            connector.close()
            exit()
        # Program will bydefault restart loop if 'Yes' is not entered.
        # So a separate 'else' statement is not needed.

    print('\n[INFO] Writing to database')

    # Generating a new ID for the new employee
    query = connector.execute('SELECT Emp_ID from Empl;')
    data = query.fetchall()
    ID_List = []
    for i in data:
        ID_List.append(int(i[0][3:]))
    emp_No = max(ID_List)
    if emp_No < 10:
        emp_ID = f'EMP0{emp_No+1}'
    else:
        emp_ID = f'EMP{emp_No+1}'

    # Database insertion
    try:
        connector.execute(f"INSERT INTO Empl VALUES('{emp_ID}','{name}',{phone},{age},'{dept}',{salary})")
        connector.commit()
        print('\n[INFO] Employee details saved succesfully.')
    except:
        print('\n[ERROR] Write to database failed. Please try again.')

    connector.close()
    exit()

# If option is 2, then the program will ask for the employee's ID
if option == '2':
    # Retrieve ID of the employee from the user
    ID = input('\nPlease enter employee ID\n--> ')
    query = connector.execute(f"SELECT * FROM Empl WHERE Emp_ID = '{ID}';")
    empl_Data = query.fetchall()
    print(empl_Data)
    if empl_Data == []:
        print(f"\n[ERROR] No employee with ID '{ID}' found. Please try again.")
        connector.close()
        exit()
    # Prints out details of the employee
    print(f"""
    Employee Details :-
    Name        - {empl_Data[0][1]}
    Phone No.   - {empl_Data[0][2]}
    Age         - {empl_Data[0][3]}
    Department  - {empl_Data[0][4]}
    Salary      - {empl_Data[0][5]}
    """)
    connector.close()
    exit()

# If option is 3, then the program will ask for employee's ID, for deletion
if option == '3':
    # Retrieve ID of the employee from the user
    ID = input('\nPlease enter employee ID\n--> ')
    query = connector.execute(f"SELECT * FROM Empl WHERE Emp_ID = '{ID}';")
    empl_Data = query.fetchall()
    if empl_Data == []:
        print(f"\n[ERROR] No employee with ID '{ID}' found. Please try again.")
        connector.close()
        exit()
    # Delete the data
    connector.execute(f"DELETE FROM Empl WHERE Emp_ID = '{ID}';")
    connector.commit()
    print('\n[INFO] Employee data was deleted successfully.')

    connector.close()
    exit()

# If the option entered is not 1,2 or 3, the program will exit
else:
    print('\n[ERROR] Invalid response recevied please try again')
    connector.close()
    exit()
