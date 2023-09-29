--Language: sql

0.	Create a Database
-- You have already learned how to create a database using the pgAdmin interface. Now it's time to use a SQL query to create a new database named "minions_db".

-- Language: sql

CREATE DATABASE minions_db;

-- Language: sql

1.	Create a Table
In the newly created database, add a new table. Write SQL statement to create table "minions" including columns:
	"id" - should be a primary key, and automatically incremented; 
	"name" - with a max length of 30 characters;
	 "age" - should be a whole number;

-- Language: sql

CREATE TABLE minions (
    id serial PRIMARY KEY,
    name character varying(30),
    age integer
);

-- Language: sql

2.	Rename the Table
To avoid confusion, rename the newly created table to "minions_info". 

-- Language: sql

ALTER TABLE minions RENAME TO minions_info;

-- Language: sql

3.	Alter the Table
As Gru builds a new weapon, he must delegate responsibilities to the Minions and give them tasks. For this reason, you need to update the table by adding new columns:
	"code" - represents the place where the Minion works and is exactly 4 characters long;
	"task" - text with no length limit;
	"salary" - specify to the third decimal place and has 8 digits;

-- Language: sql

ALTER TABLE minions_info
ADD COLUMN code character(4),
ADD COLUMN task text,
ADD COLUMN salary numeric(8,3);

-- Language: sql

4.	Rename Column
Gru does not like the name of the column "salary", so he wants to change the name of this column to "banana".

-- Language: sql

ALTER TABLE minions_info
RENAME COLUMN salary TO banana;

-- Language: sql

5.	Add New Columns
You need to update the table again because Gru forgot to mention that he needs to store emails to send Minions their schedules for the week. He also asks for information on whether Minions have the necessary equipment. Add two new columns with the following data:
	"email" - with a max length of 20 characters;
	"equipped" - state of true or false;
*** Note, PostgreSQL offers three states of BOOLEAN data type: TRUE, FALSE, or NULL. Therefore, add a constraint to the BOOLEAN type.

-- Language: sql

ALTER TABLE minions_info
ADD COLUMN email VARCHAR(20),
ADD COLUMN equipped boolean NOT NULL default false;

-- Language: sql

6.	Create ENUM Type
An enum type is a data type whose value is chosen from an enumerated list of possibilities. This will help Gru to understand how the Minions feel. Create type "type_mood" that contains the following set of values:
	('happy', 'relaxed', 'stressed', 'sad')
In the table add another column "mood" of type "type_mood".

-- Language: sql

CREATE TYPE type_mood AS ENUM ('happy', 'relaxed', 'stressed', 'sad');
ALTER TABLE minions_info
ADD COLUMN mood type_mood;

-- Language: sql

7.	Set Default
To maintain data accuracy and reliability in the table, it is necessary to establish specific rules. By default, columns allow NULL values. To enforce the columns to disallow NULL values, the following rules should be implemented:
	"age" - should have a DEFAULT 0;
	"name" and "code" - should have an empty string as the default value;
*** Note, in this case, you need to use ALTER COLUMN to update/edit specific columns.

-- Language: sql

ALTER TABLE minions_info
ALTER COLUMN age SET DEFAULT 0,
ALTER COLUMN name SET DEFAULT '',
ALTER COLUMN code SET DEFAULT '';

-- Language: sql

8.	Add Constraints
Constraints can be specified when the table is created or afterward. Please use the syntax below to add constraints to the given columns:
ALTER TABLE <table_name>
ADD CONSTRAINT <constraint_name> <constraint_definition> (<column1>, <column2>, ... <column_n>);
Add them to the following columns:
	"id" and "email"- should be UNIQUE across all the table rows. The constraint name for this column is "unique_containt";
	"banana" - should always be a positive number and greater than 0. The constraint name for this column is " banana_check";

-- Language: sql

ALTER TABLE minions_info
ADD CONSTRAINT unique_containt UNIQUE (id, email),
ADD CONSTRAINT banana_check CHECK (banana > 0);

-- Language: sql

9.	Change Column’s Data Type
Gru has noticed that Dr. Nefario is taking too much time to write about the daily tasks of the Minions. He wants to change the data type of the "task" column and limit its length to 150 characters. 

