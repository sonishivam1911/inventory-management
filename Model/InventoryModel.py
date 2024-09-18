from Data import CommonDataFetch
from Data.Query import InventoryQueries

def fetch_products_service(request):
    where_clause_list = []

    if request.sku:
        sku_name_filter = f"sku = '{request.sku}'"
        where_clause_list.append(sku_name_filter)
    
    if request.brand_name:
        brand_name_filter = f"brand_name = '{request.brand_name}'"
        where_clause_list.append(brand_name_filter)
    
    if request.category_name:
        category_name_filter = f"category_name = '{request.category_name}'"
        where_clause_list.append(category_name_filter)

    
    if len(where_clause_list) > 1:
        where_clause = "where " +  " and ".join(where_clause_list)
    elif len(where_clause_list) == 1:
        where_clause = "where " +  " ".join(where_clause_list)
    else:
        where_clause = ""

    query = InventoryQueries.fetch_products_query.format(whereclause=where_clause)
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    return output_dataframe

def fetch_brand_name():
    query = InventoryQueries.fetch_brands_query
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    return list(output_dataframe["brand_name"])


def fetch_category_name():
    query = InventoryQueries.fetch_category_query
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    return list(output_dataframe["category_name"])


def fetch_table_schema(table_name):
    query = InventoryQueries.fetch_table_schema.format(table_name=table_name)
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    return output_dataframe.to_dict('records')

def create_inventory(procedure_inputs):
    CommonDataFetch.execute_procedures('create_product',procedure_inputs)

def check_product_id(function_arguments):
    query = InventoryQueries.check_product_id_function.format(function_arguments=function_arguments)
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    return output_dataframe

def update_price_service(procedure_inputs,procedure_name):
    CommonDataFetch.execute_procedures(procedure_name,procedure_inputs)

def delete_product(product_id):
    CommonDataFetch.execute_procedures('delete_product',[product_id])
    return 