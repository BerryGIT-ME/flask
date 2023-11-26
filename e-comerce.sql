-- Categories Table
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    name VARCHAR(255)
);

-- Colors Table
CREATE TABLE colors (
    color_id INT PRIMARY KEY,
    name VARCHAR(50)
);

-- Sizes Table
CREATE TABLE sizes (
    size_id INT PRIMARY KEY,
    name VARCHAR(50)
);

-- Products Table
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    stock_quantity INT,
    category_id INT,
    color_id INT,
    size_id INT,
    product_rating DECIMAL(3, 2),
    product_image_url VARCHAR(255),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (color_id) REFERENCES colors(color_id),
    FOREIGN KEY (size_id) REFERENCES sizes(size_id)
);

-- Indexes
CREATE INDEX idx_product_id ON products(product_id);
CREATE INDEX idx_category_id ON products(category_id);
CREATE INDEX idx_color_id ON products(color_id);
CREATE INDEX idx_size_id ON products(size_id);
