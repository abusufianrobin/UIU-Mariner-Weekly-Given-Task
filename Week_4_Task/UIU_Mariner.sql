create database UIU_Mariner;
use UIU_Mariner;

CREATE TABLE UserList (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO UserList (name, email, password, phone)
VALUES ('Abu Sufian Robin', 'robin@gmail.com', 'password123', '01407993877');

select *from UserList;