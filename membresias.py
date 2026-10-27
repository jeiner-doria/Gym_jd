# membresias.py
# RF08 Registrar membresias
# RF09 Asignar membresia
# RF10 Consultar estado
# RF11 Renovar membresia
# RF12 Registrar pagos
# RF13 Consultar pagos
# RF14 Registrar ingreso

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date, datetime
import database
import validaciones


def sumar_meses(fecha, meses):
    mes = fecha.month - 1 + meses
    anio = fecha.year + mes // 12
    mes = mes % 12 + 1
    dias = [31, 29 if anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0) else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dia = min(fecha.day, dias[mes - 1])
    return date(anio, mes, dia)


class VentanaMembresias:
    def __init__(self, root):
        self.root = root
        self.root.title("Membresias, Pagos e Ingresos")
        self.root.geometry("1050x700")
        self.root.configure(bg="#ecf0f1")
        self.crear_interfaz()

    def crear_interfaz(self):
        principal = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        principal.pack(expand=True, fill="both")
        tk.Label(principal, text="MEMBRESIAS, PAGOS E INGRESOS",
                 font=("Segoe UI", 18, "bold"), fg="#1e3a5f",
                 bg="#ecf0f1").pack(pady=(0, 15))
        self.notebook = ttk.Notebook(principal)
        self.notebook.pack(expand=True, fill="both")
        self.crear_membresias()
        self.crear_asignacion()
        self.crear_estado()
        self.crear_pagos()
        self.crear_ingreso()

    def crear_membresias(self):
        frame = tk.Frame(self.notebook, bg="white", padx=20, pady=15)
        self.notebook.add(frame, text="RF08 Membresias")

        tk.Label(frame, text="Nombre:").grid(row=0, column=0, pady=8, sticky="w")
        self.nombre_membresia = tk.Entry(frame, width=30)
        self.nombre_membresia.grid(row=0, column=1, padx=10)
        tk.Label(frame, text="Duracion:").grid(row=1, column=0, pady=8, sticky="w")
        self.duracion = ttk.Combobox(
            frame, values=["Mensual", "Trimestral", "Anual"],
            state="readonly", width=27)
        self.duracion.current(0)
        self.duracion.grid(row=1, column=1, padx=10)
        tk.Label(frame, text="Precio:").grid(row=2, column=0, pady=8, sticky="w")
        self.precio = tk.Entry(frame, width=30)
        self.precio.grid(row=2, column=1, padx=10)
        tk.Button(frame, text="REGISTRAR MEMBRESIA", bg="#3498db", fg="white",
                  bd=0, width=24, command=self.registrar_membresia).grid(
                  row=3, column=0, columnspan=2, pady=15)

        self.tabla_membresias = ttk.Treeview(
            frame, columns=("ID", "Nombre", "Meses", "Precio"),
            show="headings", height=12)
        for col, ancho in zip(("ID", "Nombre", "Meses", "Precio"),
                              (50, 200, 100, 130)):
            self.tabla_membresias.heading(col, text=col)
            self.tabla_membresias.column(col, width=ancho, anchor="center")
        self.tabla_membresias.grid(row=4, column=0, columnspan=2, pady=10)
        self.cargar_membresias()

    def registrar_membresia(self):
        nombre = self.nombre_membresia.get().strip()
        precio = self.precio.get().strip()
        duraciones = {"Mensual": 1, "Trimestral": 3, "Anual": 12}
        ok, mensaje = validaciones.texto_obligatorio(nombre, "Nombre")
        if not ok:
            messagebox.showerror("Dato invalido", mensaje)
            return
        ok, mensaje = validaciones.decimal_positivo(precio, "Precio")
        if not ok:
            messagebox.showerror("Dato invalido", mensaje)
            return
        exito, mensaje = database.insertar_membresia(
            nombre, duraciones[self.duracion.get()], float(precio))
        if exito:
            messagebox.showinfo("Exito", mensaje)
            self.nombre_membresia.delete(0, tk.END)
            self.precio.delete(0, tk.END)
            self.cargar_membresias()
            self.cargar_combos()
        else:
            messagebox.showerror("Error", mensaje)

    def cargar_membresias(self):
        for item in self.tabla_membresias.get_children():
            self.tabla_membresias.delete(item)
        for fila in database.obtener_membresias():
            self.tabla_membresias.insert("", "end", values=fila)

    def obtener_cliente(self, identificacion):
        ok, mensaje = validaciones.numero_obligatorio(
            identificacion, "Identificacion")
        if not ok:
            messagebox.showerror("Dato invalido", mensaje)
            return None
        cliente = database.buscar_cliente(identificacion)
        if not cliente:
            messagebox.showerror("No encontrado",
                                 "No existe un cliente con esa identificacion.")
            return None
        return cliente

    def cargar_combos(self):
        membresias = database.obtener_membresias()
        self.membresias_cache = membresias
        self.membresias_renovar = membresias
        valores = [f"{m[0]} - {m[1]} (${m[3]:,.0f})" for m in membresias]
        self.combo_asignar["values"] = valores
        if hasattr(self, "combo_renovar"):
            self.combo_renovar["values"] = valores
        if valores:
            self.combo_asignar.current(0)
            if hasattr(self, "combo_renovar"):
                self.combo_renovar.current(0)

    def crear_asignacion(self):
        frame = tk.Frame(self.notebook, bg="white", padx=20, pady=15)
        self.notebook.add(frame, text="RF09 Asignar")
        tk.Label(frame, text="Identificacion del cliente:").grid(
            row=0, column=0, pady=10, sticky="w")
        self.id_asignar = tk.Entry(frame, width=30)
        self.id_asignar.grid(row=0, column=1, padx=10)
        tk.Label(frame, text="Membresia:").grid(
            row=1, column=0, pady=10, sticky="w")
        self.combo_asignar = ttk.Combobox(frame, state="readonly", width=27)
        self.combo_asignar.grid(row=1, column=1, padx=10)
        tk.Button(frame, text="ASIGNAR MEMBRESIA", bg="#3498db", fg="white",
                  bd=0, width=22, command=self.asignar).grid(
                  row=2, column=0, columnspan=2, pady=20)
        self.cargar_combos()

    def asignar(self):
        cliente = self.obtener_cliente(self.id_asignar.get().strip())
        indice = self.combo_asignar.current()
        if not cliente or indice < 0:
            messagebox.showerror("Dato invalido", "Seleccione una membresia.")
            return
        membresia = self.membresias_cache[indice]
        inicio = date.today()
        fin = sumar_meses(inicio, membresia[2])
        exito, mensaje = database.asignar_membresia(
            cliente[0], membresia[0], inicio.isoformat(), fin.isoformat())
        if exito:
            messagebox.showinfo("Exito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

    def crear_estado(self):
        frame = tk.Frame(self.notebook, bg="white", padx=20, pady=15)
        self.notebook.add(frame, text="RF10 Estado / RF11 Renovar")
        tk.Label(frame, text="Identificacion del cliente:").grid(
            row=0, column=0, pady=10, sticky="w")
        self.id_estado = tk.Entry(frame, width=30)
        self.id_estado.grid(row=0, column=1, padx=10)
        tk.Button(frame, text="CONSULTAR ESTADO", bg="#3498db", fg="white",
                  bd=0, command=self.consultar_estado).grid(row=0, column=2)
        self.estado_texto = tk.Text(frame, width=75, height=7, state="disabled")
        self.estado_texto.grid(row=1, column=0, columnspan=3, pady=20)
        tk.Label(frame, text="Membresia para renovar:").grid(
            row=2, column=0, sticky="w")
        self.combo_renovar = ttk.Combobox(frame, state="readonly", width=27)
        self.combo_renovar.grid(row=2, column=1, padx=10)
        tk.Button(frame, text="RENOVAR MEMBRESIA", bg="#27ae60", fg="white",
                  bd=0, width=22, command=self.renovar).grid(
                  row=3, column=0, columnspan=2, pady=15)
        self.cargar_combos()

    def consultar_estado(self):
        cliente = self.obtener_cliente(self.id_estado.get().strip())
        if not cliente:
            return
        membresia = database.obtener_membresia_cliente(cliente[0])
        self.estado_texto.config(state="normal")
        self.estado_texto.delete("1.0", tk.END)
        if not membresia:
            self.estado_texto.insert(
                tk.END, "El cliente no tiene una membresia registrada.")
        else:
            fin = datetime.strptime(membresia[5], "%Y-%m-%d").date()
            if fin < date.today():
                estado = "Vencida"
            elif (fin - date.today()).days <= 7:
                estado = "Proxima a vencer"
            else:
                estado = "Activa"
            self.estado_texto.insert(
                tk.END, f"Cliente: {cliente[2]}\n"
                         f"Membresia: {membresia[1]}\n"
                         f"Inicio: {membresia[4]}\n"
                         f"Vencimiento: {membresia[5]}\n"
                         f"Estado: {estado}")
        self.estado_texto.config(state="disabled")

    def renovar(self):
        cliente = self.obtener_cliente(self.id_estado.get().strip())
        indice = self.combo_renovar.current()
        if not cliente or indice < 0:
            messagebox.showerror("Dato invalido", "Seleccione una membresia.")
            return
        membresia = self.membresias_renovar[indice]
        inicio = date.today()
        fin = sumar_meses(inicio, membresia[2])
        exito, mensaje = database.renovar_membresia(
            cliente[0], membresia[0], inicio.isoformat(), fin.isoformat())
        if exito:
            messagebox.showinfo("Exito", mensaje)
            self.consultar_estado()
        else:
            messagebox.showerror("Error", mensaje)

    def crear_pagos(self):
        frame = tk.Frame(self.notebook, bg="white", padx=20, pady=15)
        self.notebook.add(frame, text="RF12-RF13 Pagos")
        tk.Label(frame, text="Identificacion del cliente:").grid(
            row=0, column=0, pady=8, sticky="w")
        self.id_pago = tk.Entry(frame, width=30)
        self.id_pago.grid(row=0, column=1, padx=10)
        tk.Label(frame, text="Valor del pago:").grid(
            row=1, column=0, pady=8, sticky="w")
        self.valor_pago = tk.Entry(frame, width=30)
        self.valor_pago.grid(row=1, column=1, padx=10)
        tk.Label(frame, text="Metodo:").grid(row=2, column=0, pady=8, sticky="w")
        self.metodo_pago = ttk.Combobox(
            frame, values=["Efectivo", "Tarjeta", "Transferencia"],
            state="readonly", width=27)
        self.metodo_pago.current(0)
        self.metodo_pago.grid(row=2, column=1, padx=10)
        tk.Button(frame, text="REGISTRAR PAGO", bg="#27ae60", fg="white",
                  bd=0, width=18, command=self.registrar_pago).grid(
                  row=3, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="CONSULTAR HISTORIAL", bg="#3498db", fg="white",
                  bd=0, width=22, command=self.consultar_pagos).grid(
                  row=4, column=0, columnspan=2, pady=8)
        self.tabla_pagos = ttk.Treeview(
            frame, columns=("ID", "Fecha", "Membresia", "Valor", "Metodo"),
            show="headings", height=10)
        for col, ancho in zip(
                ("ID", "Fecha", "Membresia", "Valor", "Metodo"),
                (50, 120, 180, 120, 150)):
            self.tabla_pagos.heading(col, text=col)
            self.tabla_pagos.column(col, width=ancho, anchor="center")
        self.tabla_pagos.grid(row=5, column=0, columnspan=2, pady=10)

    def registrar_pago(self):
        cliente = self.obtener_cliente(self.id_pago.get().strip())
        if not cliente:
            return
        membresia = database.obtener_membresia_cliente(cliente[0])
        if not membresia:
            messagebox.showerror(
                "Error", "El cliente debe tener una membresia antes de registrar un pago.")
            return
        valor = self.valor_pago.get().strip()
        ok, mensaje = validaciones.decimal_positivo(valor, "Valor del pago")
        if not ok:
            messagebox.showerror("Dato invalido", mensaje)
            return
        exito, mensaje = database.registrar_pago(
            cliente[0], membresia[7], date.today().isoformat(),
            float(valor), self.metodo_pago.get())
        if exito:
            messagebox.showinfo("Exito", mensaje)
            self.valor_pago.delete(0, tk.END)
            self.consultar_pagos()
        else:
            messagebox.showerror("Error", mensaje)

    def consultar_pagos(self):
        cliente = self.obtener_cliente(self.id_pago.get().strip())
        if not cliente:
            return
        for item in self.tabla_pagos.get_children():
            self.tabla_pagos.delete(item)
        for pago in database.obtener_pagos_cliente(cliente[0]):
            fila = (pago[0], pago[1], pago[2], f"${pago[3]:,.0f}", pago[4])
            self.tabla_pagos.insert("", "end", values=fila)

    def crear_ingreso(self):
        frame = tk.Frame(self.notebook, bg="white", padx=20, pady=15)
        self.notebook.add(frame, text="RF14 Ingreso")
        tk.Label(frame, text="Identificacion del cliente:").pack(pady=(30, 8))
        self.id_ingreso = tk.Entry(frame, width=35)
        self.id_ingreso.pack()
        tk.Button(frame, text="REGISTRAR INGRESO", bg="#3498db", fg="white",
                  font=("Segoe UI", 10, "bold"), bd=0, width=22,
                  command=self.registrar_ingreso).pack(pady=15)
        self.historial_ingresos = ttk.Treeview(
            frame, columns=("ID", "Fecha", "Hora"),
            show="headings", height=12)
        for col, ancho in zip(("ID", "Fecha", "Hora"), (80, 180, 180)):
            self.historial_ingresos.heading(col, text=col)
            self.historial_ingresos.column(col, width=ancho, anchor="center")
        self.historial_ingresos.pack(pady=10)

    def registrar_ingreso(self):
        cliente = self.obtener_cliente(self.id_ingreso.get().strip())
        if not cliente:
            return
        ahora = datetime.now()
        exito, mensaje = database.registrar_ingreso(
            cliente[0], ahora.date().isoformat(), ahora.strftime("%H:%M:%S"))
        if exito:
            messagebox.showinfo(
                "Ingreso registrado",
                f"Entrada de {cliente[2]} registrada a las {ahora.strftime('%H:%M:%S')}.")
            self.cargar_ingresos(cliente[0])
        else:
            messagebox.showerror("Error", mensaje)

    def cargar_ingresos(self, cliente_id):
        for item in self.historial_ingresos.get_children():
            self.historial_ingresos.delete(item)
        for ingreso in database.obtener_ingresos_cliente(cliente_id):
            self.historial_ingresos.insert("", "end", values=ingreso)

