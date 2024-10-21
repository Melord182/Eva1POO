import sqlite3
from datetime import date
from bd import *

fecha_actual = date.today()
#CONEXION CON LA BASE DE DATOS
conn=sqlite3.connect("inventario.db")
c=conn.cursor()

class Producto:
    #OBTENER FECHA ACTUAL
    fecha_actual = date.today()
    
    #METODO DE LA CLASE PRODUCTOS, EL CUAL CREARA LOS PRODUCTOS QUE SE INGRESARAN AL INVENTARIO
    def crear_producto(nombre, cantidad, descripcion,precio,proveedor):
        try:
            #Obtener la id del proveedor segun su nombre
            c.execute("SELECT prov_id from proveedor Where nomprov=?",(proveedor,))
            idprov=c.fetchone()
            #Ver si la ID no exista arrojar mensaje de proveedor no encontrado
            if idprov is None:
                print("Proveedor no encontrado.")
                return
            idprov = idprov[0]

            #INSERTAR EN TABLA PRODUCTO
            c.execute("INSERT INTO producto (nomprod,fecha, cantidad, descripcion) VALUES (?,?, ?, ?)", (nombre,fecha_actual, cantidad, descripcion,))
            
            #ALMACENAMOS LA ID QUE SE LE ASIGNA AL PRODUCTO Y LA GUARDAMOS EN UNA VARIABLE PARA PODER IDENTIFICARLO 
            prod_id = c.lastrowid
            #CREAMOS UNA CONSULTA PARA OBTENER LA ID Y EL STOCK DEL PRODUCTO, SI EL NOMBRE, DESCRIPCION Y PRECIO SON IGUALES NO LO CREARA DENUEVO
            c.execute("SELECT d.prod_id, d.stock FROM detalle d JOIN producto p ON d.prod_id = p.prod_id WHERE p.nomprod = ? AND p.descripcion = ? AND d.precio = ?", (nombre, descripcion, precio,))
            #GUARDAMOS EL RESULTADO DE LA CONSULTA EN UNA VARIABLE
            resultado = c.fetchone() 
            #SI AL REALIZAR LA CONSULTA VEMOS QUE LA ID YA EXISTE, SOLO MODIFICAMOS EL STOCK
            if resultado is not None:
                #Si el producto existe actualiza el stock
                prod_id, stock_existente = resultado
                nuevo_stock = stock_existente + cantidad
                c.execute("UPDATE detalle SET stock = ? WHERE prod_id = ?", (nuevo_stock, prod_id))
                print(f"Se han actualizado {nombre} con un nuevo stock de {nuevo_stock}.")
                print(idprov)
                conn.commit()
            else:
                #SI DETECTA QUE NO EXISTE NINGUNA ID QUE COINCIDA CON LOS PARAMETROS, INTRODUCE EL PRODUCTO COMO UNO NUEVO ASIGNANDOLE NUEVA ID
                
                c.execute("INSERT INTO detalle (precio, stock, prod_id,prov_id) VALUES (?, ?, ?, ?)", (precio, cantidad, prod_id ,idprov))
                print(f"Se han ingresado {cantidad} de {nombre}.")
        except sqlite3.Error as error:
            print(f"Error al crear el producto: {error}")
            Producto.crear_producto()
        conn.commit()
     
     
     
     #METODO QUE SE USARA PARA MODIFICAR PRODUCTOS
    def modificar_producto(id_seleccionada, nuevo_nombre, nueva_cantidad, nueva_descripcion, nuevo_precio, nuevo_proveedor):
        try:
            #PRIMERO COMPROBAMOS QUE EL NUEVO PROVEEDOR QUE INGRESARA EL USUARIO EXISTE
            c.execute("SELECT prov_id FROM proveedor WHERE nomprov=?", (nuevo_proveedor,))
            idprov = c.fetchone()
            
            if idprov is None:
                print("Proveedor no encontrado.")
                return
            
            idprov = idprov[0]
            
            #UNA VEZ COMPROBADO QUE TODO ESTE BIEN, SE MODIFICA EL PRODUCTO TANTO EN LA TABLA PRODUCTO
            c.execute("UPDATE producto SET nomprod=?, fecha=?, cantidad=?, descripcion=? WHERE prod_id=?",
                    (nuevo_nombre, fecha_actual, nueva_cantidad, nueva_descripcion, id_seleccionada))
            
            #COMO EN LA TABLA DETALLE
            c.execute("SELECT stock FROM detalle WHERE prod_id = ?",(id_seleccionada,))
            stock_actual = c.fetchone()
            stock_actual=stock_actual[0]
            int(stock_actual)
            nuevo_stock = stock_actual + nueva_cantidad
            c.execute("UPDATE detalle SET precio=?,stock=?, prov_id=? WHERE prod_id=?", (nuevo_precio,nuevo_stock, idprov, id_seleccionada))
            
            print(f"Producto con ID {id_seleccionada} ha sido modificado.")
            conn.commit()
        except sqlite3.Error as error:
            print(f"Error al modificar producto: {error}")
            
            
    #METODO PARA ELIMINAR PRODUCTOS SEGUN SU ID
    def eliminar_producto(prod_id):
        try:
            #PRIMERO EL USUARIO INGRESARA LA ID DEL PRODUCTO A ELIMINAR, PRIMERO BUSCARA SI EXISTE Y LUEGO BUSCARA LA ID DE ESE PRODUCTO PERO EN LA TABLA DETALLES
            c.execute("SELECT detalles_id FROM detalle WHERE prod_id = ?", (prod_id,))
            id_detalle = c.fetchone()
            
            #SI EN LA TABLA DETALLES NO ENCUENTRA LA ID DEL PRODUCTO IMPRIMIRA ESTE MENSAJE
            if id_detalle is None:
                print(f"No se encontró el producto con id {prod_id}.")
                return
            #SI EL ID DEL PRODUCTO EXISTE EN LA TABLA DETALLES, OBTENDREMOS LA ID DEL PRODUCTO EN ESTA TABLA PERO EN FORMA DE LISTA, AHORA SACAMOS 
            #EL PRIMER Y UNICO VALOR DE ESTA LISTA Y DE ESA FORMA TENEMOS SELECIONADO EL PRODUCTO TANTO EN LA TABLA PRODUCTOS COMO EN DETALLES
            id_detalle = id_detalle[0]
            
            #BORRAMOS EL PRODUCTO DE DETALLE CUYO PRODUCTO TENGA LA ID SELECCIONADA POR EL USUARIO 
            c.execute("DELETE FROM detalle WHERE detalles_id = ?", (id_detalle,))
            
            #FINALMENTE BORRAMOS EL PRODUCTO DE LA TABLA PRODUCTO CON LA ID INDICADA POR EL USUARIO
            c.execute("DELETE FROM producto WHERE prod_id = ?", (prod_id,))
            
            print(f"Producto con id {prod_id} y sus detalles han sido eliminados.")
            conn.commit()
        except sqlite3.Error as error:
            print(f"Error al eliminar producto {error}")
     

    



