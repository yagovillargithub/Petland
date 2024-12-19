class Venta:
    def __init__(self, id=None, fecha=None, id_articulo=None, articulos=None, metodo_pago=None, total=None, descuento=0):
        self.id = id
        self.fecha = fecha
        self.id_articulo = id_articulo
        self.articulos = articulos# Lista o diccionario con los detalles de los artículos
        self.metodo_pago = metodo_pago
        self.total = total
        self.descuento = descuento


