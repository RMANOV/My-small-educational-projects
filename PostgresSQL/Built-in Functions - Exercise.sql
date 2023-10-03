--Language: SQL

1.	Select Cities
Write a SQL query to retrieve all available information about the "cities", sorted by "id". 
Submit your query for this task in the Judge system.
Example 
id	name 	state	area
1	Redmond	Washington	44.640
2	Redmond	Washington	44.640
…	…	…	…
4	Calgary	Canada	820.620
…	…	…	…
12	Bellevue	[null]	97.140
…	…	…	…
62	Sofia	Bulgaria	492.000
63	Sofia	Bulgaria	492.000

-- Solution:
SELECT * FROM cities
ORDER BY id;
