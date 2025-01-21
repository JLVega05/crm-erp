import tkinter as tk

from clients import mostrar_seccio_clients
from inventari import mostrar_seccio_inventari
from personal import mostrar_seccio_personal
from vendes import mostrar_seccio_vendes
from vendesparticulars import mostrar_seccio_vendesparticulars

# Configuració de la finestra principal
root = tk.Tk()
root.title("CRM/ERP - Gestió Empresarial")
root.geometry("1000x600")
root.configure(bg="#e0e0e0")

# Barra de navegació
sidebar = tk.Frame(root, width=200, bg="#343a40", relief="sunken", borderwidth=2)
sidebar.pack(expand=False, fill="y", side="left", anchor="nw")

# Botons de navegació
seccions = ["Inici", "Gestió de Vendes", "Personal", "Clients", "Informes", "Inventari"]
for section in seccions:
    btn = tk.Button(
        sidebar, text=section, bg="#495057", fg="white", relief="flat",
        font=("Arial", 10), activebackground="#6c757d", activeforeground="white",
        command=lambda sec=section: mostrar_seccio(sec)
    )
    btn.pack(fill="x", pady=5)

# Marc principal per al contingut dinàmic
main_frame = tk.Frame(root, bg="#f4f4f9")
main_frame.pack(expand=True, fill="both", side="right")

# Funció per canviar entre seccions
def mostrar_seccio(seccio):
    """Mostra la secció seleccionada en el marc principal."""
    if seccio == "Inici":
        mostrar_inici()
    elif seccio == "Gestió de Vendes":
        mostrar_seccio_vendes(main_frame)
    elif seccio == "Personal":
        mostrar_seccio_personal(main_frame)
    elif seccio == "Clients":
        mostrar_seccio_clients(main_frame)
    elif seccio == "Inventari":
        mostrar_seccio_inventari(main_frame)

# Funció per mostrar la pantalla d'inici
def mostrar_inici():
    for widget in main_frame.winfo_children():
        widget.destroy()
    tk.Label(main_frame, text="Benvingut al CRM/ERP", font=("Arial", 16, "bold")).pack(pady=20)

# Mostra la pantalla d'inici en arrencar el programa
mostrar_inici()
root.mainloop()
