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
    user_id INTEGER REFERENCES users,
    visible BOOLEAN DEFAULT TRUE
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
    price INTEGER, 
    user_id INTEGER REFERENCES users,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE invoices (
    id SERIAL PRIMARY KEY, 
    biller_id INTEGER REFERENCES customers, 
    customer_id INTEGER REFERENCES customers,
    form_time TEXT,
    invoice_number TEXT UNIQUE, 
    product_one_id INTEGER REFERENCES products,
    product_two_id INTEGER REFERENCES products,
    product_three_id INTEGER REFERENCES products,
    product_four_id INTEGER REFERENCES products,
    product_five_id INTEGER REFERENCES products,
    margin INTEGER,
    no_margin_sum INTEGER,
    sum INTEGER,
    user_id INTEGER REFERENCES users,
    visible BOOLEAN DEFAULT TRUE
);



