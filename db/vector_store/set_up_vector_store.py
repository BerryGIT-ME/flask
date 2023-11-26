from dotenv import load_dotenv
load_dotenv()
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema.document import Document
from PIL import Image
import torch 
import tqdm as notebook_tqdm
import numpy as np
from transformers import CLIPTokenizerFast, CLIPProcessor, CLIPModel
import requests
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from db.initialize import get_db_connection


def initialize_vision_model(return_models=False):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_id = "openai/clip-vit-base-patch16"

    model = CLIPModel.from_pretrained(model_id).to(device)
    tokenizer = CLIPTokenizerFast.from_pretrained(model_id)
    processor = CLIPProcessor.from_pretrained(model_id)

    if return_models:
        return model, tokenizer, processor
    else:
        return
    
model, tokenizer, processor = initialize_vision_model(return_models=True)

def get_db_data():
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
    
    return merged_products


def vectorize_database():
    merged_products = get_db_data()
    
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

def get_image_embeddings(image: Image):
    image_input = processor(
        text=None,
        images=image,
        retun_tensor='pt'
    )['pixel_values']
    image_input_numpy = np.array(image_input)
    image_input = torch.from_numpy(image_input_numpy)
    model_embeddings_tensor = model.get_image_features(image_input)
    model_embeddings_numpy = model_embeddings_tensor.detach().numpy()
    return list(model_embeddings_numpy[0,:])

def vectorize_db_images():
    merged_products = get_db_data()
    data = {}

    for i, row in merged_products.iterrows():
        try:
            image_url = row['product_image_url']
            image = Image.open(requests.get(image_url, stream=True).raw)
            embeddings = get_image_embeddings(image=image)
            data[row['product_id']] = embeddings
        except:
            print(f"failed to fetch data for file {i}")
    return merged_products, data

def get_image_vector_from_file(image_path):
    image = Image.open(image_path)
    embeddngs = get_image_embeddings(image=image)
    return embeddngs

def get_similarity(embeddings, new_product_embeddings, k):
    embeddings.loc['new_prod'] = new_product_embeddings

    similarity_array = cosine_similarity(embeddings)
    df_sim = pd.DataFrame(similarity_array, columns=embeddings.index, index=embeddings.index)
    similar_ids = df_sim[['new_prod']].sort_values(by='new_prod', ascending=False).head(k).index
    return list(similar_ids)[1:]

