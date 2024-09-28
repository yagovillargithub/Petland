# Modulo que se encarga de las operaciones contra la base de datos

# IMPORTACIONES
import pyodbc
from articulo import Articulo

# INICIALIZACIONES
Articulo()

class ArticuloService:
    # FUNCIONES
    # Conexión a la base de datos
    def conectar_db(self):  # 'self' es necesario aquí
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=MARTALB\SQLEXPRESS;'
            'DATABASE=PetlandDb;'
            'UID=sa;'
            'PWD=1234'
        )
        return conn

    # Crear un artículo
    def crear(self, articuloACrear):  # Cambié 'Articulo' a 'articulo' (el parámetro)
        conn = self.conectar_db()  # Llamar al método de la misma clase
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Articulo (nombre, descripcion, precio, stock) 
            VALUES (?, ?, ?, ?)
        """, (articuloACrear.nombre, articuloACrear.descripcion, articuloACrear.precio, articuloACrear.stock))
        conn.commit()
        conn.close()
        print("Artículo creado exitosamente.")

    # Leer todos los artículos
    def leer_todos(self):
        conn = self.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Articulo")
        articulos = cursor.fetchall()
        conn.close()
        return articulos
    
    # Actualizar un artículo
    def actualizar(self, articuloAActualizar):
        conn = self.conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Articulo 
            SET nombre = ?, descripcion = ?, precio = ?, stock = ? 
            WHERE id = ?
        """, (articuloAActualizar.nombre, articuloAActualizar.descripcion, articuloAActualizar.precio, articuloAActualizar.stock, articuloAActualizar.id))
        conn.commit()
        conn.close()
        print("Artículo actualizado exitosamente.")
    
    # Eliminar un artículo
    def eliminar(self, idArticulo):
        conn = self.conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Articulo WHERE id = ?", (idArticulo,))
        conn.commit()
        conn.close()
        print("Artículo eliminado exitosamente.")
    
    # Realizar venta de un artículo
    def realizar_venta(self, cantidad, articulo):
        # Verificar si hay suficiente stock
        if articulo.stock >= cantidad:
            conn = self.conectar_db()
            cursor = conn.cursor()
    
            # Reducir stock
            nuevo_stock = articulo.stock - cantidad
            cursor.execute("""
                UPDATE Articulo
                SET stock = ?
                WHERE id = ?
            """, (nuevo_stock, articulo.id))
    
            # Insertar la venta en la tabla 'Venta'
            cursor.execute("""
                INSERT INTO Venta (id_articulo, cantidad)
                VALUES (?, ?)
            """, (articulo.id, cantidad))
    
            conn.commit()
            conn.close()
    
            print(f"Venta realizada. {cantidad} unidades vendidas. Stock restante: {nuevo_stock}")
        else:
            print("No hay suficiente stock para realizar la venta.")
    
    
