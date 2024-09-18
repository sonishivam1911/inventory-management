fetch_stock_report = """
call TotalStockQuantityProduct()
"""

fetch_purchase_order_report = """
call PurchaseOrdersByVendorWithAmount({arguments})
"""

fetch_low_quantity_report = """
call LowStockReport({arguments})
"""

fetch_get_total_stock_quantity_query = """
call GetTotalStockQuantity({arguments})
"""

fetch_get_purchases_by_vendor_query = """
call GetPurchasesByVendor({arguments})
"""