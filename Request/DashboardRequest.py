from pydantic import BaseModel


class OverallSalesModel(BaseModel):
    status: list[str] = ["PENDING","SHIPPED"] 