fetch_warehouses_query = """
SELECT *
FROM Warehouse
{whereclause}
"""

create_warehouse_query = """
call create_warehouse({arguments})
"""

update_warehouse_query = """
"""

delete_warehouse_query = """
"""

fetch_table_schema = """
SHOW COLUMNS FROM {table_name};
"""

fetch_stock_quantity = """
call GetTotalStockQuantity({arguments})"""

check_warehouse_id_function = """
select check_warehouse_exists({arguments})
"""