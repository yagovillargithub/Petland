# Modulo que se encarga de las guardar los articulos en excel

#IMPORTACIONES
import pandas as pd
import os
import pyodbc
from articulo import Articulo

# INICIALIZACIONES
Articulo()

# Ruta del archivo Excel
archivo_excel = 'articulos.xlsx'


# Función para guardar el artículo en Excel
def guardar_articulo_en_excel(Articulo):
    # Verificar si el archivo ya existe
    if os.path.exists(archivo_excel):
        # Si el archivo existe, leer los datos existentes
        df_existente = pd.read_excel(archivo_excel)
    else:
        # Si no existe, crear un DataFrame vacío
        df_existente = pd.DataFrame(columns=['Id', "'Nombre', 'Descripcion', 'Precio', 'Stock'])

    # Crear un nuevo DataFrame con el artículo nuevo
    nuevo_articulo = pd.DataFrame({
        'Id': [id]
        'Nombre': [nombre],
        'Descripcion': [descripcion]
        'Precio': [precio],
        'Stock': [stock]
    })

    # Concatenar el nuevo artículo con los existentes
    df_actualizado = pd.concat([df_existente, nuevo_articulo], ignore_index=True)

    # Guardar el DataFrame actualizado en el archivo Excel
    df_actualizado.to_excel(archivo_excel, index=False)
    print(f'Artículo "{nombre}" guardado en {archivo_excel}.')


# Ejemplo de uso
guardar_articulo_en_excel('Laptop', 1500, 2)
guardar_articulo_en_excel('Teclado', 25, 5)
