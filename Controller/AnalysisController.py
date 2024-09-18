import datetime
from Request.WarehouseRequest import WarehouseRequestModel
from Request.InventoryRequest import InventoryRequestModel
from Model.AnalysisModel import (fetch_stock_report_service,fetch_purchase_order_service,
                                 fetch_low_stock_report,fetch_get_total_stock_quantity,
                                 fetch_get_purchases_by_vendor)
from Model.WarehouseModel import fetch_warehouses_service
from Model.InventoryModel import fetch_products_service
from Controller import Constants

"""
    Method to Execute each command for different types of reports.
"""
def AnalysisController():
    try:
        operation_mapping = {
            '1' : StockReport,
            '2' : PurchaseOrderReport,
            '3' : LowQuantityStockReport,
            '4' : TotalStockQuanityReport,
            '5' : PurchasesByVendorReport,
        }
        # ask for required operations - fetch all products , filter products, fetch single inventory, update product, create product, delete product
        operation_list = ['Stock Report','Purchase Order Report',
                        'Low Quantity Stock Report','Total Stock Quanity Report','Purchases By Vendor Report','Back'] 
        is_operation_over = False
        while(not is_operation_over):
            count = 1
            for operation in operation_list:
                print(f"{count} : {operation}")
                count += 1

            input_operations = input("Please select above operations number : ")
            while int(input_operations) not in range(1,7):
                print("Value selected is incorrect please try again")
                input_operations = input("Please select above operations number : ")
            
            if input_operations == '6':
                is_operation_over = True
            else:
                operation_mapping[input_operations]()
    except Exception as e:
        print(f"Error message : {e}")
        return



"""
    Method to fetch stock report.
"""
def StockReport():
    try:
        output_df = fetch_stock_report_service()
        if len(output_df) == 0:
            print("No rows fetched")
        else:
            print(output_df)
    except Exception as e:
        print(f"Error message : {e}")
        return


def check_date(input_date):
    try:
        date_format = '%Y-%m-%d'
        dateObject = datetime.datetime.strptime(input_date, date_format)  
        return True
    except ValueError:
        return False
    
def check_threshold(input_threshold):
    try:
        check_value = int(input_threshold)
        return True
    except ValueError:
        return False

"""
    Method to fetch purchase order report.
"""
def PurchaseOrderReport():
    try:
        
        input_start_date, input_end_date = fetch_start_end_date_helper()
        output_df = fetch_purchase_order_service(f"'{input_start_date}','{input_end_date}'")
        if len(output_df) == 0:
            print("No rows fetched")
        else:
            print(output_df)
    except Exception as e:
        print(f"Error message : {e}")
        return

def fetch_start_end_date_helper():
    input_start_date = input("Please input the start date : ")
    while not check_date(input_start_date):
        print("Value selected is incorrect please try again")
        input_start_date = input("Please input the start date : ")


    input_end_date = input("Please input the end date : ")
    while not check_date(input_end_date):
        print("Value selected is incorrect please try again")
        input_end_date = input("Please input the end date : ")
    return input_start_date,input_end_date

"""
    Method to fetch low quantity stock report.
"""
def LowQuantityStockReport():
    try:
        input_warehouse_id = input("Please input the warehouse id : ")
        warehouse_info_df = fetch_warehouses_service(WarehouseRequestModel(warehouse_id=input_warehouse_id))
        while int(input_warehouse_id) not in list(warehouse_info_df['warehouse_id']):
            print("Value selected is incorrect please try again")
            input_warehouse_id = input("Please input the warehouse id : ")


        input_threshold = input("Please threshold for quantity : ")
        while not check_threshold(input_threshold):
            print("Value selected is incorrect please try again")
            input_threshold = input("Please threshold for quantity : ")

        output_df = fetch_low_stock_report(f"{input_warehouse_id},{input_threshold}")
        if len(output_df) == 0:
            print("No rows fetched")
        else:
            print(output_df)
    except Exception as e:
        print(f"Error message : {e}")
        return

"""
    Method to fetch total stock quantity report.
"""
def TotalStockQuanityReport():
    try:
        input_product_id = input("Please input the product id : ")
        product_info_df = fetch_products_service(InventoryRequestModel())
        while int(input_product_id) not in list(product_info_df['product_id']):
            print("Value selected is incorrect please try again")
            input_product_id = input("Please input the product id : ")

        output_df = fetch_get_total_stock_quantity(f"{input_product_id}")
        if len(output_df) == 0:
            print("No rows fetched")
        else:
            print(output_df)
    except Exception as e:
        print(f"Error message : {e}")
        return

"""
    Method to fetch purchases by vendor.
"""
def PurchasesByVendorReport():
    try:
        input_start_date, input_end_date = fetch_start_end_date_helper()
        output_df = fetch_get_purchases_by_vendor(f"'{input_start_date}','{input_end_date}'")
        if len(output_df) == 0:
            print("No rows fetched")
        else:
            print(output_df)
    except Exception as e:
        print(f"Error message : {e}")
        return
