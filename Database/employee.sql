-- Disable auto value increment and set transaction mode
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

-- Create the employee database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `employee_management` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `employee_management`;

-- Drop the WFHRequest table first (because it references Employee)
DROP TABLE IF EXISTS `WFHRequest`;

-- Drop the Employee table next
DROP TABLE IF EXISTS `Employee`;

-- Create the Employee table based on the provided schema
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

-- Create the WFHRequest table, referencing Employee's Staff_ID
CREATE TABLE IF NOT EXISTS `WFHRequest` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `staff_id` INT NOT NULL,
  `requested_dates` VARCHAR(255) NOT NULL,
  `time_of_day` VARCHAR(10) NOT NULL,  -- AM, PM, Full Day
  `reason` VARCHAR(255),
  `status` VARCHAR(20) DEFAULT 'Pending',
  FOREIGN KEY (`staff_id`) REFERENCES `Employee`(`Staff_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Load local data from CSV into the Employee table (might need to edit my.ini file to allow local infile if your sql cant run this)
LOAD DATA LOCAL INFILE 'C:/Users/wuhao/OneDrive/Documents/GitHub/SPM_G4_Team5/Database/employeenew.csv'
INTO TABLE Employee
FIELDS TERMINATED BY ','  
ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 ROWS  -- Skip the header row
(Staff_ID, Staff_FName, Staff_LName, Dept, Position, Country, Email, Reporting_Manager, Role);

COMMIT;
