from Data import CommonDataFetch
from Data.Query import SalesOrderQueries

def create_where_clause(request):

    request = dict(request) if not isinstance(request,dict) else request
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
    query = SalesOrderQueries.fetch_sales_order.format(whereclause=where_clause)
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    return output_dataframe


def create_sales_order(procedure_inputs):
    CommonDataFetch.execute_procedures('create_order',[procedure_inputs])
    query = SalesOrderQueries.fetch_last_insert_id.format(
        table_name = "SalesOrder",
        pk="SO_id"
    )
    sales_order_id_df = CommonDataFetch.execute_query_pandas(query)
    return int(sales_order_id_df["id"][0])

def create_sales_order_details(procedure_inputs):
    CommonDataFetch.execute_procedures('create_order_details',procedure_inputs)

def check_quantity(procedure_inputs):
    query = SalesOrderQueries.check_quantity_query.format(function_arguments=procedure_inputs)
    check_quantity_df = CommonDataFetch.execute_query_pandas(query)
    return check_quantity_df["is_sufficient_quantity"][0]

def check_customer_id_input(function_inputs):
    query = SalesOrderQueries.fetch_customer_id_count.format(function_arguments=function_inputs)
    customer_df = CommonDataFetch.execute_query_pandas(query)
    return customer_df["count"][0]


def check_order_id(function_request):
    query = SalesOrderQueries.fetch_customer_id_count.format(function_arguments=function_request)
    customer_df = CommonDataFetch.execute_query_pandas(query)
    return customer_df["count"][0]

def check_deleteorder_id(function_request):
    query = SalesOrderQueries.fetch_order_id_count.format(function_arguments=function_request)
    customer_df = CommonDataFetch.execute_query_pandas(query)
    return customer_df["count"][0]

def create_update_column(update_request):
    update_column_list = []
    for key in update_request.keys():
        if update_request[key]:
            update_column_list.append(f"{key} = '{update_request[key]}'")

    return ",".join(update_column_list)



def update_sales_order(update_request,order_id):
    update_column = create_update_column(update_request)
    query = SalesOrderQueries.update_sales_order.format(
        update_column=update_column,
        order_id = order_id
        )
    CommonDataFetch.execute_query(query,False)

def fetch_warehouse_prouduct_service():
    query = SalesOrderQueries.fetch_sales_order_details
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    return output_dataframe


def update_sales_order_details(update_request):
    # fetch the correct value for stock table 
    function_arguments = ",".join(list(update_request.values()))
    query = SalesOrderQueries.fetch_new_stock_quantity.format(function_arguments=function_arguments)
    output_dataframe = CommonDataFetch.execute_query_pandas(query)
    
    #update the sales order details
    sales_order_columns_for_update = create_update_column({
        'quantity' : update_request['quantity']
    })

    sales_order_where_clause = create_where_clause({
        'sales_order_id' : update_request['sales_order_id'],
        'product_id' : update_request['product_id']
        }
    )

    query = SalesOrderQueries.update_sales_order_details.format(
        update_column = sales_order_columns_for_update,
        whereclause = sales_order_where_clause
    )
    CommonDataFetch.execute_query(query=query,return_record=False)

    # update the stock table
    update_request['quantity'] = int(output_dataframe["quantity"][0])
    update_request.pop('sales_order_id')
    CommonDataFetch.execute_procedures('update_stock_table',list(update_request.values()))
    return

def delete_sales_order(sales_order_id):
    CommonDataFetch.execute_procedures('delete_sales_order',[sales_order_id])
    return 