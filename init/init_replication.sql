-- Script para configurar la replicación maestro-esclavo
-- Este script debe ejecutarse en el servidor maestro

-- Crear usuario para replicación
CREATE USER IF NOT EXISTS 'replica'@'%' IDENTIFIED BY '123456';
GRANT REPLICATION SLAVE ON *.* TO 'replica'@'%';
FLUSH PRIVILEGES;

-- Mostrar el estado del maestro (útil para configurar el esclavo)
SHOW MASTER STATUS;

-- Crear las bases de datos si no existen
CREATE DATABASE IF NOT EXISTS usuariosdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS productosdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
