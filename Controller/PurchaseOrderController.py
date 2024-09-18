from Model.WarehouseModel import check_warehouse_id
from Request.PurchaseOrderRequest import OrderRequestModel
from Model.PurchaseOrderModel import check_purchase_order_id, check_purchase_order_process_id, delete_purchase_order, fetch_order_service,check_vendor_id_input,create_purchase_order,create_purchase_order_details, fetch_purchase_order_detail_service, process_purchase_order, update_purchase_order_detail
from Controller import Constants


def PurchaseOrderController():
    try:    
        operation_mapping = {
            '1' : DisplayPurchaseOrders,
            '2' : CreatePurchaseOrder,
            '3' : DeletePurchaseOrder,
            '4' : UpdatePurchaseOrder,
            '5' : ProcessPurchaseOrder
            }
        # ask for required operations - fetch all products , filter products, fetch single inventory, update product, create product, delete product
        operation_list = ['Display Purchase Orders','Create Purchase Order','Delete Purchase Order','Update Purchase Order','Process Purchase Order', 'Back'] 
        while(True):
            count = 1
            for operation in operation_list:
                print(f"{count} : {operation}")
                count += 1

            input_operations = input("Please select above operations number : ")
            while int(input_operations) not in range(1,7):
                print("Value selected is incorrect please try again")
                input_operations = input("Please select above operations number : ")
                
            if input_operations == '6':
                return
            else:
                operation_mapping[input_operations]()   
    except Exception as e:
        print(f"Error message : {e}")
        return            



def DisplayPurchaseOrders():
    try:
        display_type = {
            "1": DisplayAllPurchaseOrders,
            "2": DisplayIndividualPurchaseInventory,
            "3": DisplayFilteredPurchaseInventory
        }

        count = 1
        for display_key in ["All", "Individual", "Filter"]:
            print(f"{count} : {display_key}")
            count += 1

        input_display_command = input("Please select display operation: \n")
        while input_display_command not in display_type.keys():
            print("Value selected is incorrect, please try again.")
            input_display_command = input("Please select display operation: \n")

        display_type[input_display_command]()
    except Exception as e:
        print(f"Error message: {e}")
        return



def DisplayAllPurchaseOrders():
    try:
        input_request = OrderRequestModel()
        output_df = fetch_order_service(input_request)

        for column in list(output_df.columns):
            print(column, end=" ")

        for index, row in output_df.iterrows():
            print('\n', row['purchase_order_id'], " ", row['order_date'], " ",
                  row['expected_delivery_date'], " ", row['status'], " ", row['total_quantity']
                  , " ", row['total_price'])
    except Exception as e:
        print(f"Error message: {e}")
        return

def DisplayIndividualPurchaseInventory():
    try:
        input_id = input("Please enter order id : \n").strip()
        input_request = {'purchase_order_id': int(input_id)}
        output_df = fetch_order_service(input_request)

        for column in list(output_df.columns):
            print(column, end=" ")

        for index, row in output_df.iterrows():
            print('\n', row['purchase_order_id'], " ", row['order_date'], " ",
                  row['expected_delivery_date'], " ", row['status'], " ", row['total_quantity']
                  , " ", row['total_price'])
    except Exception as e:
        print(f"Error message : {e}")


def DisplayFilteredPurchaseInventory():
    try:
        input_status = input("Please enter status (PENDING,SHIPPED,CANCELLED) : \n")
        input_order_date = input("Please enter order_date : \n")
        input_expected_delivery_date = input("Please enter expected_delivery_date : \n")
        input_request = OrderRequestModel(
            status=input_status if len(input_status) > 0 else None,
            expected_delivery_date=input_expected_delivery_date if len(input_expected_delivery_date) > 0 else None,
            order_date=input_order_date if len(input_order_date) > 0 else None
        )

        output_df = fetch_order_service(input_request)

        for column in list(output_df.columns):
            print(column, end=" ")

        for index, row in output_df.iterrows():
            print('\n', row['purchase_order_id'], " ", row['order_date'], " ",
                  row['expected_delivery_date'], " ", row['status'], " ", row['total_quantity']
                  , " ", row['total_price'])
    except Exception as e:
        print(f"Error message : {e}")


