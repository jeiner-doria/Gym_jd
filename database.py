# database.py
# Base de datos SQLite del sistema de gestion de gimnasio.

import sqlite3
from pathlib import Path

RUTA_BD = Path(__file__).resolve().parent / "gimnasio.db"


def obtener_conexion():
    conexion = sqlite3.connect(RUTA_BD)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identificacion TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT NOT NULL,
            fecha_nacimiento TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identificacion TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            cargo TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entrenadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identificacion TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            especialidad TEXT NOT NULL
        )
    """)

    # RF08: catalogo de membresias.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS membresias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            duracion_meses INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)

    # RF09-RF11: membresia que tiene actualmente cada cliente.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente_membresia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            membresia_id INTEGER NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
            FOREIGN KEY (membresia_id) REFERENCES membresias(id)
        )
    """)

    # RF12-RF13: historial de pagos.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            membresia_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            valor REAL NOT NULL,
            metodo TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
            FOREIGN KEY (membresia_id) REFERENCES membresias(id)
        )
    """)

    # RF14: entradas al gimnasio.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingresos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora_entrada TEXT NOT NULL
        )
    """)

    # Datos iniciales utiles para RF08.
    membresias_base = [
        ("Mensual", 1, 50000),
        ("Trimestral", 3, 140000),
        ("Anual", 12, 500000),
    ]

    for nombre, duracion, precio in membresias_base:
        cursor.execute("""
            INSERT OR IGNORE INTO membresias (nombre, duracion_meses, precio)
            VALUES (?, ?, ?)
        """, (nombre, duracion, precio))

    conexion.commit()
    conexion.close()


# ---------------- CLIENTES ----------------

def insertar_cliente(identificacion, nombre, telefono, correo, fecha_nacimiento):
    try:
        with obtener_conexion() as conexion:
            conexion.execute("""
                INSERT INTO clientes
                (identificacion, nombre, telefono, correo, fecha_nacimiento)
                VALUES (?, ?, ?, ?, ?)
            """, (identificacion, nombre, telefono, correo, fecha_nacimiento))
        return True, "Cliente registrado correctamente."
    except sqlite3.IntegrityError:
        return False, "Ya existe un cliente con esa identificacion."
    except Exception as e:
        return False, f"Error al registrar cliente: {e}"


def buscar_cliente(identificacion):
    try:
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT id, identificacion, nombre, telefono, correo, fecha_nacimiento
                FROM clientes
                WHERE identificacion = ?
            """, (identificacion,)).fetchone()
    except Exception:
        return None


def obtener_todos_clientes():
    try:
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT id, identificacion, nombre, telefono, correo, fecha_nacimiento
                FROM clientes
                ORDER BY nombre
            """).fetchall()
    except Exception:
        return []


def actualizar_cliente(identificacion, nombre, telefono, correo, fecha_nacimiento):
    try:
        with obtener_conexion() as conexion:
            cursor = conexion.execute("""
                UPDATE clientes
                SET nombre = ?, telefono = ?, correo = ?, fecha_nacimiento = ?
                WHERE identificacion = ?
            """, (nombre, telefono, correo, fecha_nacimiento, identificacion))
            if cursor.rowcount == 0:
                return False, "Cliente no encontrado."
        return True, "Cliente actualizado correctamente."
    except Exception as e:
        return False, f"Error al actualizar cliente: {e}"


def eliminar_cliente(identificacion):
    try:
        with obtener_conexion() as conexion:
            cursor = conexion.execute(
                "DELETE FROM clientes WHERE identificacion = ?",
                (identificacion,)
            )
            if cursor.rowcount == 0:
                return False, "Cliente no encontrado."
        return True, "Cliente eliminado correctamente."
    except Exception as e:
        return False, f"Error al eliminar cliente: {e}"


# ---------------- EMPLEADOS ----------------

def insertar_empleado(identificacion, nombre, telefono, cargo):
    try:
        with obtener_conexion() as conexion:
            conexion.execute("""
                INSERT INTO empleados (identificacion, nombre, telefono, cargo)
                VALUES (?, ?, ?, ?)
            """, (identificacion, nombre, telefono, cargo))
        return True, "Empleado registrado correctamente."
    except sqlite3.IntegrityError:
        return False, "Ya existe un empleado con esa identificacion."
    except Exception as e:
        return False, f"Error al registrar empleado: {e}"


def buscar_empleado(identificacion):
    try:
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT id, identificacion, nombre, telefono, cargo
                FROM empleados
                WHERE identificacion = ?
            """, (identificacion,)).fetchone()
    except Exception:
        return None


def obtener_todos_empleados():
    try:
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT id, identificacion, nombre, telefono, cargo
                FROM empleados
                ORDER BY nombre
            """).fetchall()
    except Exception:
        return []


# ---------------- ENTRENADORES ----------------

def insertar_entrenador(identificacion, nombre, especialidad):
    try:
        with obtener_conexion() as conexion:
            conexion.execute("""
                INSERT INTO entrenadores (identificacion, nombre, especialidad)
                VALUES (?, ?, ?)
            """, (identificacion, nombre, especialidad))
        return True, "Entrenador registrado correctamente."
    except sqlite3.IntegrityError:
        return False, "Ya existe un entrenador con esa identificacion."
    except Exception as e:
        return False, f"Error al registrar entrenador: {e}"


