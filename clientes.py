# clientes.py
import tkinter as tk
from tkinter import messagebox, ttk
import database
import validaciones
import colores   # Importamos la paleta de colores
import main      # Para volver al menú principal

class VentanaClientes:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Clientes")
        self.root.geometry("950x650")
        self.root.configure(bg=colores.COLOR_FONDO)

        for widget in self.root.winfo_children():
            widget.destroy()

        self.cliente_seleccionado_id = None
        self.crear_interfaz()
        self.cargar_lista_clientes()

    def crear_interfaz(self):
        # Frame principal como atributo de la clase
        self.principal = tk.Frame(self.root, bg=colores.COLOR_FONDO, padx=20, pady=20)
        self.principal.pack(expand=True, fill="both")

        tk.Label(self.principal, text="GESTIÓN DE CLIENTES",
                 font=("Segoe UI", 18, "bold"),
                 fg=colores.COLOR_TITULO, bg=colores.COLOR_FONDO).pack(pady=(0, 15))

        # Notebook con pestañas
        self.notebook = ttk.Notebook(self.principal)
        self.notebook.pack(expand=True, fill="both")

        self.crear_registro()
        self.crear_consulta()
        self.crear_lista()

        # Botón para volver al menú principal
        tk.Button(self.principal, text="VOLVER AL MENÚ",
                  bg=colores.COLOR_BOTON_BG, fg=colores.COLOR_BOTON_FG,
                  font=("Segoe UI", 11, "bold"), width=20, bd=0,
                  command=self.volver_menu).pack(pady=15)

    def crear_registro(self):
        frame = tk.Frame(self.notebook, bg=colores.COLOR_FONDO, padx=25, pady=20)
        self.notebook.add(frame, text="Registrar")

        campos = [
            ("Nombre:", "nombre"),
            ("Identificación:", "identificacion"),
            ("Teléfono:", "telefono"),
            ("Correo:", "correo"),
            ("Fecha nacimiento (YYYY-MM-DD):", "fecha")
        ]
        self.entries_registro = {}

        for fila, (texto, clave) in enumerate(campos):
            tk.Label(frame, text=texto, bg=colores.COLOR_FONDO, fg=colores.COLOR_TEXTO,
                     font=("Segoe UI", 10)).grid(row=fila, column=0, sticky="w", pady=9)
            entrada = tk.Entry(frame, width=38, font=("Segoe UI", 10),
                               bg=colores.COLOR_ENTRADA_BG, fg=colores.COLOR_ENTRADA_FG)
            entrada.grid(row=fila, column=1, padx=15, pady=9)
            self.entries_registro[clave] = entrada

        tk.Button(frame, text="GUARDAR CLIENTE",
                  bg=colores.COLOR_BOTON_BG, fg=colores.COLOR_BOTON_FG,
                  font=("Segoe UI", 10, "bold"), width=22, bd=0,
                  command=self.guardar_cliente).grid(row=5, column=0, columnspan=2, pady=20)
    def crear_consulta(self):
        frame = tk.Frame(self.notebook, bg=colores.COLOR_FONDO, padx=25, pady=20)
        self.notebook.add(frame, text="Consultar / Modificar / Eliminar")

        tk.Label(frame, text="Identificación:", bg=colores.COLOR_FONDO, fg=colores.COLOR_TEXTO,
                 font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=9)
        self.entry_consulta = tk.Entry(frame, width=30, font=("Segoe UI", 10),
                                       bg=colores.COLOR_ENTRADA_BG, fg=colores.COLOR_ENTRADA_FG)
        self.entry_consulta.grid(row=0, column=1, padx=15, pady=9)

        tk.Button(frame, text="CONSULTAR", bg=colores.COLOR_BOTON_BG, fg=colores.COLOR_BOTON_FG,
                  font=("Segoe UI", 10, "bold"), width=15, bd=0,
                  command=self.consultar_cliente).grid(row=0, column=2, padx=10)

    def crear_lista(self):
        frame = tk.Frame(self.notebook, bg=colores.COLOR_FONDO, padx=25, pady=20)
        self.notebook.add(frame, text="Lista de Clientes")

        columnas = ("ID", "Nombre", "Identificación", "Teléfono", "Correo", "Fecha Nacimiento")
        self.tree = ttk.Treeview(frame, columns=columnas, show="headings", height=15)

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(expand=True, fill="both", pady=10)

    def cargar_lista_clientes(self):
        # Aquí llamas a tu base de datos y llenas el Treeview
        pass

    def guardar_cliente(self):
        datos = {clave: entrada.get().strip() for clave, entrada in self.entries_registro.items()}
        # Aquí validas y guardas en la base de datos
        messagebox.showinfo("Cliente guardado", f"Cliente {datos['nombre']} registrado correctamente.")

    def volver_menu(self):
        # Limpia la ventana y regresa al menú principal
        for widget in self.root.winfo_children():
            widget.destroy()
        main.VentanaPrincipal(self.root)
