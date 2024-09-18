fetch_sales_order = """
select sales_order_id,order_date,expected_delivery_date,status,sum(quantity) as total_quantity,sum(unit_price) as total_price
from SalesOrder as so join SalesOrderDetail as sod 
on so.SO_id = sod.sales_order_id
{whereclause}
group by 1,2,3,4;
"""

check_quantity_query= """
select check_warehouse_product_quantity({function_arguments}) as is_sufficient_quantity
"""

fetch_customer_id_count = """
select fetch_customer_count({function_arguments}) as count 
"""


fetch_order_id_count = """
select fetch_order_count({function_arguments}) as count 
"""

update_sales_order = """
update SalesOrder set {update_column} where SO_id = {order_id}
"""


fetch_last_insert_id = """
select max({pk}) as id from {table_name} ;
"""

fetch_sales_order_details = """
select distinct s.warehouse_id as warehouse_id,sod.product_id as product_id from SalesOrderDetail as sod
join Stock as s on sod.product_id = s.product_id;
"""

fetch_new_stock_quantity = """
select fetch_stock_quantity({function_arguments}) as quantity 
"""

update_sales_order_details = """
update SalesOrderDetail set {update_column} {whereclause}
"""

update_stock_quantity = """
update SalesOrder set {update_column} where SO_id = {order_id}
"""