-- Language: sql

ALTER TABLE minions_info
ALTER COLUMN task TYPE VARCHAR(150);

-- Language: sql

10.	Drop Constraint
Gru has realized that he needs to give the Minions two days off per week and wants to update the database accordingly. To do this, you need to remove the constraint that prevents the "equipped" column from having a NULL value.

-- Language: sql

ALTER TABLE minions_info
-- ADD COLUMN equipped boolean NOT NULL default false;
ALTER COLUMN equipped DROP NOT NULL;

-- Language: sql

11.	Remove Column
Dr. Nefario decided to create another table and move some data there. Help him by writing a SQL query to DROP the column "age".

--Language: sql

ALTER TABLE minions_info
DROP COLUMN age;

-- Language: sql

12.	Table Birthdays
-- Assist Dr. Nefario in creating a new table to store information about the Minions' birthdays and organize surprise parties. Make sure to add constraints to the data types, the "id" must be UNIQUE, and be cautious of non-NULL and DEFAULT values. The table should be named "minions_birthdays" and include the following columns:
	"id";
	"name" - with a max length of 50 characters;
	"date_of_birth" - should be of type Date;
	"age";
	"present" - with a max length of 100 characters;
	"party" - should contain both date and time, with time zone because the guests are coming from different countries;

-- Language: sql

CREATE TABLE minions_birthdays (
    id serial PRIMARY KEY,
    "name" character varying(50) NOT NULL,
    date_of_birth date NOT NULL,
    age integer NOT NULL,
    present character varying(100) NOT NULL,
    party timestamp with time zone NOT NULL
);

-- Language: sql

13.	* Insert Into
-- Let's INSERT data into the "minions_info" table.
-- name	code	task	banana	email	equipped	mood
-- Mark	GKYA	Graphing Points	3265.265	mark@minion.com	false	happy
-- Mel	HSK	Science Investigation	54784.996	mel@minion.com	true	stressed
-- Bob	HF	Painting	35.652	bob@minion.com	true	happy
-- Darwin	EHND	Create a Digital Greeting	321.958	darwin@minion.com	false	relaxed
-- Kevin	KMHD	Construct with Virtual Blocks	35214.789	kevin@minion.com	false	happy
-- Norbert	FEWB	Testing	3265.500	norbert@minion.com	true	sad
-- Donny	L	Make a Map	8.452	donny@minion.com	true	happy


-- Language: sql

INSERT INTO minions_info (name, code, task, banana, email, equipped, mood)
VALUES ('Mark', 'GKYA', 'Graphing Points', 3265.265, 'mark@minion.com', false, 'happy'),
       ('Mel', 'HSK', 'Science Investigation', 54784.996, 'mel@minion.com', true, 'stressed'),
       ('Bob', 'HF', 'Painting', 35.652, 'bob@minion.com', true, 'happy'),
       ('Darwin', 'EHND', 'Create a Digital Greeting', 321.958, 'darwin@minion.com', false, 'relaxed'),
       ('Kevin', 'KMHD', 'Construct with Virtual Blocks', 35214.789, 'kevin@minion.com', false, 'happy'),
       ('Norbert', 'FEWB', 'Testing', 3265.500, 'norbert@minion.com', true, 'sad'),
       ('Donny', 'L', 'Make a Map', 8.452, 'donny@minion.com', true, 'happy');

-- Language: sql

14.	* Select
Gru has a specific requirement to fetch information from the "minions_info" table. Therefore, he has approached you to write a SQL query that can retrieve the "name", "task", "email", and "banana" columns for him.

-- Language: sql

SELECT name, task, email, banana
FROM minions_info;

-- Language: sql

15.	Truncate the Table
Kevin has shown you what he learned in the PostgreSQL course and deleted all data stored in the database. Can you utilize the query he wrote to TRUNCATE all the records in the "minions_info" table? 

-- Language: sql

TRUNCATE minions_info;

-- Language: sql

16.	Drop the Table
-- Gru disagrees with Dr. Nefario's idea for the parties and requests that you delete the "minions_birthdays" table.

-- Language: sql

DROP TABLE minions_birthdays;

-- Language: sql