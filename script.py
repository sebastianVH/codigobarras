import tkinter as tk
from tkinter import messagebox, ttk
from conexiondb import dbini, construir_diccionario

from dictejemplo import dict_ejemplo

root = tk.Tk()
root.withdraw()

while True:
    try:
        #rows = dbini()
        diccionario = dict_ejemplo
        break
    except Exception as e:
        print("Error al conectar a SQL Server", e)
        break

cargados = list() #Esta lista almacena todos los que se vayan cargando

def is_lote_in_codigo(diccionario, order_number, lot_number):
    """Check if a lote is in a dictionary of orden numbers and lots."""
    return (
        order_number in diccionario
        and lot_number in diccionario[order_number]
    )

def cargar():
    # Verificamos que el código no esté vacío
    nro_orden_viaje = combo_ordenes.get()
    lote = entry_codigo.get()
    if lote is None or lote == "":
        messagebox.showerror("Error", "Por favor, introduce un código")
        return
    # Verificamos que el código no haya sido cargado antes
    if lote in cargados:
        messagebox.showerror("Error", "Este código ya ha sido cargado")
        return
    # Verificamos que el código exista en el archivo
    try:
        if is_lote_in_codigo(diccionario, nro_orden_viaje, int(lote)):
            # Si la función devuelve True, cambia el color de fondo a verde
            resultado = "Cargado en el listado"
            label_resultado.config(text=resultado, bg="green")
            tree.insert("", "end", values=(lote, resultado))
            cargados.append(lote)
        else:
            # Si la función devuelve False, cambia el color de fondo a rojo y muestra una alerta
            label_resultado.config(text="Artículo no encontrado", bg="red")
            messagebox.showerror("Error", "Este artículo no está en el lote")
    except Exception as e:
        # Si ocurre algún error, muestra una alerta con la excepción
        messagebox.showerror("Error", str(e))
    finally:
        # Limpiamos el campo de código al finalizar
        entry_codigo.delete(0, "end")

def limpiar():
    if messagebox.askyesno("Limpiar", "¿Está seguro que desea borrar los datos?"):
        # Si el usuario confirma, borrar todas las filas del Treeview
        for child in tree.get_children():
            tree.delete(child)

def salir():
    if messagebox.askyesno("Salir", "¿Está seguro que desea cerrar el programa?"):
        # Si el usuario confirma, cerrar la aplicación
        root.destroy()

# Crear ventana principal
root = tk.Tk()
root.title("Búsqueda de Código")
root.geometry("500x500")

# Crear campo para introducir el código
label_codigo = tk.Label(root, text="Código:")
label_codigo.pack()
entry_codigo = tk.Entry(root)
entry_codigo.pack()

# Selector de número de orden
label_orden = tk.Label(root, text="Número de Orden de Viaje")
label_orden.pack()
combo_ordenes = ttk.Combobox(root, values=list(diccionario.keys()))
combo_ordenes.pack()

# Crear botón "Cargar" que ejecutará la función buscarCodigo
button_cargar = tk.Button(root, text="Cargar", command=cargar)
button_cargar.pack()

# Crear etiqueta para mostrar el resultado
label_resultado = tk.Label(root, text="", bg="white")
label_resultado.pack(fill=tk.X)
tree = ttk.Treeview(root, columns=("Código", "Resultado"), show="headings")
tree.heading("Código", text="Código")
tree.heading("Resultado", text="Resultado")
tree.pack(fill="both", expand=True)
# Ejecutar el bucle principal de la aplicación

# Crear menú
menu = tk.Menu(root)
root.config(menu=menu)

# Menú Opciones
menu_opciones = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Opciones", menu=menu_opciones)
menu_opciones.add_command(label="Limpiar", command=limpiar)
menu_opciones.add_command(label="Salir", command=salir)

root.mainloop()
