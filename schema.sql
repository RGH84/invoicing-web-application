CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY, 
    customer_name TEXT, 
    address TEXT, 
    phonenumber TEXT, 
    business_id TEXT, 
    user_id INTEGER REFERENCES users
);

CREATE TABLE visitors (
    id SERIAL PRIMARY KEY, 
    time TIMESTAMP
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY, 
    product_name TEXT, 
    type TEXT, 
    product_number TEXT, 
    price TEXT, 
    user_id INTEGER REFERENCES users
);



