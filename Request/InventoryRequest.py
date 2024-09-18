from typing import Optional
from pydantic import BaseModel


class InventoryRequestModel(BaseModel):
    brand_name : Optional[str]
    category_name : Optional[str]
    sku : Optional[str]