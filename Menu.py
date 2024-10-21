import os
from bd import BaseDatos
from Crud import Producto, Proveedor
from datetime import date

#DETECTA SI EXISTE LA BASE DE DATOS, SI NO LA CREA.
if not os.path.exists("inventario.db"):
    bd = BaseDatos() 
else:
    print("Base de datos 'inventario.db' encontrada.")
#FUNCION QUE MUESTRA EL MENU PRINCIPAL
def mostrar_menu():
    while True:
        print("\nBienvenido al sistema de inventario.")
        print("1. Iniciar sesión como Trabajador")
        print("2. Iniciar sesión como Administrador")
        print("3. Cerrar")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            menu_trabajador()
        elif opcion == '2':
            menu_administrador()
        elif opcion == '3':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
            
#MENU QUE MOSTRARA LAS OPCIONES DISPONIBLES PARA EL USUARIO "TRABAJADOR"
def menu_trabajador():
    while True:
        print("\n--- Menú Trabajador ---")
        print("1. Visualizar inventario")
        print("2. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            bd = BaseDatos()
            print("ID | Nombre | Proveedor | Stock total")
            bd.mostrar_vista_producto_resumen()
            
            
            input("Presiona Enter para continuar...")
        elif opcion == '2':
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

#MENU QUE MOSTRARA LAS OPCIONES DISPONIBLES PARA EL USUARIO "ADMINISTRADOR"
def menu_administrador():
    while True:
        usuario = input("Introduce el nombre de usuario: ")
        contrasena = input("Introduce la contraseña: ")

        if usuario == "usuario" and contrasena == "contraseña":
            print("Inicio de sesión exitoso.")
            break
        else:
            print("Usuario o contraseña incorrectos. Inténtalo de nuevo.")

    while True:
        print("\n--- Menú Administrador ---")
        print("1. Trabajar con Productos")
        print("2. Trabajar con Proveedores")
        print("3. Visualizar inventario")
        print("4. Cerrar sesión")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            menu_productos()
        elif opcion == '2':
            menu_proveedores()
        elif opcion == '3':
            bd = BaseDatos()
            print(" ID | Nombre | Descripcion | Precio | Proveedor | Stock")
            bd.mostrar_vista_productos_completa() 
            input("Presiona Enter para continuar...")
        elif opcion == '4':
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
#MENU DEL ADMINISTRADOR QUE LE PERMITE TRABAJAR CON LOS PRODUCTOS
def menu_productos():
    while True:
        print("\n--- Menú Productos ---")
        print("1. Crear producto")
        print("2. Modificar producto")
        print("3. Eliminar producto")
        print("4. Visualizar productos")
        print("5. Volver")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("Nombre del producto: ")
            cantidad = int(input("Cantidad: "))
            descripcion = input("Descripción: ")
            precio = float(input("Precio: "))
            proveedor = input("Nombre del proveedor: ")
            Producto.crear_producto(nombre, cantidad, descripcion, precio, proveedor)
        elif opcion == '2':
            id_seleccionada = int(input("ID del producto a modificar: "))
            nuevo_nombre = input("Nuevo nombre: ")
            nueva_cantidad = int(input("Nueva cantidad: "))
            nueva_descripcion = input("Nueva descripción: ")
            nuevo_precio = float(input("Nuevo precio: "))
            nuevo_proveedor = input("Nuevo proveedor: ")
            Producto.modificar_producto(id_seleccionada, nuevo_nombre, nueva_cantidad, nueva_descripcion, nuevo_precio, nuevo_proveedor)
        elif opcion == '3':
            prod_id = int(input("ID del producto a eliminar: "))
            Producto.eliminar_producto(prod_id)
        elif opcion == '4':
            bd = BaseDatos()
            bd.mostrar_vista_productos_completa()
            input("Presiona Enter para continuar...")
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
#MENU DEL ADMIN QUE LE PERMITE TRABAJAR CON LOS PROVEEDORES
def menu_proveedores():
    while True:
        print("\n--- Menú Proveedores ---")
        print("1. Crear proveedor")
        print("2. Visualizar proveedores")
        print("3. Eliminar proveedor")
        print("4. Modificar proveedor")
        print("5. Volver")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nomprov = input("Nombre del proveedor: ")
            direcc = input("Dirección: ")
            Proveedor.crear_proveedor(nomprov, direcc)
        elif opcion == '2':
            bd = BaseDatos()
            print("ID   |   NOMBRE   |   DIRECCION")
            bd.mostrar_vista_proveedores_completa() 
            input("Presiona Enter para continuar...")
        elif opcion == '3':
            prov_id = int(input("ID del proveedor a eliminar: "))
            Proveedor.eliminar_proveedor(prov_id)
        elif opcion == '4':
            prov_id = int(input("ID del proveedor a modificar: "))
            nuevo_nombre = input("Nuevo nombre: ")
            nueva_direccion = input("Nueva dirección: ")
            Proveedor.modificar_proveedor(prov_id, nuevo_nombre, nueva_direccion)
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
#BUCLE PARA QUE EL MENU SE MUESTRE
if __name__ == "__main__":
    mostrar_menu()
