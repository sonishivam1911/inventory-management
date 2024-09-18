from Data import CommonDataFetch
from Data.Query import AnalysisQueries
def fetch_reports_data(procedure_name,procedure_input):
    return CommonDataFetch.execute_procedures(procedure_name,procedure_input,True)


def fetch_stock_report_service():
    return CommonDataFetch.execute_query_pandas(AnalysisQueries.fetch_stock_report)

def fetch_purchase_order_service(arguments):
    query = AnalysisQueries.fetch_purchase_order_report.format(arguments=arguments)
    return CommonDataFetch.execute_query_pandas(query)

def fetch_low_stock_report(arguments):
    query = AnalysisQueries.fetch_low_quantity_report.format(arguments=arguments)
    return CommonDataFetch.execute_query_pandas(query)

def fetch_get_total_stock_quantity(arguments):
    query = AnalysisQueries.fetch_get_total_stock_quantity_query.format(arguments=arguments)
    return CommonDataFetch.execute_query_pandas(query)

def fetch_get_purchases_by_vendor(arguments):
    query = AnalysisQueries.fetch_get_purchases_by_vendor_query.format(arguments=arguments)
    return CommonDataFetch.execute_query_pandas(query)