import pyodbc
import datetime
from venta import Venta


# Clase que maneja las operaciones con la base de datos
class VentaService:
    def conectar_db(self):
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=MARTALB\\SQLEXPRESS;'
            'DATABASE=PetlandDb;'
            'UID=sa;'
            'PWD=1234'
        )
        return conn

    import datetime
    def realizar_venta(self):
        conn = self.conectar_db()
        cursor = conn.cursor()

        articulos = {}
        total = 0
        continuar = True

        # Solicitar los artículos y cantidades al usuario
        while continuar:
            id_articulo = int(input("Introduce el ID del artículo: "))
            cantidad = int(input(f"Introduce la cantidad a vender del artículo {id_articulo}: "))

            # Verificar el stock del artículo
            cursor.execute("SELECT stock, precio FROM Articulo WHERE id = ?", (id_articulo,))
            articulo = cursor.fetchone()

            if articulo is None:
                print(f"El artículo con ID {id_articulo} no existe.")
                continue

            stock, precio = articulo

            if stock >= cantidad:
                # Actualizar el stock del artículo
                nuevo_stock = stock - cantidad
                cursor.execute("""
                    UPDATE Articulo
                    SET stock = ?
                    WHERE id = ?
                """, (nuevo_stock, id_articulo))

                # Añadir el artículo al diccionario de artículos vendidos
                articulos[id_articulo] = {'cantidad': cantidad, 'precio_unitario': precio}
                total += cantidad * precio

                print(f"Venta del artículo {id_articulo} agregada. Stock restante: {nuevo_stock}")
            else:
                print(f"No hay suficiente stock para el artículo {id_articulo}. Stock disponible: {stock}")

            # Preguntar si desea agregar más artículos a la venta
            continuar = input("¿Quieres agregar otro artículo a la venta? (s/n): ").lower() == 's'

        # Recoger el método de pago
        metodo_pago = input("Introduce el método de pago: ")

        # Insertar la venta en la tabla 'Venta'
        fecha_venta = datetime.datetime.now()

        cursor.execute("""
                INSERT INTO Venta (fecha, metodo_pago, total, descuento)
                OUTPUT INSERTED.id  -- Devuelve el id generado por la inserción
                VALUES (?, ?, ?, ?)
            """, (fecha_venta, metodo_pago, total, 0))

        # Obtener el ID de la venta recién creada
        id_venta = cursor.fetchone()[0]  # Obtener el ID devuelto por OUTPUT INSERTED

        # Insertar los detalles de los artículos vendidos en la tabla 'VentaArticulo'
        for id_art, detalles in articulos.items():
            cursor.execute("""
                INSERT INTO VentaArticulo (id_venta, id_articulo, cantidad, precio_unitario)
                VALUES (?, ?, ?, ?)
            """, (id_venta, id_art, detalles['cantidad'], detalles['precio_unitario']))

        conn.commit()
        conn.close()

        print(f"Venta realizada exitosamente con un total de {total}.")

    # Calcular precio total (puedes ajustar según tu lógica)
    """
    Calcula el total de cada artículo, el precio total de cada uno y el total general.
    :param articulos: Diccionario con los detalles de los artículos vendidos.
                      Ejemplo: {1: {'cantidad': 2, 'precio_unitario': 10}, ...}
    :return: Diccionario con el desglose del total por artículo y el total general.
    """
    def calcular_total(self):

        conn = self.conectar_db()
        cursor = conn.cursor()

        articulos = {}
        continuar = True

        while continuar:
            id_articulo = int(input("Introduce el ID del artículo: "))
            cantidad = int(input(f"Introduce la cantidad del artículo {id_articulo}: "))

            # Obtener el precio del artículo desde la base de datos
            cursor.execute("SELECT precio FROM Articulo WHERE id = ?", (id_articulo,))
            articulo = cursor.fetchone()

            if articulo is None:
                print(f"El artículo con ID {id_articulo} no existe.")
                continue

            precio_unitario = articulo[0]
            articulos[id_articulo] = {'cantidad': cantidad, 'precio_unitario': precio_unitario}

            continuar = input("¿Quieres agregar otro artículo? (s/n): ").lower() == 's'

        conn.close()

        # Calcular totales
        resultado_total = self.calcular_total()

        # Mostrar el desglose
        print("Desglose del cálculo:")
        for id_articulo, info in resultado_total['desglose'].items():
            print(f"Artículo ID {id_articulo}: Cantidad: {info['cantidad']}, "
                  f"Precio Unitario: {info['precio_unitario']}, "
                  f"Total: {info['total_articulo']}")

        print(f"Total de la compra: {resultado_total['total_compra']}")

    # Leer ventas realizadas
    def leer_ventas(self):
        conn = self.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Venta")
        ventas = cursor.fetchall()
        conn.close()
        return ventas

    # Menú de opciones
    def menu(self):
        while True:
            print("\n--- CRUD Artículos ---")
            print("1. Realizar venta")
            print("2. Calcular total")
            print("3. Ver ventas")
            print("4. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.realizar_venta()

            elif opcion == "2":

              self.calcular_total()


            elif opcion == "3":
                ventas = self.leer_ventas()
                for venta in ventas:
                    print(f"ID: {venta.id}, Fecha: {venta.fecha}, Precio: {venta.total}")

            elif opcion == "4":
                print("Saliendo...")
                break

            else:
                print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    venta_service = VentaService()
    venta_service.menu()
