-- Crear base de datos con codificación UTF-8
CREATE DATABASE IF NOT EXISTS productosdb
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Seleccionar la base de datos
USE productosdb;

-- Crear tabla productos
CREATE TABLE IF NOT EXISTS productos (
    codigo INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    unidad INT NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    UNIQUE (codigo)
);

-- Insertar registros en productos
INSERT INTO productos (nombre, codigo, descripcion, unidad, categoria) VALUES
('Lápiz HB', 1234, 'Lápiz de grafito dureza HB', 5, 'papelería'),
('Cuaderno A4', 1235, 'Cuaderno de hojas A4 rayadas, 100 páginas', 3, 'papelería');
