from Data import CommonDataFetch
from Data.Query import WarehouseQueries

def fetch_warehouses_service(request):
    where_clause_list = []

    if request.warehouse_id:
        warehouse_id_filter = f"warehouse_id = {request.warehouse_id}"
        where_clause_list.append(warehouse_id_filter)

    if len(where_clause_list) > 1:
        where_clause = "WHERE " + " AND ".join(where_clause_list)
    elif len(where_clause_list) == 1:
        where_clause = "WHERE " + " ".join(where_clause_list)
    else:
        where_clause = ""

    query = WarehouseQueries.fetch_warehouses_query.format(whereclause=where_clause)
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    return output_dataframe

# def create_warehouse(procedure_inputs):
#     query = WarehouseQueries.create_warehouse_query.format(arguments = procedure_inputs)
#     CommonDataFetch.execute_query(query)

def fetch_table_schema(table_name):
    query = WarehouseQueries.fetch_table_schema.format(table_name=table_name)
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    return output_dataframe.to_dict('records')

def update_warehouse(procedure_inputs):
    CommonDataFetch.execute_procedures('update_warehouse', procedure_inputs)

def delete_warehouse(procedure_inputs):
    CommonDataFetch.execute_procedures('delete_warehouse',[procedure_inputs]) 

def create_warehouse(procedure_inputs):
    CommonDataFetch.execute_procedures('create_warehouse',procedure_inputs)

def check_warehouse_id(warehouse_id):
    function_arguments = warehouse_id
    query = WarehouseQueries.check_warehouse_id_function.format(arguments=function_arguments)
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    return output_dataframe.iloc[0, 0] == 1