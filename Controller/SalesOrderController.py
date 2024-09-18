from Request.SalesOrderRequest import OrderRequestModel
from Model.SalesOrderModel import (check_deleteorder_id, fetch_order_service,check_quantity,check_customer_id_input,
                                   create_sales_order,create_sales_order_details,check_order_id,
                                   update_sales_order,fetch_warehouse_prouduct_service,
                                   update_sales_order_details,delete_sales_order)


def SalesOrderController():
    try:
        operation_mapping = {
            '1' : DisplayOrders,
            '2' : CreateSalesOrder,
            '3' : SelectUpdateValues,
            '4' : DeleteSaleOrder
        }
        # ask for required operations - fetch all products , filter products, fetch single inventory, update product, create product, delete product
        operation_list = ['Display Orders','Create Order','Update Order','Delete Order','Back'] 
        while True:
            count = 1
            for operation in operation_list:
                print(f"{count} : {operation}")
                count += 1

            input_operations = input("Please select above operations number : ")
            while int(input_operations) not in range(1,6):
                print("Value selected is incorrect please try again")
                input_operations = input("Please select above operations number : ")
            
            if input_operations == '5':
                return
            else:
                operation_mapping[input_operations]()
        
    except Exception as e:
        print(f"Error message : {e}")
        return


def DisplayOrders():
    try:
        display_type = {
            "1" : DisplayAllOrders,
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


def DisplayAllOrders():
    try:
        input_request = OrderRequestModel()
        output_df = fetch_order_service(input_request)

        for column in list(output_df.columns):
            print(column,end=" ")

        for index, row in output_df.iterrows():
            print('\n',row['sales_order_id']," ",row['order_date']," ",
                row['expected_delivery_date']," ",row['status']," ",row['total_quantity']
                ," ",row['total_price'])

    except Exception as e:
        print(f"Error message : {e}")
        return
        
def DisplayIndividualInventory():
    try:
        input_id = input("Please enter order id : \n").strip()
        input_request = {'sales_order_id' : int(input_id)}
        output_df = fetch_order_service(input_request)

        for column in list(output_df.columns):
            print(column,end=" ")

        for index, row in output_df.iterrows():
            print('\n',row['sales_order_id']," ",row['order_date']," ",
                row['expected_delivery_date']," ",row['status']," ",row['total_quantity']
                ," ",row['total_price'])
            
    except Exception as e:
        print(f"Error message : {e}")
        return
        


def DisplayFilteredInventory():
    try:
        input_status = input("Please enter status (PENDING,SHIPPED,CANCELLED) : \n")
        input_order_date = input("Please enter order_date : \n")
        input_expected_delivery_date= input("Please enter expected_delivery_date : \n")
        input_request = OrderRequestModel(
            status=input_status if len(input_status)>0 else None,
            expected_delivery_date=input_expected_delivery_date if len(input_expected_delivery_date)>0 else None,
            order_date=input_order_date if len(input_order_date)>0 else None
        )

        output_df = fetch_order_service(input_request)

        for column in list(output_df.columns):
            print(column,end=" ")

        for index, row in output_df.iterrows():
            print('\n',row['sales_order_id']," ",row['order_date']," ",
                row['expected_delivery_date']," ",row['status']," ",row['total_quantity']
                ," ",row['total_price'])
            
    except Exception as e:
        print(f"Error message : {e}")
        return
        

def CreateSalesOrder():    
    # take input for customer id and check customer id else ask for another input
    try:
        input_customer_id = fetch_customer_id_helper()
        sales_order_id = create_sales_order(int(input_customer_id))
        add_more_procducts = "Yes"
        while(add_more_procducts != 'No'):
            input_column_mapping = fetch_sales_order_details(sales_order_id)
            input_column_mapping['sales_order_id'] = sales_order_id
            create_sales_order_details(list(input_column_mapping.values()))
            add_more_products = input("\n Add more products ? Yes : No  ").strip()
            while(add_more_products not in ["Yes","No"]):
                add_more_products = input("\n Add more products ? Yes : No  ").strip()
        print("\n Sales Order created")

    except Exception as e:
        print(f"Error message : {e}")
        return


def fetch_sales_order_details(is_update : bool = False):
    input_column_mapping = {}
    sales_order_df = fetch_warehouse_prouduct_service()
    while(True):
        for column in ['warehouse_id','product_id','quantity']:    
            input_column_mapping[column] = input(f"\n Please enter value for column {column} : ").strip()

        if is_update and int(input_column_mapping["warehouse_id"]) not in list(sales_order_df["warehouse_id"]) or int(input_column_mapping["product_id"]) not in list(sales_order_df["product_id"]): 
            continue
        else:
            break

    while(check_quantity(",".join(list(input_column_mapping.values()))) == 0):
        input_column_mapping[column] = input(f"\n Please enter value for column {column} : ").strip()

    return input_column_mapping

def fetch_customer_id_helper():
    input_customer_id = input("Please enter the customer id : ").strip()
    while(check_customer_id_input(input_customer_id)==0):
        input_customer_id = input("Please enter the customer id : ").strip()
    return input_customer_id

def SelectUpdateValues():
    try:
        update_type = {
            "1" : UpdateSalesOrder,
            "2" : UpdateSalesOrderDetails,
        }

        while(True):
            count = 1
            for display_key in ['Update Sales Order','Update Sales Order Details']:
                print(f"{count} : {display_key}")
                count += 1
            
            input_display_command = input("Please select update operation : \n").strip()
            while int(input_display_command) not in range(1,4):
                print("Value selected is incorrect please try again")
                input_display_command = input("Please select update operation : \n").strip()

            if input_display_command in update_type.keys():
                update_type[input_display_command]()
                return
    
    except Exception as e:
        print(f"Error message : {e}")
        return
    


def UpdateSalesOrder():
    try:
        input_order_id = fetch_order_id()
        input_status = input("Please enter the status (PENDING,SHIPPED,CANCELLED) : ").strip()
        input_expected_delivery_date = input("Please enter the expected delivery date (use /) : ").strip()
        update_sales_order({
            'status' : input_status,
            'expected_delivery_date' : input_expected_delivery_date
        },input_order_id)
        print("\n Sales Order Updated")

    except Exception as e:
        print(f"Error message : {e}")
        return

def fetch_order_id():
    input_order_id = input("Please enter the order id : ").strip()
    while(check_order_id(input_order_id)==0):
        input_order_id = input("Please enter the order id : ").strip()

    return input_order_id

def fetch_order_id_delete():
    input_order_id = input("Please enter the order id to delete: ").strip()
    while(check_deleteorder_id(input_order_id)==0):
        input_order_id = input("Please enter the order id : ").strip()
    return input_order_id


def UpdateSalesOrderDetails():
    try:
        input_order_id = fetch_order_id()
        input_column_mapping = fetch_sales_order_details(True)
        input_column_mapping['sales_order_id'] = input_order_id
        update_sales_order_details(input_column_mapping)
        print(f"\n Sales Order Updated for {input_order_id}")

    except Exception as e:
        print(f"Error message : {e}")

def DeleteSaleOrder():
    try:
        input_order_id = fetch_order_id_delete()
        delete_sales_order(int(input_order_id))
        print(f"\n Sales Order Deleted for {input_order_id}")
    except Exception as e:
        print(f"Error message : {e}")
        return





    