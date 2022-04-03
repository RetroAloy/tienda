instructions = [
    'SET FOREIGN_KEY_CHECKS=0;' ,
    'DROP TABLE IF EXISTS product;',
    'DROP TABLE IF EXISTS user;',
    'DROP TABLE IF EXISTS rol;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
        CREATE TABLE product (
            id INT PRIMARY KEY AUTO_INCREMENT,
            productname VARCHAR(50) UNIQUE NOT NULL,
            price DECIMAL(6,2) NOT NULL,
            quantity INT NOT NULL,
            description VARCHAR(50)
        );
    """,
    """
        CREATE TABLE rol (
            id INT PRIMARY KEY AUTO_INCREMENT,
            rolname VARCHAR(30) UNIQUE NOT NULL
        ); 
    """,
    """
        CREATE TABLE user (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(150) NOT NULL,
            rol_id INT,
            FOREIGN KEY ( rol_id ) REFERENCES rol ( id )
        );
    """,
    "INSERT INTO rol (rolname) VALUES ('Administrador');",
    "INSERT INTO rol (rolname) VALUES ('Empleado');"
]