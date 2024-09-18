from Request.WarehouseRequest import WarehouseRequestModel
from Model.WarehouseModel import check_warehouse_id, fetch_table_schema, fetch_warehouses_service, create_warehouse, update_warehouse, delete_warehouse
from Controller import Constants

def WarehouseController():
    while True:
        try:
            operation_mapping = {
                '1': DisplayWarehouses,
                '2': CreateWarehouse,
                '3': UpdateWarehouse,
                '4': DeleteWarehouse
            }

            operation_list = ['Display Warehouses', 'Create Warehouse',
                              'Update Warehouse', 'Delete Warehouse', 'Back']
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


def DisplayWarehouses():
    try:
        input_request = WarehouseRequestModel()
        output_df = fetch_warehouses_service(input_request)

        for column in list(output_df.columns):
            print(column, end=" ")

        for index, row in output_df.iterrows():
            print('\n', row['warehouse_id'], " ", row['warehouse_name'], " ",
                  row['street'], " ", row['city'], " ", row['state'], " ",
                  row['country'], " ", row['postal_code'], " ", row['phone'])

    except Exception as e:
        print(f"Error message : {e}")

def CreateWarehouse():
    
    column_list = []
    for table in ['Warehouse']:
        input_columns = fetch_table_schema(table)
        column_list.extend(input_columns)


    input_column_mapping = {}

    for column in column_list:
        if column["Field"] in Constants.WarehouseProcedureArgumentOrderList:
            input_column_mapping[column['Field']] = input(f"\n Please enter value for column {column['Field']} : ")

    argument_list = []
    for column_name in Constants.WarehouseProcedureArgumentOrderList:
        argument_list.append(input_column_mapping[column_name])

    create_warehouse(argument_list)
    print("\nWarehouse created")
    return


def UpdateWarehouse():
    warehouse_id = input("Please enter the Warehouse ID to update: ").strip()

    # Display the warehouse details for the given warehouse id
    input_request = WarehouseRequestModel()
    input_request.warehouse_id = int(warehouse_id)
    output_df = fetch_warehouses_service(input_request)

    print("Warehouse Information:")
    for column in list(output_df.columns):
        print(column, end=" ")

    for index, row in output_df.iterrows():
        print('\n', row['warehouse_id'], " ", row['warehouse_name'], " ",
              row['street'], " ", row['city'], " ", row['state'], " ",
              row['country'], " ", row['postal_code'], " ", row['phone'])

    # Ask for the fields to update
    update_fields = []
    print("Select the fields you want to update or 'all' to update all fields:")
    print("1: Warehouse Name")
    print("2: Street")
    print("3: City")
    print("4: State")
    print("5: Country")
    print("6: Postal Code")
    print("7: Phone")
    print("all: Update all fields")
    
    valid_inputs = ['1', '2', '3', '4', '5', '6', '7', 'all']
    fields = input().split(',')
    while not all(field in valid_inputs for field in fields):
        print("Invalid input, please try with valid input again.")
        fields = input().split(',')

    warehouse_name = None
    street = None
    city = None
    state = None
    country = None
    postal_code = None
    phone = None

    if 'all' in fields:
        warehouse_name = input("Enter the new Warehouse Name: ").strip()
        street = input("Enter the new Street: ").strip()
        city = input("Enter the new City: ").strip()
        state = input("Enter the new State: ").strip()
        country = input("Enter the new Country: ").strip()
        postal_code = input("Enter the new Postal Code: ").strip()
        phone = input("Enter the new Phone: ").strip()
    else:
        if '1' in fields:
            warehouse_name = input("Enter the new Warehouse Name: ").strip()
        if '2' in fields:
            street = input("Enter the new Street: ").strip()
        if '3' in fields:
            city = input("Enter the new City: ").strip()
        if '4' in fields:
            state = input("Enter the new State: ").strip()
        if '5' in fields:
            country = input("Enter the new Country: ").strip()
        if '6' in fields:
            postal_code = input("Enter the new Postal Code: ").strip()
        if '7' in fields:
            phone = input("Enter the new Phone: ").strip()

    update_warehouse([warehouse_id, warehouse_name, street, city, state, country, postal_code, phone])
    print("Warehouse updated.")
    return

def DeleteWarehouse():
    try:
        warehouse_id = fetch_warehouse_id()
        if warehouse_id is not None:
            delete_warehouse(warehouse_id)
            print(f"\n Warehouse Deleted : {warehouse_id}")
        else:
            print("Please try again with a valid warehouse ID.")
    except Exception as e:
        print(f"Error: {e}")
    return


def fetch_warehouse_id():
    input_warehouse_id = input("Select warehouse id to delete : \n").strip()
    if not check_warehouse_id(input_warehouse_id):
        print("Warehouse ID does not exist")
        return None
    return input_warehouse_id