def buscar_entrenador(identificacion):
    try:
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT id, identificacion, nombre, especialidad
                FROM entrenadores
                WHERE identificacion = ?
            """, (identificacion,)).fetchone()
    except Exception:
        return None


def obtener_todos_entrenadores():
    try:
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT id, identificacion, nombre, especialidad
                FROM entrenadores
                ORDER BY nombre
            """).fetchall()
    except Exception:
        return []


# ---------------- MEMBRESIAS RF08-RF11 ----------------

def obtener_membresias():
    with obtener_conexion() as conexion:
        return conexion.execute("""
            SELECT id, nombre, duracion_meses, precio
            FROM membresias
            ORDER BY duracion_meses
        """).fetchall()


def insertar_membresia(nombre, duracion_meses, precio):
    try:
        with obtener_conexion() as conexion:
            conexion.execute("""
                INSERT INTO membresias (nombre, duracion_meses, precio)
                VALUES (?, ?, ?)
            """, (nombre, duracion_meses, precio))
        return True, "Membresia registrada correctamente."
    except sqlite3.IntegrityError:
        return False, "Ya existe una membresia con ese nombre."
    except Exception as e:
        return False, f"Error al registrar membresia: {e}"


def asignar_membresia(cliente_id, membresia_id, fecha_inicio, fecha_fin):
    try:
        with obtener_conexion() as conexion:
            conexion.execute("""
                UPDATE cliente_membresia
                SET estado = 'Vencida'
                WHERE cliente_id = ? AND estado = 'Activa'
            """, (cliente_id,))

            conexion.execute("""
                INSERT INTO cliente_membresia
                (cliente_id, membresia_id, fecha_inicio, fecha_fin, estado)
                VALUES (?, ?, ?, ?, 'Activa')
            """, (cliente_id, membresia_id, fecha_inicio, fecha_fin))

        return True, "Membresia asignada correctamente."
    except Exception as e:
        return False, f"Error al asignar membresia: {e}"


def obtener_membresia_cliente(cliente_id):
    with obtener_conexion() as conexion:
        return conexion.execute("""
            SELECT cm.id, m.nombre, m.duracion_meses, m.precio,
                   cm.fecha_inicio, cm.fecha_fin, cm.estado, m.id
            FROM cliente_membresia cm
            INNER JOIN membresias m ON m.id = cm.membresia_id
            WHERE cm.cliente_id = ?
            ORDER BY cm.id DESC
            LIMIT 1
        """, (cliente_id,)).fetchone()


def actualizar_estados_membresias():
    with obtener_conexion() as conexion:
        conexion.execute("""
            UPDATE cliente_membresia
            SET estado = 'Vencida'
            WHERE date(fecha_fin) < date('now') AND estado != 'Vencida'
        """)


def renovar_membresia(cliente_id, membresia_id, fecha_inicio, fecha_fin):
    try:
        with obtener_conexion() as conexion:
            conexion.execute("""
                UPDATE cliente_membresia
                SET estado = 'Vencida'
                WHERE cliente_id = ? AND estado = 'Activa'
            """, (cliente_id,))

            conexion.execute("""
                INSERT INTO cliente_membresia
                (cliente_id, membresia_id, fecha_inicio, fecha_fin, estado)
                VALUES (?, ?, ?, ?, 'Activa')
            """, (cliente_id, membresia_id, fecha_inicio, fecha_fin))

        return True, "Membresia renovada correctamente."
    except Exception as e:
        return False, f"Error al renovar membresia: {e}"


# ---------------- PAGOS RF12-RF13 ----------------

def registrar_pago(cliente_id, membresia_id, fecha, valor, metodo):
    try:
        with obtener_conexion() as conexion:
            conexion.execute("""
                INSERT INTO pagos (cliente_id, membresia_id, fecha, valor, metodo)
                VALUES (?, ?, ?, ?, ?)
            """, (cliente_id, membresia_id, fecha, valor, metodo))
        return True, "Pago registrado correctamente."
    except Exception as e:
        return False, f"Error al registrar pago: {e}"


def obtener_pagos_cliente(cliente_id):
    with obtener_conexion() as conexion:
        return conexion.execute("""
            SELECT p.id, p.fecha, m.nombre, p.valor, p.metodo
            FROM pagos p
            INNER JOIN membresias m ON m.id = p.membresia_id
            WHERE p.cliente_id = ?
            ORDER BY p.id DESC
        """, (cliente_id,)).fetchall()


# ---------------- INGRESOS RF14 ----------------

def registrar_ingreso(cliente_id, fecha, hora):
    try:
        with obtener_conexion() as conexion:
            conexion.execute("""
                INSERT INTO ingresos (cliente_id, fecha, hora_entrada)
                VALUES (?, ?, ?)
            """, (cliente_id, fecha, hora))
        return True, "Ingreso registrado correctamente."
    except Exception as e:
        return False, f"Error al registrar ingreso: {e}"


def obtener_ingresos_cliente(cliente_id):
    with obtener_conexion() as conexion:
        return conexion.execute("""
            SELECT id, fecha, hora_entrada
            FROM ingresos
            WHERE cliente_id = ?
            ORDER BY id DESC
        """, (cliente_id,)).fetchall()


crear_tablas()
actualizar_estados_membresias()

