fetch_products_query = """
select product_id,sku,name,price,brand_name,category_name
from Product as p join ProductBrand as pb 
on p.product_brand_id = pb.brand_id
join ProductCategory as pc on p.product_category_id = pc.category_id
{whereclause}
"""

fetch_brands_query = """
select distinct brand_name
from ProductBrand
"""


fetch_category_query = """
select distinct category_name
from ProductCategory
"""

fetch_table_schema = """
SHOW COLUMNS FROM {table_name};
"""

create_inventory_procedure = """
call create_inventory({arguments})
"""

check_product_id_function = """
select create_inventory({arguments})
"""