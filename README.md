Lambda Complex V1 is a project tracking system which focuses on tracking changes made to coding projects.
Please refer the Word document of the system to get proper insights of Lambda Complex as a system
For installation please make sure that you have installed SQL Server on your machine and python too.
For Python packages you need to install only three packages for Server, DB Connectivity and Session management which are 
Flask(3.0.2)
pyodbc(5.1.0)
Flask-Session(0.7.0)

Step 1 Install all of them using this command:
`pip install Flask==3.0.2 pyodbc==5.1.0 Flask-Session==0.7.0`

Step 2 In SQL Server you need to create a System User named 'Server_Admin' and its access password should be 'root'.

Step 3 In SQL Server run the BACKUP.sql file which is present in 'LambdaComplex\LambdaComplexDatabase\BACKUP.sql' path in the main directory of the project, this will create Important database schemas for the system.

Step 4 In Python code, you need to make changes to Credentials.py present at 'LambdaComplex\LambdaComplex\LambdaComplex_Entities\Credentials.py' change the SERVER Variable in Credentials class to your SQL Server name.

Step 5(OPTIONAL) In Credentials.py you can notice there are System user name and password set there if you want to change your User name and password to an existing user then you can just change it here, One more optional change is suggested if your Flask App URL is different then it can be changed at Common.js at 'LambdaComplex\LambdaComplex\static\js\Logic\Common.js' just change the top three URL Variables to your need

Step 6 Till now if everything is working then open Main LambdaComplex folder in VS Code(Note you have to open the LambdaComplex folder inside of the main project folder not the main folder)

Step 7 Hitting run will start the web application and you can debug it how ever you like and login as 'Root_admin' with password 'LC_Admin@2024' then you will be logged in as Admin user
