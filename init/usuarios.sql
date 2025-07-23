-- Crear base de datos con codificación UTF-8
CREATE DATABASE IF NOT EXISTS usuariosdb
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Seleccionar la base de datos
USE usuariosdb;

-- Crear tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Insertar registros en usuarios
INSERT INTO usuarios (nombre, apellido, email, password) VALUES
('Mateo', 'Torres', 'mateo.torres@epn.edu.ec', '1234'),
('Mireya', 'García', 'mireya.garcia@epn.edu.ec', 'mire1234'),
('Anthony', 'Astudillo', 'anthony.astudillo@epn.edu.ec', 'antuan1234'),
('Walter', 'Cobacango', 'walter.cobacango@epn.edu.ec', 'walter1234');
