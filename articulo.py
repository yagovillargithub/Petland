import pyodbc

class Articulo:
    def __init__(self, id=None, nombre=None, descripcion=None, precio=None, stock=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

    # Crear un artículo
    def crear(self):
        conn = Articulo.conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Articulo (nombre, descripcion, precio, stock) 
            VALUES (?, ?, ?, ?)
        """, (self.nombre, self.descripcion, self.precio, self.stock))
        conn.commit()
        conn.close()
        print("Artículo creado exitosamente.")

    # Leer todos los artículos
    @staticmethod
    def leer_todos():
        conn = Articulo.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Articulo")
        articulos = cursor.fetchall()
        conn.close()
        return articulos

    # Actualizar un artículo
    def actualizar(self):
        conn = Articulo.conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Articulo 
            SET nombre = ?, descripcion = ?, precio = ?, stock = ? 
            WHERE id = ?
        """, (self.nombre, self.descripcion, self.precio, self.stock, self.id))
        conn.commit()
        conn.close()
        print("Artículo actualizado exitosamente.")

    # Eliminar un artículo
    @staticmethod
    def eliminar(id):
        conn = Articulo.conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Articulo WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        print("Artículo eliminado exitosamente.")

    # Realizar venta de un artículo
    def realizar_venta(self, cantidad):
        # Verificar si hay suficiente stock
        if self.stock >= cantidad:
            conn = Articulo.conectar_db()
            cursor = conn.cursor()

            # Reducir stock
            nuevo_stock = self.stock - cantidad
            cursor.execute("""
                UPDATE Articulo
                SET stock = ?
                WHERE id = ?
            """, (nuevo_stock, self.id))

            # Insertar la venta en la tabla 'Venta'
            cursor.execute("""
                INSERT INTO Venta (id_articulo, cantidad)
                VALUES (?, ?)
            """, (self.id, cantidad))

            conn.commit()
            conn.close()

            print(f"Venta realizada. {cantidad} unidades vendidas. Stock restante: {nuevo_stock}")
        else:
            print("No hay suficiente stock para realizar la venta.")

