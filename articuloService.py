# Modulo que se encarga de las operaciones contra la base de datos

# IMPORTACIONES
import pyodbc
from articulo import Articulo
import pandas as pd #para poder importar y exportar excel

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

    # Exportar artículos a un archivo Excel
    def exportar_articulos_a_excel(self, archivo):
        conn = self.conectar_db()
        query = "SELECT * FROM Articulo"
        df = pd.read_sql(query, conn)
        conn.close()
        df.to_excel(archivo, index=False)
        print(f"Datos exportados a {archivo} exitosamente.")

    # Importar artículos desde un archivo Excel
    def importar_articulos_desde_excel(self, archivo):
        df = pd.read_excel(archivo)
        conn = self.conectar_db()
        cursor = conn.cursor()

        for index, row in df.iterrows():
            # Verificar si el artículo ya existe en la base de datos
            cursor.execute("SELECT * FROM Articulo WHERE id = ?", (row['id'],))
            articulo_existente = cursor.fetchone()

            if articulo_existente:
                # Si existe, actualizamos el artículo
                cursor.execute("""
                                UPDATE Articulo
                                SET nombre = ?, descripcion = ?, precio = ?, stock = ?
                                WHERE id = ?
                            """, (row['nombre'], row['descripcion'], row['precio'], row['stock'], row['id']))
                print(f"Artículo con ID {row['id']} actualizado.")
            else:
                # Si no existe, insertamos el artículo con su propio ID
                cursor.execute("""
                                SET IDENTITY_INSERT Articulo ON;
                                INSERT INTO Articulo (id, nombre, descripcion, precio, stock) 
                                VALUES (?, ?, ?, ?, ?);
                                SET IDENTITY_INSERT Articulo OFF;
                            """, (row['id'], row['nombre'], row['descripcion'], row['precio'], row['stock']))
                print(f"Artículo con ID {row['id']} insertado.")

        conn.commit()
        conn.close()
        print(f"Datos importados desde {archivo} exitosamente.")


    # Exportar ventas a un archivo Excel
    def exportar_ventas_a_excel(self, archivo):
        conn = self.conectar_db()
        query = "SELECT * FROM Venta"
        df = pd.read_sql(query, conn)
        conn.close()
        df.to_excel(archivo, index=False)
        print(f"Ventas exportadas a {archivo} exitosamente.")

    # Importar ventas desde un archivo Excel
    def importar_ventas_desde_excel(self, archivo):
        df = pd.read_excel(archivo)
        conn = self.conectar_db()
        cursor = conn.cursor()

        for index, row in df.iterrows():
            # Verificar si la venta ya existe en la base de datos
            cursor.execute("SELECT * FROM Venta WHERE id = ?", (row['id'],))
            venta_existente = cursor.fetchone()

            if venta_existente:
                # Si existe, actualizamos la venta
                cursor.execute("""
                    UPDATE Venta
                    SET id_articulo = ?, cantidad = ?
                    WHERE id = ?
                """, (row['id_articulo'], row['cantidad'], row['id']))
                print(f"Venta con ID {row['id']} actualizada.")
            else:
                # Si no existe, insertamos la venta con su propio ID
                cursor.execute("""
                    SET IDENTITY_INSERT Venta ON;
                    INSERT INTO Venta (id, id_articulo, cantidad) 
                    VALUES (?, ?, ?);
                    SET IDENTITY_INSERT Venta OFF;
                """, (row['id'], row['id_articulo'], row['cantidad']))
                print(f"Venta con ID {row['id']} insertada.")

        conn.commit()
        conn.close()
        print(f"Ventas importadas desde {archivo} exitosamente.")