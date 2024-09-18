from typing import Optional
from pydantic import BaseModel


class OrderRequestModel(BaseModel):
    vendor_id : Optional[str]
    order_date : Optional[str]
    expected_delivery_date : Optional[str]
    status : Optional[str]