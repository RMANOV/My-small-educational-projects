1.	Find Book Titles
Write an SQL query to find all books whose titles start with "The". Order the result by id. 

--Language:SQL
SELECT title FROM books WHERE title LIKE 'The%' ORDER BY id;

--Language:SQL

2.	Replace Titles
Write an SQL query to find all books, whose titles start with "The" and replace the substring with 3 asterisks. 
Retrieve data about the updated titles. 
Order the result by id. Submit your query statements.
Example
title
*** Mysterious Affair at Styles
*** Big Four
*** Murder at the Vicarage
*** Mystery of the Blue Train
*** Ring
*** Alchemist
*** Fifth Mountain
*** Zahir

--Language:SQL

Replace(SELECT title FROM books WHERE title LIKE 'The%', '*** ') ORDER BY id;

SELECT 
