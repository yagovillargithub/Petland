from articulo import Articulo
from articuloService import ArticuloService
from venta import Venta
from ventaService import VentaService

# INICIALIZACION
articulo_service = ArticuloService()
Venta()
_ventaService = VentaService()

# Menú de opciones
def menu():
    while True:
        print("\n--- CRUD Artículos ---")
        print("1. Crear artículo")
        print("2. Ver artículos")
        print("3. Actualizar artículo")
        print("4. Eliminar artículo")
        print("5. Realizar venta")
        print("6. Leer ventas")
        print("7. Exportar artículos a Excel")
        print("8. Importar artículos desde Excel")
        print("9. Exportar ventas a Excel")
        print("10. Importar ventas desde Excel")
        print("11. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            descripcion = input("Descripción: ")
            precio = float(input("Precio: "))
            stock = int(input("Stock: "))
            articuloACrear = Articulo(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock)
            articulo_service.crear(articuloACrear)

        elif opcion == "2":
            articulos = articulo_service.leer_todos()
            for articulo in articulos:
                print(f"ID: {articulo.id}, Nombre: {articulo.nombre}, Precio: {articulo.precio}, Stock: {articulo.stock}")

        elif opcion == "3":
            id = int(input("ID del artículo a actualizar: "))
            nombre = input("Nuevo nombre: ")
            descripcion = input("Nueva descripción: ")
            precio = float(input("Nuevo precio: "))
            stock = int(input("Nuevo stock: "))
            articuloAActualizar = Articulo(id=id, nombre=nombre, descripcion=descripcion, precio=precio, stock=stock)
            articulo_service.actualizar(articuloAActualizar)

        elif opcion == "4":
            idArticulo = int(input("ID del artículo a eliminar: "))
            articulo_service.eliminar(idArticulo)

        elif opcion == "5":
            id = int(input("ID del artículo a vender: "))
            cantidad = int(input("Cantidad a vender: "))
            articulos = articulo_service.leer_todos()
            articulo_encontrado = None

            for articulo in articulos:
                if articulo.id == id:
                    articulo_encontrado = articulo
                    break

            if articulo_encontrado:
                articulo_service.realizar_venta(cantidad, articulo_encontrado)

            else:
                print("Artículo no encontrado.")

        elif opcion == "6":
            ventas = articulo_service.leer_ventas()
            for venta in ventas:
                print(
                    f"ID Venta: {venta.id}, ID Artículo: {venta.id_articulo}, Cantidad: {venta.cantidad}, Fecha: {venta.fecha}")


        elif opcion == "7":
            archivo = input("Ingresa el nombre del archivo Excel para exportar (ejemplo: backup.xlsx): ")
            articulo_service.exportar_articulos_a_excel(archivo)

        elif opcion == "8":
            archivo = input("Ingresa el nombre del archivo Excel para importar (ejemplo: backup.xlsx): ")
            articulo_service.importar_articulos_desde_excel(archivo)

        elif opcion == "9":
            archivo = input("Ingresa el nombre del archivo Excel para exportar ventas (ejemplo: ventas_backup.xlsx): ")
            articulo_service.exportar_ventas_a_excel(archivo)

        elif opcion == "10":
            archivo = input("Ingresa el nombre del archivo Excel para importar ventas (ejemplo: ventas_backup.xlsx): ")
            articulo_service.importar_ventas_desde_excel(archivo)

        elif opcion == "11":
            break

#menu()
_ventaService.menu()
