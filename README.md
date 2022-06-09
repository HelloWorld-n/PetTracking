# Installation

Step 1:  
```bash
sudo apt-get install apache2 -y
sudo apt-get install mysql -y
sudo apt-get install python3 -y
sudo apt-get install python3-pymysql -y
```

&nbsp;

Step 2:  
Configure **mysql** and **apache2**.

&nbsp;
&nbsp;
&nbsp;

# SetUp

Step 1:  
```bash
sudo /etc/init.d/apache2 start
sudo /etc/init.d/mysql start
```

&nbsp;

Step 2:  

`Connect.py` has following code:  
```py
HOST = "[::1]"
PORT = "3306"
SQL_USERNAME = "root"
SQL_PASSWORD = "myPassword"
```  
that can be changed to match configurations from Installation step 2.

&nbsp;


Step 3:  
Create database by opening `prepareDatabase.py`.

&nbsp;

Step 4:  
Create administrator account at `createAccount.py`.

&nbsp;
&nbsp;
&nbsp;

# PetTracking
