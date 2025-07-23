-- Configuración de replicación para MySQL 5.7
-- Este script se ejecuta en el esclavo

-- Detener la replicación si está activa
STOP SLAVE;

-- Configurar la conexión al maestro (sintaxis MySQL 5.7)
CHANGE MASTER TO
    MASTER_HOST='mysql_maestro_replicado',
    MASTER_USER='replica',
    MASTER_PASSWORD='123456',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=154;

-- Iniciar la replicación
START SLAVE;

-- Mostrar el estado del esclavo
SHOW SLAVE STATUS\G