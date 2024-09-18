from Request.InventoryRequest import InventoryRequestModel
from Model.InventoryModel import (fetch_products_service,fetch_table_schema,create_inventory,
                                  check_product_id,update_price_service,fetch_brand_name,
                                  fetch_category_name,delete_product)
from Controller import Constants

"""
    Method to Execute each command for different operations performed for each product.
"""
def InventoryController():
    try:
        operation_mapping = {
            '1' : DisplayInventory,
            '2' : CreateInventory,
            '3' : UpdateInventoryPrice,
            '4' : DeleteProduct,
            '5' : BackController
        }
        # ask for required operations - fetch all products , filter products, fetch single inventory, update product, create product, delete product
        operation_list = ['Fetch Inventory','Create Inventory',
                        'Update Inventory','Delete Inventory','Back'] 
        is_operation_over = False
        while(not is_operation_over):
            count = 1
            for operation in operation_list:
                print(f"{count} : {operation}")
                count += 1

            input_operations = input("Please select above operations number : ")
            while int(input_operations) not in range(1,6):
                print("Value selected is incorrect please try again")
                input_operations = input("Please select above operations number : ")
            
            if input_operations == '5':
                is_operation_over = True
            else:
                operation_mapping[input_operations]()
    except Exception as e:
        print(f"Error message : {e}")
        return
        


"""
    Method to fetch product attributes.
"""
def DisplayInventory():
    try:
        display_type = {
            "1" : DisplayEntireInventory,
            "2" : DisplayIndividualInventory,
            "3" : DisplayFilteredInventory
        }

        count = 1
        for display_key in ["All","Indiviual","Filter"]:
            print(f"{count} : {display_key}")
            count += 1
        
        input_display_command = input("Please select display operation : \n")
        while int(input_display_command) not in range(1,4):
            print("Value selected is incorrect please try again")
            input_display_command = input("Please select display operation : \n")

        display_type[input_display_command]()
    
    except Exception as e:
        print(f"Error message : {e}")
        return

"""
    Method to fetch product attributes with no filters.
"""
def DisplayEntireInventory():
    try:
        input_request = InventoryRequestModel()
        output_df = fetch_products_service(input_request)

        for column in list(output_df.columns):
            print(column,end=" ")

        for index, row in output_df.iterrows():
            print('\n',row['product_id']," ",row['sku']," ",row['name']," ",
                row['price']," ",row['brand_name']," ",row['category_name'])
    except Exception as e:
        print(f"Error message : {e}")
        return
    
"""
    Method to fetch product attributes for each product."
"""        
def DisplayIndividualInventory():
    try:
        input_sku = input("Please enter SKU : \n")
        input_request = InventoryRequestModel(sku=input_sku)
        output_df = fetch_products_service(input_request)

        for column in list(output_df.columns):
            print(column,end=" ")

        for index, row in output_df.iterrows():
            print('\n',row['product_id']," ",row['sku']," ",row['name']," ",
                row['price']," ",row['brand_name']," ",row['category_name']) 
    except Exception as e:
        print(f"Error message : {e}")
        return

"""
    Method to fetch product attributes based on brand and category filters.
"""
def DisplayFilteredInventory():
    try:
        input_brand = input("Please enter brand : \n")
        input_category = input("Please enter category : \n")
        input_request = InventoryRequestModel(
            brand_name=input_brand,
            category_name=input_category
        )
        output_df = fetch_products_service(input_request)

        for column in list(output_df.columns):
            print(column,end=" ")

        for index, row in output_df.iterrows():
            print('\n',row['product_id']," ",row['sku']," ",row['name']," ",
                row['price']," ",row['brand_name']," ",row['category_name'])
    except Exception as e:
        print(f"Error message : {e}")
        return

