CREATE TABLE IF NOT EXISTS coordinators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) UNIQUE,
    offering YEAR
);

CREATE TABLE IF NOT EXISTS knowledge_trees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coordinator_id INT,
    course_id INT,
    s3_link VARCHAR(100),
    FOREIGN KEY (coordinator_id) REFERENCES coordinators(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);