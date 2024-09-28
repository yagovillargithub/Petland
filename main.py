from articulo import Articulo
from articuloService import ArticuloService

# INICIALIZACION
articulo_service = ArticuloService()

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
                articulo = Articulo(id=articulo_encontrado.id, nombre=articulo_encontrado.nombre,
                                    descripcion=articulo_encontrado.descripcion, precio=articulo_encontrado.precio,
                                    stock=articulo_encontrado.stock)
                articulo_service.realizar_venta(cantidad, articulo)
            else:
                print("Artículo no encontrado.")

        elif opcion == "6":
            break

menu()

