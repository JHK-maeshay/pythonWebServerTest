DROP TABLE IF EXISTS safetensors;
CREATE TABLE safetensors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(127),
    file_type VARCHAR(63),
    volume BIGINT,
    descr VARCHAR(255),
    file_path VARCHAR(255),
    file_image_path VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;