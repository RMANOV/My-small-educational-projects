
CREATE TABLE authors (
	id serial PRIMARY KEY,
	first_name VARCHAR(30) NOT NULL,
	middle_name VARCHAR(30),
	last_name VARCHAR(30) NOT NULL,
	born DATE NOT NULL,
	died DATE
);

INSERT INTO authors(id,first_name, middle_name, last_name, born, died) VALUES
	(1,'Agatha', 'Mary Clarissa','Christie', '1890-09-15', '1976-01-12'),
	(2,'William', NULL,'Shakespeare', '1564-04-26', '1616-04-23'),
	(3,'Danielle', 'Fernandes Dominique', 'Schuelein-Steel', '1947-07-14', NULL),
	(4,'Joanne', NULL,'Rowling' , '1965-07-31', NULL),
	(5,'Lev', 'Nikolayevich', 'Tolstoy', '1828-09-09', '1910-11-20'),
	(6,'Paulo', 'Coelho de', 'Souza', '1947-08-24', NULL),
	(7,'Stephen', 'Edwin', 'King', '1947-09-21', NULL),
	(8,'John', 'Ronald Reuel', 'Tolkien', '1892-01-03', '1973-09-02'),
	(9,'Erika', NULL, 'Mitchell_ELJ', '1963-03-07', NULL);
	
CREATE TABLE books (
	id serial PRIMARY KEY,
	title VARCHAR(100) NOT NULL,
	author_id INT NOT NULL,
	year_of_release DATE,
	description TEXT,
	cost decimal NOT NULL,
	CONSTRAINT fk_author_id FOREIGN KEY (author_id) REFERENCES authors(id)
);

INSERT INTO books(author_id,title, year_of_release,cost, description) VALUES
	(1,'Unfinished Portrait', '1930-01-01', 15.99, 'Unfinished Portrait is a semi-autobiographical novel written by Agatha Christie and first published in the UK by Collins in March 1934 and in the US by Doubleday later in the same year. The British edition retailed for seven shillings and sixpence (7/6) and the US edition at $2.00. It is the second of six novels Christie wrote under the pen name Mary Westmacott.'),
	(1,'The Mysterious Affair at Styles', '1920-01-01',17.99, 'The Mysterious Affair at Styles is the first detective novel by British writer Agatha Christie, introducing her fictional detective Hercule Poirot. It was written in the middle of the First World War, in 1916, and first published by John Lane in the United States in October 1920.'),
	(1,'The Big Four', '1927-01-01',14.99, NULL),
	(1,'The Murder at the Vicarage', '1930-01-01',13.99, NULL),
	(1,'The Mystery of the Blue Train', '1928-01-01',12.99, NULL),
	(2,'Julius Caesar', '1599-01-01',11.99, NULL),
	(2,'Timon of Athens', '1607-01-01',13.99, NULL),
	(2,'As You Like It', '1600-01-01',18.99, NULL),
	(2,'A Midsummer Nights Dream', '1595-01-01',15.99, NULL),
	(3,'Going Home', '1973-01-01',15.99, NULL),
	(3,'The Ring', '1980-01-01',14.99, NULL),
	(3,'Secrets', '1985-01-01',15.99, NULL),
	(3,'Message From Nam', '1990-01-01',13.99, NULL),
	(4,'Career of Evil', '2015-01-01',15.99, NULL),
	(4,'Harry Potter and the Philosophers Stone','1997-01-01',19.99, NULL),
	(4,'Harry Potter and the Chamber of Secrets','1998-01-01',19.99, NULL),
	(4,'Harry Potter and the Prisoner of Azkaban','1999-01-01',19.99, NULL),
	(4,'Harry Potter and the Goblet of Fire','2000-01-01',19.99, NULL),
	(4,'Harry Potter and the Order of the Phoenix','2003-01-01',19.99, NULL),
	(4,'Harry Potter and the Half-Blood Prince','2005-01-01',19.99, NULL),
	(4,'Harry Potter and the Deathly Hallows','2007-01-01',19.99, NULL),
	(4,'Harry Potter and the Deathly Hallows','2007-01-01',15.99, NULL),
	(5,'Anna Karenina','1877-01-01',15.99, NULL),
	(5,'War And Peace','1869-01-01',30, NULL),
	(5,'Boyhood','1854-01-01',15.99, NULL),
	(6,'By the River Piedra I Sat Down and Wept','1994-01-01',15.99, NULL),
	(6,'The Alchemist','1988-01-01',15.99, NULL),
	(6,'The Fifth Mountain','1996-01-01',15.99, NULL),
	(6,'The Zahir','2005-01-01',15.99, NULL),
	(7,'Rage','1977-01-01',13.99, NULL),
	(7,'The Dead Zone','1979-01-01',13.99, NULL),
	(7,'It','1986-01-01',13.99, NULL),
	(8,'The Hobbit','1937-01-01',20.99, NULL),	
	(8,'The Adventures of Tom Bombadil','1962-01-01',13.99, NULL);

CREATE TABLE triangles (
	id serial PRIMARY KEY,
	side decimal NOT NULL,
	height decimal NOT NULL
	);

INSERT INTO triangles(side, height) VALUES 
	(2, 4),
	(1, 18),
	(4.5, 3),
	(8, 12),
	(3, 5);
