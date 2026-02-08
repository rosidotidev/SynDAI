-- DDL Script for creating SEQUENCEs and TABLEs for the School -> Classroom -> Student -> Activity hierarchy.

-- =================================================================================
-- 1. SEQUENCE DEFINITIONS
-- These sequences will be used to populate the Primary Keys (PKs) of the tables.
-- =================================================================================

-- Sequence for School IDs (Root)
CREATE SEQUENCE SchoolID_Sequence
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1
    NO MAXVALUE;
GO

-- Sequence for Classroom IDs (Child of School)
CREATE SEQUENCE ClassroomID_Sequence
    START WITH 10
    INCREMENT BY 1
    MINVALUE 10
    NO MAXVALUE;
GO

-- Sequence for Student IDs (Child of Classroom)
CREATE SEQUENCE StudentID_Sequence
    START WITH 100
    INCREMENT BY 1
    MINVALUE 100
    NO MAXVALUE;
GO

-- Sequence for Activity IDs (Child of Student)
CREATE SEQUENCE ActivityID_Sequence
    START WITH 1000
    INCREMENT BY 1
    MINVALUE 1000
    NO MAXVALUE;
GO

-- =================================================================================
-- 2. TABLE DEFINITIONS
-- Tables are created in dependency order (from root to leaf).
-- =================================================================================

-- A. School (Root Table)
-- PK: school_id (populated by SchoolID_Sequence)
CREATE TABLE School (
    school_id INT PRIMARY KEY,
    school_name NVARCHAR(100) NOT NULL,
    address NVARCHAR(255)
);
GO

-- B. Classroom (Child of School)
-- PK: classroom_id / FK: school_id
CREATE TABLE Classroom (
    classroom_id INT PRIMARY KEY,
    room_number NVARCHAR(10) NOT NULL,
    capacity INT,

    -- Foreign Key pointing to SCHOOL
    school_id INT NOT NULL,

    CONSTRAINT FK_Classroom_School
        FOREIGN KEY (school_id)
        REFERENCES School(school_id)
        ON DELETE CASCADE             -- If the School is deleted, the Classrooms are deleted
        ON UPDATE NO ACTION           -- PK updates are not allowed
);
GO

-- C. Student (Child of Classroom)
-- PK: student_id / FK: classroom_id
CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    enrollment_date DATE NOT NULL,

    -- Foreign Key pointing to CLASSROOM
    classroom_id INT NOT NULL,

    CONSTRAINT FK_Student_Classroom
        FOREIGN KEY (classroom_id)
        REFERENCES Classroom(classroom_id)
        ON DELETE NO ACTION           -- Prevents deletion of Classroom if Students are assigned
        ON UPDATE NO ACTION
);
GO

-- D. Activity (Child of Student)
-- PK: activity_id / FK: student_id
CREATE TABLE Activity (
    activity_id INT PRIMARY KEY,
    activity_name NVARCHAR(100) NOT NULL,
    activity_date DATETIME NOT NULL,

    -- Foreign Key pointing to STUDENT
    student_id INT NOT NULL,

    CONSTRAINT FK_Activity_Student
        FOREIGN KEY (student_id)
        REFERENCES Student(student_id)
        ON DELETE CASCADE             -- If the Student is deleted, their Activities are deleted
        ON UPDATE NO ACTION
);
GO