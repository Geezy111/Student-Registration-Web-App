-- CSC 312 - Web Application Development (Tutor-Marked Assessment)
-- ClassMate: creates the database and the tbl_user table
-- Usage (PowerShell):  mysql -u root -p -e "source schema.sql"

CREATE DATABASE IF NOT EXISTS classmate_db;
USE classmate_db;

CREATE TABLE IF NOT EXISTS tbl_user (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(25)  NOT NULL UNIQUE,
    password_hash CHAR(60)     NOT NULL,          -- bcrypt hashes are always 60 characters
    joined_on     DATETIME     DEFAULT CURRENT_TIMESTAMP
);
