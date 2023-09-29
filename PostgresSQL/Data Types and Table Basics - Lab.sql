-- Language: sql

1.  Create Tables	
Table "employees":
•	id – serial, primary key, Not NULL;
•	first_name – character varying, max length 30;
•	last_name – character varying, max length 50; 
•	hiring_date– date, default "2023-01-01"; 
•	salary – numeric, specified to the second decimal place, and has 10 digits in total;
•	devices_number – integer; 
Create the "departments" and "issues" tables analogically:
Table "departments":
•	id – serial, primary key, Not NULL;
•	name – character varying, max length 50; 
•	code– character, fixed length 3;
•	description – text; 
Table "issues":
•	id – serial, primary key, unique;
•	description – character varying, max length 150;
•	date – date;
•	start – timestamp without time zone;

-- Language: sql

CREATE TABLE employees (
    id serial PRIMARY KEY NOT NULL,
    first_name character varying(30),
    last_name character varying(50),
    hiring_date date DEFAULT '2023-01-01',
    salary numeric(10,2),
    devices_number integer
);

CREATE TABLE departments (
    id serial PRIMARY KEY NOT NULL,
    name character varying(50),
    code character(3),
    description text
);

CREATE TABLE issues (
    id serial PRIMARY KEY,
    description character varying(150),
    date date,
    start timestamp without time zone
);

-- Language: sql


2.  Insert Data in Tables

Insert data in the "employees" table:
•	Insert 5 employees with the following data:
o	First name: "John", Last name: "Doe", Salary: 1000.00, Devices number: 3;
o	First name: "Jane", Last name: "Doe", Salary: 2000.00, Devices number: 2;
o	First name: "John", Last name: "Smith", Salary: 3000.00, Devices number: 1;
o	First name: "Jane", Last name: "Smith", Salary: 4000.00, Devices number: 0;
o	First name: "John", Last name: "Johnson", Salary: 5000.00, Devices number: 0;
•	Insert 3 employees with the following data:
o	First name: "John", Last name: "Doe", Salary: 1000.00, Devices number: 3;
o	First name: "Jane", Last name: "Doe", Salary: 2000.00, Devices number: 2;
o	First name: "John", Last name: "Smith", Salary: 3000.00, Devices number: 1;
•	Insert 2 employees with the following data:
o	First name: "Jane", Last name: "Smith", Salary: 4000.00, Devices number: 0;
o	First name: "John", Last name: "Johnson", Salary: 5000.00, Devices number: 0;

-- Language: sql

INSERT INTO employees (first_name, last_name, salary, devices_number)
VALUES ('John', 'Doe', 1000.00, 3),
       ('Jane', 'Doe', 2000.00, 2),
       ('John', 'Smith', 3000.00, 1),
       ('Jane', 'Smith', 4000.00, 0),
       ('John', 'Johnson', 5000.00, 0);

INSERT INTO employees (first_name, last_name, salary, devices_number)

VALUES ('John', 'Doe', 1000.00, 3),
       ('Jane', 'Doe', 2000.00, 2),
       ('John', 'Smith', 3000.00, 1);

INSERT INTO employees (first_name, last_name, salary, devices_number)

VALUES ('Jane', 'Smith', 4000.00, 0),
       ('John', 'Johnson', 5000.00, 0);

-- Language: sql

3.  Alter Tables
Altering the tables is done via the "ALTER TABLE" clause. Add a new column – "middle_name", "VARCHAR(50)" to the "employees" table. 

-- Language: sql

ALTER TABLE employees
ADD COLUMN middle_name character varying(50);

-- Language: sql

4.  Add Constraints
In the table "employees", set the salary column as Not NULL with a default value of 0. Set the hiring date column as Not NULL too.

-- Language: sql

ALTER TABLE employees
ALTER COLUMN salary SET NOT NULL,
ALTER COLUMN salary SET DEFAULT 0,
ALTER COLUMN hiring_date SET NOT NULL;

-- Language: sql

5.  Modify Columns
Change the property "VARCHAR(50)" to "VARCHAR(100)" for the middle_name column in "employees" table.

-- Language: sql

ALTER TABLE employees
ALTER COLUMN middle_name TYPE character varying(100);

-- Language: sql

6.  Truncate Tables
Truncate table "issues".

-- Language: sql

TRUNCATE TABLE issues;

-- Language: sql

7.  Drop Tables
Drop table "departments".

-- Language: sql

DROP TABLE departments;

-- Language: sql