CREATE DATABASE IF NOT EXISTS ocr;

USE ocr;

CREATE TABLE IF NOT EXISTS thai_id_cards (
    id INT PRIMARY KEY AUTO_INCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(10),
    ocr_result JSON
);