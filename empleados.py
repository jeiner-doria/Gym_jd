# empleados.py
# RF05 Registrar empleados
# RF06 Consultar empleados

import tkinter as tk
from tkinter import messagebox, ttk
import database
import validaciones


class VentanaEmpleados:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Empleados")
        self.root.geometry("780x570")
        self.root.configure(bg="#ecf0f1")
        self.crear_interfaz()
        self.cargar_lista()

    def crear_interfaz(self):
        principal = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        principal.pack(expand=True, fill="both")
        tk.Label(principal, text="GESTION DE EMPLEADOS",
                 font=("Segoe UI", 18, "bold"), fg="#1e3a5f",
                 bg="#ecf0f1").pack(pady=(0, 15))
        self.notebook = ttk.Notebook(principal)
        self.notebook.pack(expand=True, fill="both")
        self.crear_registro()
        self.crear_consulta()
        self.crear_lista()

    def crear_registro(self):
        frame = tk.Frame(self.notebook, bg="white", padx=25, pady=20)
        self.notebook.add(frame, text="Registrar")
        campos = [
            ("Identificacion:", "identificacion"),
            ("Nombre:", "nombre"),
            ("Telefono:", "telefono"),
            ("Cargo:", "cargo")
        ]
        self.entries = {}
        for fila, (texto, clave) in enumerate(campos):
            tk.Label(frame, text=texto, bg="white").grid(
                row=fila, column=0, sticky="w", pady=10)
            entrada = tk.Entry(frame, width=38)
            entrada.grid(row=fila, column=1, padx=15, pady=10)
            self.entries[clave] = entrada

        tk.Button(frame, text="GUARDAR EMPLEADO", bg="#2ecc71",
                  fg="white", bd=0, width=22,
                  command=self.guardar).grid(
                  row=4, column=0, columnspan=2, pady=20)

    def guardar(self):
        datos = {k: e.get().strip() for k, e in self.entries.items()}
        ok, mensaje = validaciones.validar_empleado(
            datos["identificacion"], datos["nombre"],
            datos["telefono"], datos["cargo"]
        )
        if not ok:
            messagebox.showerror("Dato invalido", mensaje)
            return

        exito, mensaje = database.insertar_empleado(
            datos["identificacion"], datos["nombre"],
            datos["telefono"], datos["cargo"]
        )
        if exito:
            messagebox.showinfo("Exito", mensaje)
            for e in self.entries.values():
                e.delete(0, tk.END)
            self.cargar_lista()
        else:
            messagebox.showerror("Error", mensaje)

    def crear_consulta(self):
        frame = tk.Frame(self.notebook, bg="white", padx=25, pady=20)
        self.notebook.add(frame, text="Consultar")
        tk.Label(frame, text="Identificacion:").grid(
            row=0, column=0, sticky="w", pady=10)
        self.buscar = tk.Entry(frame, width=32)
        self.buscar.grid(row=0, column=1, padx=10)
        tk.Button(frame, text="BUSCAR", bg="#2ecc71", fg="white",
                  bd=0, command=self.consultar).grid(row=0, column=2)

        self.resultado = tk.Text(frame, width=60, height=8, state="disabled")
        self.resultado.grid(row=1, column=0, columnspan=3, pady=25)

    def consultar(self):
        identificacion = self.buscar.get().strip()
        ok, mensaje = validaciones.numero_obligatorio(
            identificacion, "Identificacion")
        if not ok:
            messagebox.showerror("Dato invalido", mensaje)
            return
        empleado = database.buscar_empleado(identificacion)
        self.resultado.config(state="normal")
        self.resultado.delete("1.0", tk.END)
        if empleado:
            self.resultado.insert(
                tk.END,
                f"Identificacion: {empleado[1]}\n"
                f"Nombre: {empleado[2]}\n"
                f"Telefono: {empleado[3]}\n"
                f"Cargo: {empleado[4]}"
            )
        else:
            self.resultado.insert(tk.END, "Empleado no encontrado.")
        self.resultado.config(state="disabled")

    def crear_lista(self):
        frame = tk.Frame(self.notebook, bg="white", padx=15, pady=15)
        self.notebook.add(frame, text="Lista de Empleados")
        self.tabla = ttk.Treeview(
            frame, columns=("ID", "Identificacion", "Nombre", "Telefono", "Cargo"),
            show="headings", height=16)
        for columna, ancho in zip(
            ("ID", "Identificacion", "Nombre", "Telefono", "Cargo"),
            (40, 120, 180, 120, 180)
        ):
            self.tabla.heading(columna, text=columna)
            self.tabla.column(columna, width=ancho, anchor="center")
        self.tabla.pack(expand=True, fill="both")
        tk.Button(frame, text="ACTUALIZAR LISTA", bg="#2ecc71",
                  fg="white", bd=0, command=self.cargar_lista).pack(pady=10)

    def cargar_lista(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for empleado in database.obtener_todos_empleados():
            self.tabla.insert("", "end", values=empleado)

