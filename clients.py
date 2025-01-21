import tkinter as tk
from tkinter import ttk, messagebox
from database import obtenir_clients_particulars, obtenir_clients_empreses, actualitzar_clients_empreses, actualitzar_clients_particulars

def mostrar_seccio_clients(main_frame):

    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="Gestió de Clients", font=("Arial", 16, "bold"), bg="#f4f4f9").pack(pady=10)

    # Taula de clients particulars
    tk.Label(main_frame, text="Clients Particulars", font=("Arial", 12, "bold"), bg="#f4f4f9").pack(pady=5)

    particulars_frame = tk.Frame(main_frame)
    particulars_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columnes_particulars = (
        "ID", "Nom", "Cognoms", "DNI", "Email", "Telèfon",
        "Adreça", "Data Registre", "Actiu", "Comentaris"
    )
    particulars_tree = ttk.Treeview(particulars_frame, columns=columnes_particulars, show="headings",
                                    height=6)

    for col in columnes_particulars:
        particulars_tree.heading(col, text=col, anchor="center")
        particulars_tree.column(col, width=120, anchor="center")

    scrollbar_particulars_y = ttk.Scrollbar(particulars_frame, orient="vertical",
                                            command=particulars_tree.yview)

    particulars_tree.configure(yscrollcommand=scrollbar_particulars_y.set)
    scrollbar_particulars_y.pack(side="right", fill="y")
    particulars_tree.pack(fill="both", expand=True)

    scrollbar_particulars_x = ttk.Scrollbar(particulars_frame, orient="horizontal",
                                            command=particulars_tree.xview)
    particulars_tree.configure(xscrollcommand=scrollbar_particulars_x.set)
    scrollbar_particulars_x.pack(side="bottom", fill="x")

    def carregar_dades_particulars():
        particulars_tree.delete(*particulars_tree.get_children())
        clients_particulars = obtenir_clients_particulars()
        for persona in clients_particulars:
            particulars_tree.insert("", "end", values=(
                persona["id_client"], persona["nom"], persona["cognoms"], persona["dni"],
                persona["email"], persona["telefon"], persona["direccio"], persona["data_registre"],
                "Sí" if persona["actiu"] else "No", persona["comentaris"]
            ))

    carregar_dades_particulars()

    def obrir_finestra_edicio_particulars(event):
        seleccionat = particulars_tree.selection()
        if not seleccionat:
            return
        dades = particulars_tree.item(seleccionat[0], "values")
        client_id = dades[0]

        finestra_edicio = tk.Toplevel()
        finestra_edicio.title(f"Editar Client Particular ID: {client_id}")
        finestra_edicio.geometry("500x600")
        finestra_edicio.configure(bg="#e6f7ff")

        camps = ["Nom", "Cognoms", "DNI", "Email", "Telèfon", "Adreça","Data Registre", "Actiu", "Comentaris"]
        entrades = {}

        marc = tk.Frame(finestra_edicio, pady=10, padx=10, bg="#e6f7ff")
        marc.pack(fill="both", expand=True)

        for idx, camp in enumerate(camps):
            tk.Label(marc, text=camp, bg="#e6f7ff", font=("Arial", 10, "bold")).grid(row=idx, column=0, pady=5,
                                                                                     sticky="w")
            entrada = tk.Entry(marc, font=("Arial", 10))
            entrada.grid(row=idx, column=1, pady=5, padx=10, sticky="ew")
            entrada.insert(0, dades[idx + 1])
            entrades[camp] = entrada

        def guardar_canvis_particulars():
            valors = {camp: entrada.get() for camp, entrada in entrades.items()}
            valors["Actiu"] = 1 if valors["Actiu"].lower() in ["sí", "1", "true"] else 0

            actualitzar_clients_particulars(client_id, valors)
            messagebox.showinfo("Èxit", "Dades actualitzades correctament.")
            finestra_edicio.destroy()
            carregar_dades_particulars()

        tk.Button(finestra_edicio, text="Guardar Canvis", command=guardar_canvis_particulars, bg="#28a745", fg="white").pack(
            pady=10)

    particulars_tree.bind("<Double-1>", obrir_finestra_edicio_particulars)

    # Taula de clients empreses
    tk.Label(main_frame, text="Clients Empreses", font=("Arial", 12, "bold"), bg="#f4f4f9").pack(pady=5)

    empreses_frame = tk.Frame(main_frame)
    empreses_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columnes_empreses = (
        "ID", "Nom Empresa", "CIF", "Email Empresa", "Telèfon Empresa", "Direcció Empresa", "Data Registre",
        "Actiu", "Comentaris"
    )
    empreses_tree = ttk.Treeview(empreses_frame, columns=columnes_empreses, show="headings", height=6)

    for col in columnes_empreses:
        empreses_tree.heading(col, text=col, anchor="center")
        empreses_tree.column(col, width=120, anchor="center")

    scrollbar_empreses_y = ttk.Scrollbar(empreses_frame, orient="vertical", command=empreses_tree.yview)
    empreses_tree.configure(yscrollcommand=scrollbar_empreses_y.set)
    scrollbar_empreses_y.pack(side="right", fill="y")
    empreses_tree.pack(fill="both", expand=True)

    scrollbar_empreses_x = ttk.Scrollbar(empreses_frame, orient="horizontal", command=empreses_tree.xview)
    empreses_tree.configure(xscrollcommand=scrollbar_empreses_x.set)
    scrollbar_empreses_x.pack(side="bottom", fill="x")


    def carregar_dades_empreses():
        empreses_tree.delete(*empreses_tree.get_children())
        clients_empreses = obtenir_clients_empreses()
        for empresa in clients_empreses:
            empreses_tree.insert("", "end", values=(
                empresa["id_empresa"], empresa["nom_empresa"], empresa["cif"],
                empresa["email_empresa"], empresa["telefon_empresa"], empresa["direccio_empresa"],
                empresa["data_registre"], "Sí" if empresa["actiu"] else "No", empresa["comentaris"]
            ))

    carregar_dades_empreses()

    def obrir_finestra_edicio_empreses(event):
        seleccionat = empreses_tree.selection()
        if not seleccionat:
            return
        dades = empreses_tree.item(seleccionat[0], "values")
        empresa_id = dades[0]

        finestra_edicio = tk.Toplevel()
        finestra_edicio.title(f"Editar Empresa ID: {empresa_id}")
        finestra_edicio.geometry("500x600")
        finestra_edicio.configure(bg="#e6f7ff")

        camps = ["nom_empresa", "cif", "email_empresa", "telefon_empresa", "direccio_empresa","data_registre", "actiu", "comentaris"]
        entrades = {}

        marc = tk.Frame(finestra_edicio, pady=10, padx=10, bg="#e6f7ff")
        marc.pack(fill="both", expand=True)

        for idx, camp in enumerate(camps):
            tk.Label(marc, text=camp.capitalize(), bg="#e6f7ff", font=("Arial", 10, "bold")).grid(row=idx, column=0, pady=5,
                                                                                     sticky="w")
            entrada = tk.Entry(marc, font=("Arial", 10))
            entrada.grid(row=idx, column=1, pady=5, padx=10, sticky="ew")
            entrada.insert(0, dades[idx + 1])
            entrades[camp] = entrada

        def guardar_canvis_empreses():
            valors = {camp: entrada.get() for camp, entrada in entrades.items()}
            valors["actiu"] = 1 if valors["actiu"].lower() in ["sí", "1", "true"] else 0

            actualitzar_clients_empreses(empresa_id, valors)
            messagebox.showinfo("Èxit", "Dades actualitzades correctament.")
            finestra_edicio.destroy()
            carregar_dades_empreses()

        tk.Button(finestra_edicio, text="Guardar Canvis", command=guardar_canvis_empreses, bg="#28a745", fg="white").pack(
            pady=10)

    empreses_tree.bind("<Double-1>", obrir_finestra_edicio_empreses)
