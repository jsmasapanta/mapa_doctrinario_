import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        """
        Inicializa la conexión con la base de datos SQLite y crea la tabla si no existe.
        """
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """
        Crea la tabla 'manuales' si no existe.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS manuales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria_x TEXT,
                subcategoria_x TEXT,
                categoria_y TEXT,
                nombre TEXT,
                anio INTEGER,
                estado TEXT,
                subproceso_estado TEXT,
                id_categoria INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_manual(self, categoria_x, subcategoria_x, categoria_y, nombre, anio, estado, subproceso_estado, id_categoria=0):
        """
        Agrega un nuevo manual a la base de datos SQLite.
        """
        self.cursor.execute('''
            INSERT INTO manuales (categoria_x, subcategoria_x, categoria_y, nombre, anio, estado, subproceso_estado, id_categoria)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (categoria_x, subcategoria_x, categoria_y, nombre, anio, estado, subproceso_estado, id_categoria))
        self.conn.commit()
        return self.cursor.lastrowid  # Devuelve el ID del nuevo manual

    def fetch_data(self):
        """
        Obtiene todos los manuales de la base de datos.
        """
        self.cursor.execute('SELECT * FROM manuales')
        rows = self.cursor.fetchall()
        return [self._convert_to_dict(row) for row in rows]

    def fetch_manual_by_id(self, manual_id):
        """
        Obtiene un manual específico por su ID.
        """
        self.cursor.execute('SELECT * FROM manuales WHERE id = ?', (manual_id,))
        row = self.cursor.fetchone()
        return self._convert_to_dict(row) if row else None

    def update_manual(self, manual_id, categoria_x, subcategoria_x, categoria_y, nombre, anio, estado, subproceso_estado):
        """
        Actualiza un manual existente en la base de datos.
        """
        self.cursor.execute('''
            UPDATE manuales
            SET categoria_x = ?, subcategoria_x = ?, categoria_y = ?, nombre = ?, anio = ?, estado = ?, subproceso_estado = ?
            WHERE id = ?
        ''', (categoria_x, subcategoria_x, categoria_y, nombre, anio, estado, subproceso_estado, manual_id))
        self.conn.commit()

    def delete_manual(self, manual_id):
        """
        Elimina un manual por su ID.
        """
        self.cursor.execute('DELETE FROM manuales WHERE id = ?', (manual_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0  # Devuelve True si se eliminó un registro

    def _convert_to_dict(self, row):
        """
        Convierte una fila de la base de datos en un diccionario.
        """
        return {
            "id": row[0],
            "categoria_x": row[1],
            "subcategoria_x": row[2],
            "categoria_y": row[3],
            "nombre": row[4],
            "anio": row[5],
            "estado": row[6],
            "subproceso_estado": row[7],
            "id_categoria": row[8]
        }

    def close_connection(self):
        """
        Cierra la conexión con la base de datos.
        """
        self.conn.close()