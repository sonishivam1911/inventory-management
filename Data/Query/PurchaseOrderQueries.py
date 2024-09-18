fetch_purchase_order = """
select purchase_order_id,order_date,expected_delivery_date,status,sum(quantity) as total_quantity,sum(price) as total_price
from PurchaseOrder as po join PurchaseOrderDetail as pod 
on po.PO_id = pod.purchase_order_id
{whereclause}
group by 1,2,3,4;
"""

fetch_vendor_id_count = """
select fetch_vendor_count({function_arguments}) as count 
"""

fetch_last_insert_id = """
select max({pk}) as id from {table_name} ;
"""

fetch_purchase_order_detail = """
select PO_det_id, purchase_order_id, product_id, quantity, price
from PurchaseOrderDetail
{whereclause};
"""

count_purchase_order_by_id = """
SELECT COUNT(*) as count
FROM PurchaseOrder
WHERE PO_id = {purchase_order_id};
"""

count_purchase_order_process_by_id = """
SELECT COUNT(*) as count
FROM PurchaseOrder
WHERE PO_id = {purchase_order_id} AND status = 'PENDING';
"""