def CreatePurchaseOrder():    
    # take input for customer id and check customer id else ask for another input
    input_vendor_id = input("Please enter the vendor id : ").strip()
    while(check_vendor_id_input(input_vendor_id)==0):
        input_vendor_id = input("Please enter the customer id : ").strip()

    purchase_order_id = create_purchase_order(int(input_vendor_id))
    add_more_products = "Yes"
    while add_more_products.lower() != 'no':
        input_column_mapping = {}
        for column in ['warehouse_id','product_id','quantity']:    
            input_column_mapping[column] = input(f"\n Please enter value for column {column} : ").strip()
            
      #  while(check_quantity(",".join(list(input_column_mapping.values()))) == 0):
      #     input_column_mapping[column] = input(f"\n Please enter value for column {column} : ").strip()
            
        input_column_mapping['purchase_order_id'] = purchase_order_id
        create_purchase_order_details(list(input_column_mapping.values()))
        add_more_products = input("\n Add more products ? Yes : No  ").strip()
        while(add_more_products not in ["Yes","No"]):
            add_more_products = input("\n Add more products ? Yes : No  ").strip()


    print("\n Purchase Order created ")
    return

def DeletePurchaseOrder():
    try:
        purchase_order_id = input("Please enter the Purchase Order ID to delete: ").strip()

        if not check_purchase_order_id(purchase_order_id):
            print("Purchase Order ID does not exist. Please try again.")
        else:
            delete_purchase_order(purchase_order_id)
            print("Purchase Order deleted.")
    except Exception as e:
        print(f"Error message: {e}")

def UpdatePurchaseOrder():
    try:
        PO_id = input("Please enter the Purchase Order ID to update: ").strip()

        if not check_purchase_order_id(PO_id):
            print("Purchase Order ID does not exist. Please try again.")
        else :    
            # Display the purchase order details for the given purchase order id
            input_request = {'purchase_order_id': int(PO_id)}
            output_df = fetch_purchase_order_detail_service(input_request)

            print("Purchase Order Detail Information:")
            for column in list(output_df.columns):
                print(column, end=" ")

            for index, row in output_df.iterrows():
                print('\n', row['PO_det_id'], " ", row['purchase_order_id'], " ",
                  row['product_id'], " ", row['quantity'], " ", row['price'])

            # Ask for the purchase order detail id to update
            PO_det_id = input("\nPlease enter the Purchase Order Detail ID to update: ").strip()

            update_fields = []
            print("Select the fields you want to update or 'all' to update all fields:")
            print("1: Product ID")
            print("2: Quantity")
            print("3: Price")
            print("all: Update all fields")
            fields = input().split(',')

            product_id = None
            quantity = None
            price = None

            if 'all' in fields:
                product_id = input("Enter the new Product ID: ").strip()
                quantity = input("Enter the new Quantity: ").strip()
                price = input("Enter the new Price: ").strip()
            else:
                if '1' in fields:
                    product_id = input("Enter the new Product ID: ").strip()
                if '2' in fields:
                    quantity = input("Enter the new Quantity: ").strip()
                if '3' in fields:
                    price = input("Enter the new Price: ").strip()

            update_purchase_order_detail([PO_id, PO_det_id, product_id, quantity, price])
            print("Purchase Order Detail updated.")
    except Exception as e:
        print(f"Error message : {e}")


def ProcessPurchaseOrder():
    try:
        purchase_order_id = input("Please enter the purchase order id to process: ").strip()
        warehouse_id = input("Please enter the warehouse id where Stock will be added: ").strip()

        if not check_purchase_order_process_id(purchase_order_id):
            print("Purchase Order ID does not exist or is already processed. Please try again.")
        elif not check_warehouse_id(warehouse_id):
            print("Warehouse ID does not exist. Please try again.")
        else:
            process_purchase_order(int(purchase_order_id), int(warehouse_id))
            print("\n Purchase Order processed")
    except Exception as e:
        print(f"Error message: {e}")

