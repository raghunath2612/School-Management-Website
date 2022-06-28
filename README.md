# School-Management-Website
 
1.Download and extract this project into a folder.
2.Export students.bak file into MS SQL Server.
3.Change your MS SQL connection settings in the project. ie change
conn = pyodbc.connect('Driver={sql server};'
                          'Server=LAPTOP-8J652NOT\MSSQLSERVER01;'
                          'Database=Students;'
                          'Trusted_Conntection=yes;')
to your connection configuration
          
4.run "python manage.py runserver"
