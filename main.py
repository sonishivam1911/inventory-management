from Controller import AnalysisController,InventoryController,WarehouseController,SalesOrderController,PurchaseOrderController

function_mapping = {
        '1' : InventoryController.InventoryController,
        '2' : WarehouseController.WarehouseController,
        '3' : AnalysisController.AnalysisController,
        '4' : SalesOrderController.SalesOrderController,
        '5' : PurchaseOrderController.PurchaseOrderController
    }

"""
    Method to Execute each command based on function_mapping dict.
"""
def execute_command(selected_screen_number : str):
    function_mapping[selected_screen_number]()


"""
    Method to fetch the screen number and catch excetion
"""
def fetch_screen_number():
    try:
        print("Select preferred screen : ")
        print(" 1 : Inventory")
        print(" 2 : WareHouse")
        print(" 3 : Reports")
        print(" 4 : Sales Order")
        print(" 5 : Purchase Order")
        print(" 6 : Terminate")
        selected_screen_number = int(input("Please enter screen number : ").strip())
        return selected_screen_number
    except Exception as e:
            print(f"Error message : {e.message}")

            
if __name__ == '__main__':
    is_program_terminated = False
    while(not is_program_terminated):
        try:
            selected_screen_number = fetch_screen_number()
            if selected_screen_number not in [1,2,3,4,5,6]:
                print("You entered incorrect argument try again please")
            elif selected_screen_number == 6:
                is_program_terminated = True 
            else:
                execute_command(str(selected_screen_number))
        except Exception as e:
            print(f"Error message : {e.message}")
        finally:
            continue

    print("Program Terminated")

        
    