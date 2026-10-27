# validaciones.py
# Validaciones de los formularios de RF01-RF07 y de los nuevos modulos.

import re
from datetime import datetime


def texto_obligatorio(valor, campo):
    if not valor.strip():
        return False, f"El campo {campo} es obligatorio."
    if not valor.strip().replace(" ", "").isalpha():
        return False, f"El campo {campo} solo debe contener letras y espacios."
    return True, ""


def numero_obligatorio(valor, campo):
    if not valor.strip():
        return False, f"El campo {campo} es obligatorio."
    if not valor.strip().isdigit():
        return False, f"El campo {campo} debe ser numerico."
    return True, ""


def correo_valido(valor):
    if not valor.strip():
        return False, "El campo Correo es obligatorio."
    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(patron, valor.strip()):
        return False, "El correo no tiene un formato valido."
    return True, ""


def fecha_valida(valor):
    if not valor.strip():
        return False, "La fecha de nacimiento es obligatoria."
    try:
        datetime.strptime(valor.strip(), "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "La fecha debe tener el formato YYYY-MM-DD."


def validar_cliente(nombre, identificacion, telefono, correo, fecha):
    for ok, mensaje in [
        texto_obligatorio(nombre, "Nombre"),
        numero_obligatorio(identificacion, "Identificacion"),
        numero_obligatorio(telefono, "Telefono"),
        correo_valido(correo),
        fecha_valida(fecha),
    ]:
        if not ok:
            return False, mensaje
    return True, ""


def validar_empleado(identificacion, nombre, telefono, cargo):
    for ok, mensaje in [
        numero_obligatorio(identificacion, "Identificacion"),
        texto_obligatorio(nombre, "Nombre"),
        numero_obligatorio(telefono, "Telefono"),
    ]:
        if not ok:
            return False, mensaje

    if not cargo.strip():
        return False, "El cargo es obligatorio."
    return True, ""


def validar_entrenador(identificacion, nombre, especialidad):
    for ok, mensaje in [
        numero_obligatorio(identificacion, "Identificacion"),
        texto_obligatorio(nombre, "Nombre"),
    ]:
        if not ok:
            return False, mensaje

    if not especialidad:
        return False, "Debe seleccionar una especialidad."
    return True, ""


def entero_positivo(valor, campo):
    try:
        numero = int(valor)
        if numero <= 0:
            raise ValueError
        return True, ""
    except ValueError:
        return False, f"El campo {campo} debe ser un numero entero positivo."


def decimal_positivo(valor, campo):
    try:
        numero = float(valor)
        if numero <= 0:
            raise ValueError
        return True, ""
    except ValueError:
        return False, f"El campo {campo} debe ser un numero positivo."


def fecha_iso_valida(valor, campo="Fecha"):
    try:
        datetime.strptime(valor.strip(), "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, f"{campo} debe tener el formato YYYY-MM-DD."

