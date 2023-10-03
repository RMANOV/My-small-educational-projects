--Language:SQL

-- 1.	Find Book Titles
-- Write an SQL query to find all books whose titles start with "The". Order the result by id. 

--Language:SQL
SELECT title FROM books WHERE title LIKE 'The%' ORDER BY id;

--Language:SQL

-- 2.	Replace Titles
-- Write an SQL query to find all books, whose titles start with "The" and replace the substring with 3 asterisks. 
-- Retrieve data about the updated titles. 
-- Order the result by id. Submit your query statements.
-- Example
-- title
-- *** Mysterious Affair at Styles
-- *** Big Four
-- *** Murder at the Vicarage
-- *** Mystery of the Blue Train
-- *** Ring
-- *** Alchemist
-- *** Fifth Mountain
-- *** Zahir

--Language: SQL

UPDATE books
SET title = '***' || SUBSTRING(title FROM 4)
WHERE title LIKE 'The%';

SELECT title FROM books WHERE title LIKE '***%' ORDER BY id;

--Language: SQL

-- 3.	Triangles on Bookshelves
-- Write an SQL query to calculate the area of triangles with a given side and height from table triangles.
-- 	Display the resulting table with columns id and area. Order by id.
-- Submit your query statements. 
-- Example
-- id	area
-- 1	4.0000000000000000
-- 2	9.0000000000000000
-- 3	6.7500000000000000
-- 4	48.0000000000000000
-- 5	7.5000000000000000

--Language: SQL

SELECT id, (side * height) / 2 AS area
FROM triangles
ORDER BY id;

--Language: SQL

-- 4.	Format Costs
-- Write an SQL query to get each book’s title and cost (cost as modified_price) and format the output to 3 digits after the decimal point. Order by id. 
-- Submit your query statements. 
-- Example
-- title	modified_price
-- Unfinished Portrait	15.990
-- The Mysterious Affair at Styles	17.990
-- The Big Four	14.990
-- The Murder at the Vicarage	13.990
-- The Mystery of the Blue Train	12.990

--Language: SQL

SELECT title, CAST(cost AS numeric(10,3)) AS modified_price
FROM books
ORDER BY id;

--Language: SQL

-- 5.	Year of Birth
-- Write an SQL query to get the year of birth for each author. Your query should return:
-- 	first_name – the first name of each author
-- 	last_name – the last name of each author
-- 	year – the year of birth of each author
-- Submit your query statements. 
-- Example
-- first_name	last_name	year
-- Agatha 	Christie	1890
-- William 	Shakespeare	1564
-- Danielle 	Schuelein-Steel	1947
-- Joanne 	Rowling	1965
-- Lev 	Tolstoy	1828

--Language: SQL

SELECT first_name, last_name, EXTRACT(YEAR FROM born) AS year
FROM authors;

--Language: SQL

-- 6.	Format Date of Birth
-- Write an SQL query to display the author’s last name and date of birth in the format 15 (Mon) Sep 1890. 
-- 	use date format: DD (Dy) Mon YYYY
-- 	born field(formatted) as Date of Birth
-- 	last_name as Last Name
-- Submit your query statements. 
-- Example
-- Last Name	Date of Birth
-- Christie	15 (Mon) Sep 1890
-- Shakespeare	26 (Sun) Apr 1564
-- Schuelein-Steel	14 (Mon) Jul 1947
-- Rowling	31 (Sat) Jul 1965
-- Tolstoy	09 (Tue) Sep 1828

--Language: SQL

SELECT last_name, TO_CHAR(born, 'DD (Dy) Mon YYYY') AS "Date of Birth"
FROM authors;

--Language: SQL

7.	Harry Potter Books
Write an SQL query to retrieve titles of all the Harry Potter books. Order the information by id. 
Submit your query statements.
	Use the WHERE clause with the LIKE operator.
Example
title
Harry Potter and the Philosophers Stone
Harry Potter and the Chamber of Secrets
Harry Potter and the Prisoner of Azkaban
Harry Potter and the Goblet of Fire

--Language: SQL

SELECT title FROM books WHERE title LIKE 'Harry Potter%' ORDER BY id;

--Language: SQL