-- Disable auto value increment and set transaction mode
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

-- Create the employee database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `employee_management` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `employee_management`;

-- Drop the Employee table if it exists (to reset the schema)
DROP TABLE IF EXISTS `Employee`;

-- Employee table based on the provided schema
CREATE TABLE IF NOT EXISTS `Employee` (
  `Staff_ID` INT NOT NULL,
  `Staff_FName` VARCHAR(50) NOT NULL,
  `Staff_LName` VARCHAR(50) NOT NULL,
  `Dept` VARCHAR(50) NOT NULL,
  `Position` VARCHAR(50) NOT NULL,
  `Country` VARCHAR(50) NOT NULL,
  `Email` VARCHAR(50) NOT NULL,
  `Reporting_Manager` INT,
  `Role` INT NOT NULL,
  PRIMARY KEY (`Staff_ID`),
  FOREIGN KEY (`Reporting_Manager`) REFERENCES `Employee`(`Staff_ID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Load data from CSV into the Employee table
LOAD DATA INFILE '/SPM_G4_Team5/Database/employeenew.csv'
INTO TABLE Employee
FIELDS TERMINATED BY ','  -- Assuming CSV is comma-separated
ENCLOSED BY '"'  -- Assuming fields are enclosed by double quotes
LINES TERMINATED BY '\n'
IGNORE 1 ROWS  -- Skip header row
(Staff_ID, Staff_FName, Staff_LName, Dept, Position, Country, Email, Reporting_Manager, Role);

COMMIT;