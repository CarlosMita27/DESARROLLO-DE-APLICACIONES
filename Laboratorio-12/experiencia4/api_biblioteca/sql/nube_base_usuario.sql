-- En el cliente SQL conectado al servidor en la nube (con el usuario administrador)
CREATE DATABASE IF NOT EXISTS biblioteca
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'biblioteca_app'@'%' IDENTIFIED BY 'ClaveGeneradaPorElProveedor';
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON biblioteca.* TO 'biblioteca_app'@'%';
