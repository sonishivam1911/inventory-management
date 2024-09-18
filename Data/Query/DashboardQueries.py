fetch_overall_sales_query = """
select SO_id,c.name,expected_delivery_date,status,quantity,unit_price
from SalesOrder as so join SalesOrderDetail as sod
on so.SO_id = sod.sales_order_id
join Customer as c on so.customer_id = c.customer_id
{whereclause}
"""