class Proveedor:
    
    fecha_actual = date.today()
    
    #METODO PARA CREAR PROVEEDOR
    def crear_proveedor(nomprov,direcc):
        try:
        
            c.execute("SELECT p.prov_id FROM proveedor p WHERE p.nomprov = ? AND p.direcc = ?",(nomprov,direcc,))
            resultadop = c.fetchone()
            
            
            if resultadop is not None:
                print("Proveedor ya existe")
            
            else: 
                c.execute("INSERT INTO proveedor (nomprov,direcc) VALUES (?,?)",(nomprov,direcc,))
                print("Proveedor creado")
            conn.commit()
        except sqlite3.Error as error:
            print(f"Error al crear proveedor {error}")
        
    #ELIMINAR PROVEEDOR CON LA ID
    def eliminar_proveedor(prov_id):
        try:
            c.execute("DELETE FROM proveedor WHERE prov_id=?",(prov_id,))
            print("Proveedor Eliminado")
            conn.commit()
        except sqlite3.Error as error:
            print(f"Error al eliminar proveedor {error}")
       
    #MODIFICAR PROVEEDOR CON LA ID
    def modificar_proveedor(prov_id, nuevo_nombre, nueva_direccion):
        try:
            # Verificar si el proveedor existe
            c.execute("SELECT prov_id FROM proveedor WHERE prov_id=?", (prov_id,))
            resultado = c.fetchone()
            
            if resultado is None:
                print("Proveedor no encontrado.")
                return
            
            # Actualizar la tabla proveedor
            c.execute("UPDATE proveedor SET nomprov=?, direcc=? WHERE prov_id=?", 
                    (nuevo_nombre, nueva_direccion, prov_id))
            
            print(f"Proveedor con ID {prov_id} ha sido modificado.")
            conn.commit()
        except sqlite3.Error as error:
            print(f"Error al modificar proveedor: {error}")