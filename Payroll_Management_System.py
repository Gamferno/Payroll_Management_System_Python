import mysql.connector
import datetime
from tabulate import tabulate

db=input("Enter name of your database:  ")

mydb=mysql.connector.connect(host='localhost',user='root',passwd='amoiamoi',auth_plugin='mysql_native_password')
mycursor=mydb.cursor()


sql=f"CREATE DATABASE if not exists {db}"

mycursor.execute(sql)

print("Database created succesfully..")

mycursor.execute(f"Use {db}")
tablename=input("Name of the table to be created: ")
query=f"create table if not exists {tablename}(empno int primary key,name varchar(15) not null,job varchar(15),BasicSalary int,DA float,HRA float,GrossSalary float,Tax float,NetSalary float);"

mycursor.execute(query)
print(f"Table {tablename} created successfully.....")
print()
while True:
    print("*"*95)
    print()
    print("MAIN MENU".center(90))
    print()
    print("*"*95)
    print()
    print("\t\t\t\t1. Adding Employee Records")
    print("\t\t\t\t2. For Displaying Record of a Particular Employee")
    print("\t\t\t\t3. For Displaying Record of All the Employees")
    print("\t\t\t\t4. For Deleting Records of All the Employees")
    print("\t\t\t\t5. For Deleting a Record of a Particular Employee")
    print("\t\t\t\t6. For Modification in a Record")
    print("\t\t\t\t7. For Displaying Payroll for a Particular Employee")
    print("\t\t\t\t8. For Displaying Payroll for All the Employees")
    print("\t\t\t\t9. Exit the Program")

    choice=int(input('Enter choice: '))

    if choice == 1:
        try:
            print('Enter employee information...')
            mempno=int(input("Enter employee no.: "))
            mname=input('Enter employee name: ')
            mjob=input('Enter employee job: ')
            mbasic=float(input("Enter basic salary: "))

            if mjob.upper()=='OFFICER':
                mda=mbasic*0.5
                mhra=mbasic*0.35
                mtax=mbasic*0.2

            elif mjob.upper()=='MANAGER':
                mda=mbasic*0.45
                mhra=mbasic*0.30
                mtax=mbasic*0.15
            else:
                mda=mbasic*0.4
                mhra=mbasic*0.25
                mtax=mbasic*0.1
            mgross=mbasic+mda+mhra
            mnet=mgross-mtax
            query=f"insert into {tablename} values ({mempno},'{mname.capitalize()}','{mjob.capitalize()}',{mbasic},{mda},{mhra},{mgross},{mtax},{mnet});"
            mycursor.execute(query)
        
            mydb.commit()
            input("Press Enter to Continue.........")
        except Exception as e:
            print('Something Went Wrong',e)
    
    elif choice == 2:
        try:
            en=input('Enter employee no. of the record to be displayed: ')
            query=f"select empno,name,job,basicsalary from {tablename} where empno={en};"
            mycursor.execute(query)
     #       myrecord=mycursor.fetchone()
            print(f"\n\n Record of Employee No. {en}")
            #print(myrecord)
            print(tabulate(mycursor,headers=['Empno','Name','Job','Basic Salary'],tablefmt='fancy_grid'))
            c=mycursor.rowcount
            input("Press Enter to Continue......")

            if c==-1:
                print("Nothing to display")

        except Exception as e:
            print("Something Went Wrong",e)

    elif choice == 3:
        mycursor.execute(f"select empno,name,job,basicsalary from {tablename}")
        print(tabulate(mycursor,headers=['Empno','Name','Job''Basic Salary'],tablefmt='fancy_grid'))
        input("Press Enter to Continue......")

    elif choice == 4:
        print("Warning! All your Records are about to be deleted")
        a=input("Continue with the deletion (Y/N)")
        if a.upper == 'YES' or a.upper == 'Y':

            mycursor.excecute(f"delete from {tablename}")
            print("All Records are Deleted")

    elif choice == 5:
        try:
            en=input("Enter Employee No. of the Record to be Deleted: ")
            mycursor.execute(f"delete from {tablename} where empno={en}")
            mydb.commit()
            c=mycursor.rowcount
            print(c)
            if c >0:
                print("Deletion Done")
            else:
                print(f"Employee no {en} not found!")
        except Exception as e:
            print("Error Occured",e)

    elif choice == 6:
        try:
            en=input('Enter employee no. of the record to be modified....')
            query=f'select * from {tablename} where empno={en}'
            mycursor.execute(query)
            c=mycursor.rowcount
            if c == -1:
                print(f"Empno {en} does not exist")

            else:
                myrecord=mycursor.fetchone()
                mname=myrecord[1]
                mjob=myrecord[2]
                mbasic=myrecord[3]
                print(mname,mjob,mbasic)
                print(f'empno  : {myrecord[0]}')
                print(f'name  : {myrecord[1]}')
                print(f'job  : {myrecord[2]}')
                print(f'basic  : {myrecord[3]}')
                print(f'da  : {myrecord[4]}')
                print(f'hra  : {myrecord[5]}')
                print(f'gross  : {myrecord[6]}')
                print(f'tax  : {myrecord[7]}')
                print(f'net  : {myrecord[8]}')
                print('--------------------------')
                print("Type values to modify below or just Enter for no change")
                x=input('Enter name: ')
                if len(x)>0:
                    mname=x

                x=input('Enter job: ')
                if len(x)>0:
                    mjob=x
                x=input('Enter basic salary: ')
                if len(x)>0:
                    mbasic=float(x)
                query=f"update {tablename} set name = '{mname}', job='{mjob}',basicsalary={mbasic} where empno={en};"
            

                mycursor.execute(query)
        except Exception as e:
            print(e)





        
    elif choice == 7:
        try:
            en=int(input("Enter Employee No. of the Record:  "))
            mycursor.execute(f'select * from {tablename} where empno={en}')
            myrecords=mycursor.fetchall()
            print()
            print('*'*95)
            print()
            #print()
            print('" Employee Payroll "'.center(90))
            print()
            print('*'*95)
            now=datetime.datetime.now()
            hello=now.strftime("%Y-%m-%d %H:%M: %S")
            print()
            print(f"Current Date and Time: {hello}")
            print()

            print(tabulate(myrecords,headers=['Empno','Name','Basic Salary','DA','HRA','Gross Salary','Tax','Net Salary'],tablefmt='fancy_grid'))

            input("Press Enter to Continue....")
        except Exception as e:
            print(e)

    elif choice == 8:
        try:
            mycursor.execute(f'select * from {tablename}')
            myrecords=mycursor.fetchall()
            
            print('*'*95)
            print()
            print('Employee Payroll'.center(90))
            print()
            print('*'*95)
            print()
            now=datetime.datetime.now()
            hello=now.strftime("%Y-%m-%d %H:%M: %S")
            print(f"Current Date and Time: {hello}")
            print()
            
            print(tabulate(myrecords,headers=['Empno','Name','Basic Salary','DA','HRA','Gross Salary','Tax','Net Salary'],tablefmt='fancy_grid'))

            

            input("Press Enter to Continue....")
        except Exception as e:
            print(e)

    elif choice==9:
        print("Have a Good Day :)")
        break

        


