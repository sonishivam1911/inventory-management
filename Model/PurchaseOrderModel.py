from Data import CommonDataFetch
from Data.Query import PurchaseOrderQueries

def create_where_clause(request):

    request = dict(request)
    request_list = []
    for key in request.keys():
        if request[key]:
            request_list.append(f"{key} = '{request[key]}'")
    
    if len(request_list) == 0:
        return ""

    if len(request_list) > 1:
        join_operator = " and "
    else:
        join_operator = " "

    return "where " + join_operator.join(request_list) 


def fetch_order_service(request):

    where_clause = create_where_clause(request)
    query = PurchaseOrderQueries.fetch_purchase_order.format(whereclause=where_clause)
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    return output_dataframe

# def fetch_table_schema(table_name):
#     query = InventoryQueries.fetch_table_schema.format(table_name=table_name)
#     output_dataframe = CommonDataFetch.execute_query_pandas(query)
#     return output_dataframe.to_dict('records')

def create_purchase_order(procedure_inputs):
    CommonDataFetch.execute_procedures('create_purchase_order',[procedure_inputs])
    query = PurchaseOrderQueries.fetch_last_insert_id.format(
        table_name = "PurchaseOrder",
        pk="PO_id"
    )
    purchase_order_id_df = CommonDataFetch.execute_query_pandas(query)
    return int(purchase_order_id_df["id"][0])

def create_purchase_order_details(procedure_inputs):
    CommonDataFetch.execute_procedures('create_purchase_order_details',procedure_inputs)

def check_vendor_id_input(function_inputs):
    query = PurchaseOrderQueries.fetch_vendor_id_count.format(function_arguments=function_inputs)
    vendor_df = CommonDataFetch.execute_query_pandas(query)
    return vendor_df["count"][0]

def delete_purchase_order(purchase_order_id):
    CommonDataFetch.execute_procedures('delete_purchase_order', [purchase_order_id])

def update_purchase_order_detail(procedure_inputs):
    CommonDataFetch.execute_procedures('update_purchase_order_detail', procedure_inputs)

def fetch_purchase_order_detail_service(request):
    where_clause = create_where_clause(request)
    query = PurchaseOrderQueries.fetch_purchase_order_detail.format(whereclause=where_clause)
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    return output_dataframe

def process_purchase_order(purchase_order_id, warehouse_id):
    CommonDataFetch.execute_procedures('process_purchase_order', [purchase_order_id, warehouse_id])

def check_purchase_order_id(purchase_order_id):
    query = PurchaseOrderQueries.count_purchase_order_by_id.format(purchase_order_id=purchase_order_id)
    count_df = CommonDataFetch.execute_query_pandas(query)
    return count_df["count"][0] > 0

def check_purchase_order_process_id(purchase_order_id):
    query = PurchaseOrderQueries.count_purchase_order_process_by_id.format(purchase_order_id=purchase_order_id)
    count_df = CommonDataFetch.execute_query_pandas(query)
    return count_df["count"][0] > 0
