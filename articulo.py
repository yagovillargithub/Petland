import pyodbc

class Articulo:
    def __init__(self, id=None, nombre=None, descripcion=None, precio=None, stock=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

    # Conexión a la base de datos
    def conectar_db():
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=MARTALB\SQLEXPRESS;'
            'DATABASE=PetlandDb;'
            'UID=sa;'
            'PWD=1234'
        )
        return conn


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

# Menú de opciones
def menu():
    while True:
        print("\n--- CRUD Artículos ---")
        print("1. Crear artículo")
        print("2. Ver artículos")
        print("3. Actualizar artículo")
        print("4. Eliminar artículo")
        print("5. Realizar venta")
        print("6. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            descripcion = input("Descripción: ")
            precio = float(input("Precio: "))
            stock = int(input("Stock: "))
            articulo = Articulo(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock)
            articulo.crear()

        elif opcion == "2":
            articulos = Articulo.leer_todos()
            for articulo in articulos:
                print(f"ID: {articulo.id}, Nombre: {articulo.nombre}, Precio: {articulo.precio}, Stock: {articulo.stock}")

        elif opcion == "3":
            id = int(input("ID del artículo a actualizar: "))
            nombre = input("Nuevo nombre: ")
            descripcion = input("Nueva descripción: ")
            precio = float(input("Nuevo precio: "))
            stock = int(input("Nuevo stock: "))
            articulo = Articulo(id=id, nombre=nombre, descripcion=descripcion, precio=precio, stock=stock)
            articulo.actualizar()

        elif opcion == "4":
            id = int(input("ID del artículo a eliminar: "))
            Articulo.eliminar(id)

        elif opcion == "5":
            id = int(input("ID del artículo a vender: "))
            cantidad = int(input("Cantidad a vender: "))
            articulos = Articulo.leer_todos()
            articulo_encontrado = None

            for articulo in articulos:
                if articulo.id == id:
                    articulo_encontrado = articulo
                    break

            if articulo_encontrado:
                articulo = Articulo(id=articulo_encontrado.id, nombre=articulo_encontrado.nombre,
                                    descripcion=articulo_encontrado.descripcion, precio=articulo_encontrado.precio,
                                    stock=articulo_encontrado.stock)
                articulo.realizar_venta(cantidad)
            else:
                print("Artículo no encontrado.")

        elif opcion == "6":
            break


if __name__ == "__main__":
    menu()
