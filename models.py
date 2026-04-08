from pydantic import BaseModel
from typing import Dict

class CleanAction(BaseModel):
    column: str
    operation: str  # Options: 'fillna_mean', 'drop_nulls', 'drop_column'

class Observation(BaseModel):
    total_rows: int
    missing_values: Dict[str, int]