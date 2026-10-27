# entrenadores.py
# RF07 Registrar entrenadores y asociarlos con una especialidad.

import tkinter as tk
from tkinter import messagebox, ttk
import database
import validaciones

ESPECIALIDADES = [
    "Musculacion", "Cardio", "Yoga", "Boxeo", "Rumba",
    "Entrenamiento funcional"
]


class VentanaEntrenadores:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Entrenadores")
        self.root.geometry("780x570")
        self.root.configure(bg="#ecf0f1")
        self.crear_interfaz()
        self.cargar_lista()

    def crear_interfaz(self):
        principal = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        principal.pack(expand=True, fill="both")
        tk.Label(principal, text="GESTION DE ENTRENADORES",
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
        tk.Label(frame, text="Identificacion:").grid(row=0, column=0, sticky="w", pady=10)
        self.identificacion = tk.Entry(frame, width=38)
        self.identificacion.grid(row=0, column=1, padx=15, pady=10)

        tk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=10)
        self.nombre = tk.Entry(frame, width=38)
        self.nombre.grid(row=1, column=1, padx=15, pady=10)

        tk.Label(frame, text="Especialidad:").grid(row=2, column=0, sticky="w", pady=10)
        self.especialidad = ttk.Combobox(
            frame, values=ESPECIALIDADES, state="readonly", width=35)
        self.especialidad.current(0)
        self.especialidad.grid(row=2, column=1, padx=15, pady=10)

        tk.Button(frame, text="GUARDAR ENTRENADOR", bg="#e67e22",
                  fg="white", bd=0, width=22,
                  command=self.guardar).grid(row=3, column=0,
                  columnspan=2, pady=20)

    def guardar(self):
        ok, mensaje = validaciones.validar_entrenador(
            self.identificacion.get(), self.nombre.get(),
            self.especialidad.get())
        if not ok:
            messagebox.showerror("Dato invalido", mensaje)
            return

        exito, mensaje = database.insertar_entrenador(
            self.identificacion.get().strip(),
            self.nombre.get().strip(),
            self.especialidad.get())
        if exito:
            messagebox.showinfo("Exito", mensaje)
            self.identificacion.delete(0, tk.END)
            self.nombre.delete(0, tk.END)
            self.cargar_lista()
        else:
            messagebox.showerror("Error", mensaje)

    def crear_consulta(self):
        frame = tk.Frame(self.notebook, bg="white", padx=25, pady=20)
        self.notebook.add(frame, text="Consultar")
        tk.Label(frame, text="Identificacion:").grid(row=0, column=0, pady=10)
        self.buscar = tk.Entry(frame, width=32)
        self.buscar.grid(row=0, column=1, padx=10)
        tk.Button(frame, text="BUSCAR", bg="#e67e22", fg="white",
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
        entrenador = database.buscar_entrenador(identificacion)
        self.resultado.config(state="normal")
        self.resultado.delete("1.0", tk.END)
        if entrenador:
            self.resultado.insert(
                tk.END,
                f"Identificacion: {entrenador[1]}\n"
                f"Nombre: {entrenador[2]}\n"
                f"Especialidad: {entrenador[3]}"
            )
        else:
            self.resultado.insert(tk.END, "Entrenador no encontrado.")
        self.resultado.config(state="disabled")

    def crear_lista(self):
        frame = tk.Frame(self.notebook, bg="white", padx=15, pady=15)
        self.notebook.add(frame, text="Lista de Entrenadores")
        self.tabla = ttk.Treeview(
            frame, columns=("ID", "Identificacion", "Nombre", "Especialidad"),
            show="headings", height=16)
        for columna, ancho in zip(
            ("ID", "Identificacion", "Nombre", "Especialidad"),
            (40, 120, 180, 220)
        ):
            self.tabla.heading(columna, text=columna)
            self.tabla.column(columna, width=ancho, anchor="center")
        self.tabla.pack(expand=True, fill="both")
        tk.Button(frame, text="ACTUALIZAR LISTA", bg="#e67e22",
                  fg="white", bd=0, command=self.cargar_lista).pack(pady=10)

    def cargar_lista(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for entrenador in database.obtener_todos_entrenadores():
            self.tabla.insert("", "end", values=entrenador)

