import sqlite3

class BaseDatos:
    def __init__(self, inventario="inventario.db"):
        self.conexion = sqlite3.connect(inventario)
        self.cursor = self.conexion.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS CATEGORIA (
            CATEGORIA_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE VARCHAR(20) NOT NULL
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS PRODUCTO (
            PROD_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMPROD VARCHAR(20),
            FECHA DATE,
            CANTIDAD INTEGER,
            DESCRIPCION VARCHAR(20),
            CATEGORIA_ID INTEGER,
            FOREIGN KEY (CATEGORIA_ID) REFERENCES CATEGORIA(CATEGORIA_ID)
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS PROVEEDOR (
            PROV_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMPROV VARCHAR(20),
            DIRECC VARCHAR(20) 
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS DETALLE (
            DETALLES_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            PRECIO INTEGER,
            STOCK INTEGER,
            PROD_ID INTEGER,
            PROV_ID INTEGER,
            FOREIGN KEY (PROD_ID) REFERENCES PRODUCTO(PROD_ID),
            FOREIGN KEY (PROV_ID) REFERENCES PROVEEDOR(PROV_ID)
        )""")
        self.conexion.commit()

    def cerrar_conexion(self):
        self.conexion.close()

    def crear_vista_proveedor(self):
        try:
            self.cursor.execute("""CREATE VIEW IF NOT EXISTS VISTA_PROVEEDOR AS SELECT * FROM PROVEEDOR""")
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la vista proveedor: {e}")

    def mostrar_vista_proveedor(self):
        self.cursor.execute("SELECT * FROM VISTA_PROVEEDOR")
        resultados = self.cursor.fetchall()
        for fila in resultados:
            print(fila)

    def crear_vista_productos_resumen(self):
        try:
            self.cursor.execute("""CREATE VIEW IF NOT EXISTS VISTA_PRODUCTOS_RESUMEN AS 
                                SELECT PRODUCTO.PROD_ID, PRODUCTO.NOMPROD, PROVEEDOR.NOMPROV, DETALLE.STOCK
                                FROM PRODUCTO 
                                JOIN DETALLE ON PRODUCTO.PROD_ID = DETALLE.PROD_ID
                                JOIN PROVEEDOR ON DETALLE.PROV_ID = PROVEEDOR.PROV_ID
                                """)
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la vista de productos resumen: {e}")

    def mostrar_vista_producto_resumen(self):
        self.cursor.execute("SELECT * FROM VISTA_PRODUCTOS_RESUMEN")
        resultados = self.cursor.fetchall()
        for fila in resultados:
            print(fila)

    def crear_vista_productos_completa(self):
        try:
            self.cursor.execute(""" CREATE VIEW IF NOT EXISTS VISTA_PRODUCTO_COMPLETA AS
                                SELECT p.PROD_ID, p.NOMPROD, p.DESCRIPCION, d.PRECIO, d.STOCK AS STOCK, pr.NOMPROV
                                FROM PRODUCTO p 
                                JOIN DETALLE d ON p.PROD_ID = d.PROD_ID 
                                JOIN PROVEEDOR pr ON d.PROV_ID = pr.PROV_ID
                                """)
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la vista de productos completa: {e}")

    def mostrar_vista_productos_completa(self):
        self.cursor.execute("SELECT * FROM VISTA_PRODUCTO_COMPLETA")
        resultados = self.cursor.fetchall()
        for fila in resultados:
            print(fila)

    def crear_categoria(self, nombre):
        try:
            self.cursor.execute("INSERT INTO CATEGORIA (NOMBRE) VALUES (?)", (nombre,))
            self.conexion.commit()
            print(f"La categoría '{nombre}' insertada con éxito.")
        except sqlite3.Error as e:
            print(f"Error al insertar la categoría: {e}")

    def crear_vista_categoria(self):
        try:
            self.cursor.execute("""CREATE VIEW IF NOT EXISTS VISTA_CATEGORIA AS SELECT * FROM CATEGORIA""")
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la vista categoría: {e}")

    def mostrar_categorias(self):
        self.cursor.execute("SELECT * FROM VISTA_CATEGORIA")
        resultados = self.cursor.fetchall()
        for fila in resultados:
            print(fila)


    def crear_vista_proveedores_completa(self):
        try:
            self.cursor.execute(""" 
                CREATE VIEW IF NOT EXISTS VISTA_PROVEEDORES_COMPLETA AS 
                SELECT * FROM PROVEEDOR
            """)
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la vista de proveedores completa: {e}")

        except sqlite3.Error as e:
            print(f"Error al crear la vista de productos completa: {e}")
    def mostrar_vista_proveedores_completa(self):
        self.cursor.execute("SELECT * FROM VISTA_PROVEEDORES_COMPLETA")
        resultados = self.cursor.fetchall()
        if resultados:
            for fila in resultados:
                print(fila)
        else:
            print("No hay proveedores disponibles.")




bd = BaseDatos()
bd.crear_vista_proveedores_completa()
bd.crear_vista_productos_completa()
bd.crear_vista_productos_resumen()
bd.cerrar_conexion()