"""
    Method to create products.
"""
def CreateInventory():
    try : 
        column_list = []
        for table in ['Product','ProductBrand','ProductCategory']:
            input_columns = fetch_table_schema(table)
            column_list.extend(input_columns)

        
        input_column_mapping = {}
        for column in column_list:
            if column["Extra"] not in ['auto_increment',
                                    'DEFAULT_GENERATED on update CURRENT_TIMESTAMP',
                                    'DEFAULT_GENERATED'] and column['Field'] not in ['product_category_id','product_brand_id']:
                
                input_column_mapping[column['Field']] = input(f"\n Please enter value for column {column['Field']} : ")

        argument_list = []
        for column_name in Constants.InventoryProcedureArgumentOrderList:
            argument_list.append(input_column_mapping[column_name])

        create_inventory(argument_list)
        print("\n Inventory created")
    except Exception as e:
        print(f"Error message : {e}")
        return

"""
    Method to update product price - caller method.
"""
def UpdateInventoryPrice():
    try:
        update_type = {
            "1" : UpdateIndividualPrice,
            "2" : UpdatePriceUsingFilter
        }

        count = 1
        for update_key in ["Individual","Filter"]:
            print(f"{count} : {update_key}")
            count += 1
        
        input_update_command = input("Please select update operation : \n")
        while input_update_command not in ["1","2"]:
            input_update_command = input("Select desired value : \n").strip()
        update_type[input_update_command]()
    except Exception as e:
        print(f"Error message : {e}")
        return

"""
    Method to update product price - for individual product.
"""
def UpdateIndividualPrice():
    try:
        input_product_id = fetch_product_id()
        update_percentage = fetch_user_price_percentage()
        update_price_service([input_product_id,update_percentage/100],"update_price_for_product")
        print("\n Inventory updated")
    except Exception as e:
        print(f"Error message : {e}")
        return

"""
    Method to input and validate user percentage value.
"""
def fetch_user_price_percentage():
    count = 1
    for update_key in ["Increase","Decrease"]:
        print(f"{count} : {update_key}")
        count += 1
    
    input_update_command = input("Select desired value : \n").strip()
    signed_bit_value = 1
    while input_update_command not in ["1","2"]:
        input_update_command = input("Select desired value : \n").strip()

    if input_update_command == "2":
        signed_bit_value *= -1

    input_price_value = input("Select desired value for price change in % : \n").strip()
    return float(input_price_value) * signed_bit_value 

"""
    Method to input and validate user product id.
"""
def fetch_product_id():
    input_product_id = input("Select input product id : \n").strip()
    while not check_product_id:
        input_product_id = input("Select input product id : \n").strip()

    return input_product_id

"""
    Method to input and validate brand.
"""
def fetch_brand_filter():
    input_brand_command = input("Please input brand name : \n").strip()
    while input_brand_command not in fetch_brand_name():
        input_brand_command = input("Please input brand name :  \n").strip()

    return input_brand_command

"""
    Method to input and validate category.
"""
def fetch_category_filter():
    input_category_command = input("Please input category name : \n").strip()
    while input_category_command not in fetch_category_name():
        input_category_command = input("Please input category name : \n").strip()

    return input_category_command

def fetch_filter_value():
    filter_type = {
        "1" : fetch_brand_filter,
        "2" : fetch_category_filter
    }

    count = 1
    for update_key in ["Brand","Category"]:
        print(f"{count} : {update_key}")
        count += 1
    
    input_update_command = input("Select desired value : \n").strip()
    while input_update_command not in ["1","2"]:
        input_update_command = input("Select desired value : \n").strip()

    if input_update_command == "1":
        return "Brand",filter_type[input_update_command]()
    else:
        return "Category",filter_type[input_update_command]()



def UpdatePriceUsingFilter():
    try:
        procedure_type = {
            "Brand" : "update_price_for_product_based_on_brand",
            "Category" : "update_price_for_product_based_on_category"
        }
        update_percentage = fetch_user_price_percentage()
        filter_type,filter_value = fetch_filter_value()
        update_price_service([filter_value,update_percentage/100],procedure_type[filter_type])
        print("\n Inventory updated")
    except Exception as e:
        print(f"Error message : {e}")
        return

"""
    Method to delete product.
"""
def DeleteProduct():
    try:
        input_product_id = fetch_product_id()
        delete_product(int(input_product_id))
        print(f"\n Product deleted for {input_product_id}")
    except Exception as e:
        print(f"Error message : {e}")
        return


def BackController():
    return