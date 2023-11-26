from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema.document import Document
from dotenv import load_dotenv
import pandas as pd

from db.initialize import get_db_connection



def vectorize_database():
    connection = get_db_connection()

    # read all the data in 
    products = pd.read_sql("Select * from products",connection)
    categories = pd.read_sql("select * from categories", connection)
    sizes = pd.read_sql("Select * from sizes", connection)
    colors = pd.read_sql("select * from colors", connection)

    categories = categories.rename(columns={'name': "category"})
    sizes = sizes.rename(columns={'name': "size"})
    colors = colors.rename(columns={'name': "color"})

    # merge all the data to a single table

    merged_products = products.merge(
        categories, how='left', on='category_id'
        ).merge(sizes, how='left', on='size_id').merge(colors, how='left', on='color_id')
    
    document_list = list()
    for i,row in merged_products.iterrows():
        text =f"""
    Name - {row['name']}
    description - {row['description']}
    category - {row['category']}
    color - {row['color']}
    """
        doc = Document(page_content=text, metadata=row.to_dict())
        document_list.append(doc)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(document_list, embeddings)

    return db