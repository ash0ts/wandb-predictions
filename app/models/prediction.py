from typing import Dict, Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: bool
