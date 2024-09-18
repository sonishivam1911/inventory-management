from typing import Optional
from pydantic import BaseModel

class WarehouseRequestModel(BaseModel):
    warehouse_id: Optional[int]
