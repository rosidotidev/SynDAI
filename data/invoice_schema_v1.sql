-- ******************************************************
-- 1. SEQUENCE CREATION
--    Sequences are used to generate unique IDs for all tables.
-- ******************************************************

CREATE SEQUENCE Seq_Customer_ID
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1
    NO MAXVALUE
    CACHE 10;
GO

CREATE SEQUENCE Seq_Product_ID
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1
    NO MAXVALUE
    CACHE 10;
GO

CREATE SEQUENCE Seq_Invoice_ID
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1
    NO MAXVALUE
    CACHE 10;
GO

CREATE SEQUENCE Seq_Invoice_Item_ID
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1
    NO MAXVALUE
    CACHE 10;
GO

---
-- ******************************************************
-- 2. CUSTOMER TABLE
--    Primary Key: customer_id.
--    'code' is the unique soft reference key.
-- ******************************************************

CREATE TABLE Customer (
    -- PK manually populated using Seq_Customer_ID
    customer_id INT PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    last_name NVARCHAR(100) NOT NULL,
    code NVARCHAR(50) NOT NULL UNIQUE, -- Soft reference key for Invoice
    day_of_birth DATE NULL
);
GO

---
-- ******************************************************
-- 3. PRODUCT TABLE
--    Primary Key: product_id.
--    'code' is the unique soft reference key.
-- ******************************************************

CREATE TABLE Product (
    -- PK manually populated using Seq_Product_ID
    product_id INT PRIMARY KEY,
    code NVARCHAR(50) NOT NULL UNIQUE, -- Soft reference key for Invoice_Item
    name NVARCHAR(255) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL
);
GO

---
-- ******************************************************
-- 4. INVOICE TABLE (1 side of 1:N)
--    Primary Key: invoice_id.
--    Contains soft reference 'customer_code'.
-- ******************************************************

CREATE TABLE Invoice (
    -- PK manually populated using Seq_Invoice_ID
    invoice_id INT PRIMARY KEY,
    invoice_date DATETIME2(0) NOT NULL DEFAULT GETDATE(),
    customer_code NVARCHAR(50) NOT NULL, -- Soft reference to Customer
    total_amount DECIMAL(19, 4) NOT NULL DEFAULT 0
);
GO

---
-- ******************************************************
-- 5. INVOICE_ITEM TABLE (N side of 1:N)
--    Primary Key: invoice_item_id.
--    Hard FK to Invoice, Soft FK to Product.
--    line_total must be calculated by the application logic.
-- ******************************************************

CREATE TABLE Invoice_Item (
    -- PK manually populated using Seq_Invoice_Item_ID
    invoice_item_id INT PRIMARY KEY,
    invoice_id INT NOT NULL,
    line_number INT NOT NULL,
    product_code NVARCHAR(50) NOT NULL, -- Soft reference to Product
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    line_total DECIMAL(10, 2) NOT NULL, -- Field for line total (must be calculated externally as unit_price*quantity)

    -- Logical consistency constraint
    CONSTRAINT UQ_InvoiceItem_Line UNIQUE NONCLUSTERED (invoice_id, line_number),

    -- HARD REFERENCE (FOREIGN KEY) for the 1:N relationship
    CONSTRAINT FK_InvoiceItem_Invoice FOREIGN KEY (invoice_id)
        REFERENCES Invoice (invoice_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
GO