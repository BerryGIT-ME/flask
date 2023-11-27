from langchain.prompts import PromptTemplate
import sys

decode_model_prompt_template = PromptTemplate(
        input_variables=['conversation'],
        template="""
I have conversation between an employee of an e-commerce store and a customer. 
As an AI agent, I want you to summarize this exchange and return a single sentence that explains best explains what
the customer is doing based on the statments of the customer

Your reply must be of one of the three following classes.
1. The customer may be greeting in which case you must reply with - "Greeting"
2. The customer is searching for a product but you are not sure what it is, in that case you must reply with - "The customer is searching for top rated products"
3. The custoner is searching for a product and has described the product, in that case summarize the product e.g you can reply with - "The customer is searching for red gucci bags"
4. The customer is done searching. An example of when the customer is done searching is when they imply that they have found what they are searching for, in that case you must reply with - "Finalize"

Here is the conversation
{conversation}
Please summarize the exchange into a single sentence explaining what the customer is doing and remember the 4 classes above. Always reply with a single sentence
e.g 
1. if the customer is greeting, you must reply with - "Greetings"
2. if the customer is not sure of the product they want, you must reply with - "The customer is searching for top rated products"
3. if the customer has described the prouduct, you must reply witha summary of product description e.g You can reply with - "The customer is looking for red gucci bags" or "The customer is looking for phones" or "The customer is looking for a hand bag" etc
4. If the custmer implies that they have seen the product they need, you must reply with - "finalize"
Do not include anyother text in your reply only reply with the texts format as already described

"""
    )

sql_model_prompt_template = PromptTemplate(
        input_variables=['customer_needs'],
        template="""
Here is the schema of an e-commerce database;
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
                     
The Category names in the database are;  
1. Fashion 
2. Appliance 
3. Phones and Tablets
4. Grocery
                     
Use this knowledge to decide when to filter by categories or not.

You are the database administrator of an ecommerce shop with that database schema, You recieve descriptions of products that customers are
interested in and you respond with only the sql query that can satisfy or come close to satisfying the customers request.
      
Here is one such request
customers request - {customer_needs}

Generate the sql query that can satisfy this request, return only the sql query and nothing else. Do not use exact matches and try
generalize the sql query so that even if exact matches are not present, items that are close can be returned.
"""
)

system_message = """
You are an AI assistant of an ecomerce store, you role is to help customers find the product they would like.
The products we have are in the following categories;
1. Fashion 
2. Appliance 
3. Phones and Tablets
4. Grocery
            
Make it clear to the customer that we only have products in those categories.
            
Our products also have attributes such as;
1. color - which is the color of the product
2. size - which is the size of the product
            
These attributes may not be provided, so where neccessary, feel free to request for additional information
about those attributes
"""
