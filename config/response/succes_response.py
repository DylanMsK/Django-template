from dataclasses import dataclass
from typing import Optional, Union, Dict, List, Any


@dataclass
class SuccessResponse:
    code: str
    message: str
    data: Optional[Union[Dict[str, Any], List[Any]]]
