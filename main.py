# main.py
import tkinter as tk
from tkinter import messagebox
import clientes
import empleados
import entrenadores
import membresias
import colores   # Importamos la paleta de colores

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestion de Gimnasio")
        self.root.geometry("650x650")
        self.root.resizable(False, False)
        self.root.configure(bg=colores.COLOR_FONDO)  # Fondo uniforme
        self.crear_interfaz()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def crear_interfaz(self):
        self.limpiar_ventana()
        principal = tk.Frame(self.root, bg=colores.COLOR_FONDO, padx=45, pady=30)
        principal.pack(expand=True, fill="both")

        tk.Label(principal, text="SISTEMA DE GESTION DE GIMNASIO",
                 font=("Segoe UI", 18, "bold"),
                 fg=colores.COLOR_TITULO, bg=colores.COLOR_FONDO).pack(pady=(0, 8))

        tk.Label(principal, text="Requerimientos funcionales RF01 - RF14",
                 font=("Segoe UI", 11),
                 fg=colores.COLOR_TEXTO, bg=colores.COLOR_FONDO).pack(pady=(0, 25))

        botones = [
            ("CLIENTES  | RF01-RF04", self.abrir_clientes),
            ("EMPLEADOS | RF05-RF06", self.abrir_empleados),
            ("ENTRENADORES | RF07", self.abrir_entrenadores),
            ("MEMBRESIAS / PAGOS / INGRESOS | RF08-RF14", self.abrir_membresias),
        ]

        for texto, comando in botones:
            tk.Button(principal, text=texto,
                      bg=colores.COLOR_BOTON_BG, fg=colores.COLOR_BOTON_FG,
                      font=("Segoe UI", 11, "bold"),
                      width=38, height=2, bd=0, cursor="hand2",
                      command=comando).pack(pady=8)

        tk.Frame(principal, height=2, bg=colores.COLOR_TITULO).pack(fill="x", pady=20)

        tk.Button(principal, text="SALIR",
                  bg=colores.COLOR_SALIR_BG, fg=colores.COLOR_SALIR_FG,
                  font=("Segoe UI", 11, "bold"),
                  width=20, bd=0,
                  command=self.salir).pack()

    def abrir_clientes(self):
        self.limpiar_ventana()
        clientes.VentanaClientes(self.root)

    def abrir_empleados(self):
        self.limpiar_ventana()
        empleados.VentanaEmpleados(self.root)

    def abrir_entrenadores(self):
        self.limpiar_ventana()
        entrenadores.VentanaEntrenadores(self.root)

    def abrir_membresias(self):
        self.limpiar_ventana()
        membresias.VentanaMembresias(self.root)

    def salir(self):
        if messagebox.askyesno("Confirmar salida", "¿Está seguro de que desea salir?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    VentanaPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()
