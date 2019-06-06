# Guidlines for using the code

##  1. Code Design

The folder has the following files, along with their functionality:
* README.md: Containing the guidlines of running the project
* news.py : the main code which ocntains the core functionality & the main function
* newsdb.py: a controller file, which contains the methods used for connecting to the database
* .idea (folder): Please ignore this folder, as it is automatically created, since I was working on the project on the phpStorm IDE.


##  2. Code Prep for running

First of all, you will need to ocnnect to the news.sql databse, and run the following commands, to create the necessary views:

*View #1*

``` SQL
create view error_count as select date(time), count(status) from log where status NOT like '200 OK' group by date(time);
```
*View #2*

``` SQL
 create view overall_count as select date(time), count(status) from log group by date(time);
```


## 3. Running the code

To run the code, please run this command in the terminal : "python news.py", with making sure all these prerequisites are met:
* You are inside the folder's directory, where all other files are there
* You can connect to the news database
* You have run the above 2 commands within the databse itself, to create two views named _overal count_ and _error count_