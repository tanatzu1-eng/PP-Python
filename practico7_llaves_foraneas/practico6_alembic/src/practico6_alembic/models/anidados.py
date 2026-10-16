# segun la IA, si quiero un archivo por cada tabla, necesito un anidados.py, porque sino voy a hacer un bucle de importes entre ambos archivos
from .articulo import ArticuloPublic
from .proveedor import ProveedorPublic


# Articulo
class ArticuloNested(ArticuloPublic):
    proveedores: ProveedorPublic | None = None


class ProveedorNested(ProveedorPublic):
    proveedores: list[ArticuloPublic] | None = []