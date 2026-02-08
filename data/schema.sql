-- 1. Sequence for Author IDs (PKs)
CREATE SEQUENCE AuthorID_Sequence
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1
    NO MAXVALUE; -- Define max value if required
GO

-- 2. Sequence for Book IDs (PKs)
CREATE SEQUENCE BookID_Sequence
    START WITH 100
    INCREMENT BY 1
    MINVALUE 100
    NO MAXVALUE;
GO

-- Root (Parent) Table: AUTHOR
-- The PK will be populated by the AuthorID_Sequence on INSERT.

CREATE TABLE Author (
    author_id INT PRIMARY KEY,         -- Primary Key (PK)
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    birth_year INT
);
GO

---

-- Dependent (Child) Table: BOOK
-- The FK (author_id) links back to the Author table, establishing the 1:N relationship.

CREATE TABLE Book (
    book_id INT PRIMARY KEY,           -- Primary Key (PK) populated by BookID_Sequence
    title NVARCHAR(255) NOT NULL,
    publication_year INT,

    -- Foreign Key (FK) column linking to the Author
    author_id INT NOT NULL,

    -- Define the Foreign Key constraint for referential integrity
    CONSTRAINT FK_Book_Author
        FOREIGN KEY (author_id)
        REFERENCES Author(author_id)
        ON DELETE NO ACTION            -- Referential Action: prevent deletion if linked
        ON UPDATE NO ACTION            -- Referential Action: prevent update if linked
);
GO