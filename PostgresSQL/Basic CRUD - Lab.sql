1.	Select and Display Employee Information by Concatenating Columns
Write a query to select all employees and retrieve information about their id,  first_name, last_name (as Full Name), and job_title (as Job Title).
Example
id	Full Name	Job Title
1	John Smith	Manager
2	John Johnson	Customer Service
3	Smith Johnson	Porter
…	…	…

--Language: SQL

SELECT id, CONCAT(first_name, ' ', last_name) AS "Full Name", job_title AS "Job Title" FROM employees;

--Language: SQL

2.	Select Employees by Filtering and Ordering
Write a query to select all employees (id, first_name, and last_name (as full_name), job_title, salary) whose salaries are higher than 1000.00, ordered by id. Concatenate fields first_name and last_name into 'full_name'.
Example
id	full_name	job_title	salary
3	Smith Johnson	Porter	1100
4	Peter Petrov	Front Desk Clerk	1100
5	Peter Ivanov	Sales	1500.23
…	…	…	…

--Language: SQL

SELECT id, CONCAT(first_name, ' ', last_name) AS "full_name", job_title, salary FROM employees WHERE salary > 1000.00 ORDER BY id;

--Language: SQL

3.	Select Employees by Multiple Filters
Write a query to retrieve information about employees, who are in department 4 and have a salary higher or equal to 1000. Order the information by id.
Example
id	first_name	last_name	job_title	department_id	salary
3	Smith	Johnson	Porter	4	1100
9	Nikolay	Ivanov	Housekeeping	4	1600

--Language: SQL

SELECT id, first_name, last_name, job_title, department_id, salary FROM employees WHERE department_id = 4 AND salary >= 1000 ORDER BY id;

--Language: SQL

4.	Insert Data into Employees Table
Insert new records into table employees by writing a query. Select all employees’ info to check the new entries.
New values: 
Samantha Young, Housekeeping, 4, 900
Roger Palmer, Waiter, 3, 928.33
Submit both INSERT and SELECT queries.
Example
id	first_name	last_name	job_title	department_id	salary
…	…	…	…	…	…
10	Samantha	Young	Housekeeping	4	900
11	Roger	Palmer	Waiter	3	928.33

--Language: SQL

INSERT INTO employees (first_name, last_name, job_title, department_id, salary) 
VALUES ('Samantha', 'Young', 'Housekeeping', 4, 900), 
        ('Roger', 'Palmer', 'Waiter', 3, 928.33);
SELECT * FROM employees;

--Language: SQL

-- 5.	Update Employees Salary
-- Update all employees' salaries whose job_title is "Manager" by adding 100. 
-- Retrieve information from table employees for all managers.
-- Submit both UPDATE and SELECT queries.
-- Example
-- id	first_name	last_name	job_title	department_id	salary
-- 1	John	Smith	Manager	1	1000

--Language: SQL

UPDATE employees 
SET salary = salary + 100 
WHERE job_title = 'Manager';
SELECT * FROM employees 
WHERE job_title = 'Manager';

--Language: SQL

-- 6.	Delete from Table
-- Write a query to delete all employees from the employees table who are in department 2 or 1. Then select all from table employees and order the information by id.
-- Submit both DELETE and SELECT queries.
-- Example
-- id	first_name	last_name	job_title	department_id	salary
-- 3	Smith	Johnson	Porter	4	1100
-- 6	Ivan	Petrov	Waiter	3	990
-- 7	Jack	Jackson	Executive Chef	3	1800
-- 9	Nikolay	Ivanov	Housekeeping	4	1600

--Language: SQL

DELETE FROM employees 
WHERE department_id IN (1, 2);
SELECT * FROM employees
ORDER BY id;

--Language: SQL

7.	Create a View for Top Paid Employee
Write a query to create a view that selects all information about the top-paid employee from the employees table in the hotel database. Call your view to check the results.
Submit both CREATE VIEW and SELECT queries.
Example
id	first_name	last_name	job_title	department_id	salary
8	Pedro	Petrov	Front Desk Supervisor	1	2100

--Language: SQL

CREATE VIEW top_paid_employee AS 
SELECT * FROM employees
ORDER BY salary DESC
LIMIT 1;
SELECT * FROM top_paid_employee;

--Language: SQL