# Sistema de Gestion de Gimnasio - RF01 a RF14

Proyecto basado en el Gym.zip original, reorganizado y ampliado.

## Requerimientos implementados

1. Registrar clientes.
2. Consultar clientes por identificacion.
3. Modificar datos del cliente.
4. Eliminar clientes. Incluye boton independiente "ELIMINAR CLIENTE".
5. Registrar empleados.
6. Consultar empleados.
7. Registrar entrenadores y asociar especialidad.
8. Registrar membresias mensual, trimestral y anual.
9. Asignar una membresia a un cliente.
10. Consultar estado: Activa, Proxima a vencer o Vencida.
11. Renovar membresia.
12. Registrar pagos.
13. Consultar historial de pagos por cliente.
14. Registrar ingreso al gimnasio con fecha y hora.

## Validaciones agregadas

- Identificacion: solo numeros.
- Telefono: solo numeros.
- Nombre: letras y espacios.
- Correo: formato de correo valido.
- Fecha de nacimiento: YYYY-MM-DD.
- Precio y valor de pago: numeros positivos.
- Duracion: se selecciona desde una lista.
- Los campos obligatorios no pueden quedar vacios.
- Las identificaciones repetidas son rechazadas por la base de datos.

Cuando el usuario escribe un tipo de dato incorrecto, aparece un mensaje
" Dato invalido " y la operacion no continua.

## Archivos

- main.py
- database.py
- validaciones.py
- clientes.py
- empleados.py
- entrenadores.py
- membresias.py
- requirements.txt

Solo se utilizan tkinter y sqlite3, incluidas con Python.
