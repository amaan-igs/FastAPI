CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    price DECIMAL(10,2),
    user_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(username) ON DELETE CASCADE
);
-- PostgreSQL

INSERT INTO books (title, author, genre, price, user_id) VALUES
('Atomic Habits', 'James Clear', 'Productivity', 1100.00, 'amaan'),
('It Ends with Us', 'Colleen Hoover', 'Romance', 1200.00, 'amaan'),
('The 5 AM Club', 'Robin Sharma', 'Self-Help', 1500.00, 'ayaan'),
('Deep Work', 'Cal Newport', 'Productivity', 1300.00, 'Umer Siddiqui'),
('The Psychology of Money', 'Morgan Housel', 'Finance', 1400.00, 'Umer Siddiqui');