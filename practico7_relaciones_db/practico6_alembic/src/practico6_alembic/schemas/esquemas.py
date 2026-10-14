from sqlmodel import Field
from typing import Annotated


PARAMETROS_ID = Annotated[int, Field(ge = 0)]
PARAMETROS_NOMBRE = Annotated[str, Field(min_length = 3, max_length = 50)]
PARAMETROS_PRECIO = Annotated[float, Field(gt = 0)]
PARAMETROS_DISPONIBLE = Annotated[bool, Field(default = True)]