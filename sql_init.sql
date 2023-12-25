CREATE DATABASE IF NOT EXISTS ocr;

USE ocr;

CREATE TABLE IF NOT EXISTS thai_id_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    identification_number VARCHAR(20) NOT NULL,
    date_of_issue DATE,
    date_of_expiry DATE,
    date_of_birth DATE
);
