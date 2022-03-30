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
            price DECIMAL(3,2) NOT NULL,
            quantity INT NOT NULL
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
            password VARCHAR(100) NOT NULL,
            rol_id INT,
            FOREIGN KEY ( rol_id ) REFERENCES rol ( id )
        );
    """
    
]