from typing_extensions import Annotated
from pydantic import BaseModel, Field


#===================================================================================================================================================
# parametros:
#===================================================================================================================================================
PARAMETROS_ID = Annotated[int, Field(ge = 0)]
PARAMETROS_NOMBRE = Annotated[str, Field(min_length = 3, max_length = 50, description = "Indica el nombre del producto")]
PARAMETROS_PRECIO = Annotated[float, Field(gt = 0, description = "Indica el precio del producto")]
PARAMETROS_DISPONIBLE = Annotated[bool, Field(description = "Indica si el producto esta disponible o no")]
#===================================================================================================================================================


#===================================================================================================================================================
# esquemas:
#===================================================================================================================================================
class ArticuloSchema(BaseModel):
    id: PARAMETROS_ID
    nombre: PARAMETROS_NOMBRE
    precio: PARAMETROS_PRECIO
    disponible: PARAMETROS_DISPONIBLE


class UpdateSchema(BaseModel):
    nombre: PARAMETROS_NOMBRE
    precio: PARAMETROS_PRECIO
    disponible: PARAMETROS_DISPONIBLE
#===================================================================================================================================================
