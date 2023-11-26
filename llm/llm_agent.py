import os
from openai import OpenAI 
from langchain.llms import OpenAI as langchain_OpenAI
from llm.prompt_templates import system_message, decode_model_prompt_template, sql_model_prompt_template
from db.initialize import get_db_connection
import pandas as pd
import sys
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


connection = get_db_connection()
model_temperature = 0.6
similarity_score = 0.6
k_nearest_neigbors = 5

api_key = os.getenv('OPEN_AI_API_KEY')


def decode_customer_needs(messages):
    conversation = "\n"

    for chat in messages:
        role = chat['role']
        content = chat['content']
        if role == 'assistant':
            conversation = conversation + "employee - " + content + "\n"
        elif role == 'user':
            conversation = conversation + "customer - " + content + "\n" 
        
    model = langchain_OpenAI(temperature=model_temperature)
    customer_needs = model(decode_model_prompt_template.format(**{'conversation': conversation})).replace('\n', '')

    return customer_needs

def execute_query_for_costomer_needs(customer_needs: str):

    model = langchain_OpenAI(temperature=model_temperature)
    sql_query = model(sql_model_prompt_template.format(**{'customer_needs': customer_needs}))
    sql_query = sql_query.replace('\n', ' ')
    
    # connection = get_db_connection()
    connection = get_db_connection()
    results = pd.read_sql(sql_query, connection)
    log(sql_query)

    return [value for key, value in results.T.to_dict().items()]

def get_product_similar_to_customer_needs(customer_need: str):
    embeddings = OpenAIEmbeddings()
    try: 
        new_db = FAISS.load_local("ecommerce_index", embeddings)
        docs = new_db.similarity_search_with_relevance_scores(customer_need, k_nearest_neigbors)
        return [d.metadata for d, score in docs if score > similarity_score]
    except:
        return []

def combine_query_results_and_similar_products(total_results):
    # this simply removes any duplicates
    unique_products = dict()
    for product in total_results:
        unique_products[product['product_id']] = product
    
    return [value for key,value in unique_products.items()]

    


def ai_chat(messages):
    try:
        client = OpenAI()
        customer_needs = decode_customer_needs(messages)
        log(customer_needs)
        query_results = execute_query_for_costomer_needs(customer_needs)
        log(f'total lenght of query items - {len(query_results)}')

        similar_results = get_product_similar_to_customer_needs(customer_needs)
        log(f'total len of similar products - {similar_results}')

        product_suggestions = combine_query_results_and_similar_products([*query_results, *similar_results])
        product_names = list(map(lambda x: {x['name']}, product_suggestions))
        log(f'product names suggested {product_names}')
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_message}, *messages]
        )

        message = response.choices[0].message.content

        if len(product_suggestions)>0:
            message = message + f"\n Here are {len(product_suggestions)} suggestions you might like"
            
        log('Done!!')
        return message, product_suggestions
    except Exception as e:
        log("Generated an error")
        raise e

def log(variable):
    print(variable, file=sys.stderr)