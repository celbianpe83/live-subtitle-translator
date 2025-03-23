import sqlite3

class TranslationRepository:
    def __init__(self, db_path="traduciones.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS traducciones (
                filme TEXT,
                original TEXT,
                traducido TEXT,
                UNIQUE(filme, original)
            )
        """)
        self.conn.commit()

    def obtener_titulos_existentes(self):
        self.cursor.execute("SELECT DISTINCT filme FROM traducciones")
        return [row[0] for row in self.cursor.fetchall()]

    def obtener_traducciones_por_filme(self, filme):
        self.cursor.execute("SELECT original, traducido FROM traducciones WHERE filme = ?", (filme,))
        return self.cursor.fetchall()

    def guardar_traduccion(self, filme, original, traducido):
        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO traducciones (filme, original, traducido) VALUES (?, ?, ?)",
                (filme, original, traducido)
            )
        except Exception as e:
            print(f"Error al guardar traducción: {e}")

    def guardar_traducciones(self, filme, nuevas_traducciones):
        for original, traducido in nuevas_traducciones.items():
            self.guardar_traduccion(filme, original, traducido)
        self.conn.commit()

    def cerrar(self):
        self.conn.commit()
        self.conn.close()