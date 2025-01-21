import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from database import obtenir_personal, connectar_bbdd, guardar_canvis_personal, obtenir_registre


def mostrar_seccio_personal(main_frame):
    """Funció per mostrar la secció de personal en el marc principal."""
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Títol de la secció
    tk.Label(main_frame, text="Gestió de Personal", font=("Arial", 16, "bold"), bg="#f4f4f9").pack(pady=10)

    # Marc del Treeview
    personal_frame = tk.Frame(main_frame)
    personal_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Definició de les columnes
    columnes = (
        "ID", "Nom", "Cognoms", "DNI", "Email", "Telèfon", "Data Contractació",
        "Puesto", "Salari", "Departament", "Data Naixement", "Actiu", "Preferent"
    )
    personal_tree = ttk.Treeview(personal_frame, columns=columnes, show="headings", height=15)

    for col in columnes:
        personal_tree.heading(col, text=col, anchor="center")
        personal_tree.column(col, width=120, anchor="center")

    # Barra de desplaçament
    scrollbar = ttk.Scrollbar(personal_frame, orient="vertical", command=personal_tree.yview)
    personal_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    personal_tree.pack(fill="both", expand=True)

    # Barra de desplaçament
    scrollbar = ttk.Scrollbar(personal_frame, orient="horizontal", command=personal_tree.xview)
    personal_tree.configure(xscrollcommand=scrollbar.set)
    scrollbar.pack(side="bottom", fill="x")
    personal_tree.pack(fill="both", expand=True)

    # Carrega les dades al Treeview
    def carregar_dades():
        personal_tree.delete(*personal_tree.get_children())
        personal = obtenir_personal()
        for persona in personal:
            personal_tree.insert("", "end", values=(
                persona["id_personal"], persona["nombre"], persona["apellidos"],
                persona["dni"], persona["email"], persona["telefono"],
                persona["fecha_contratacion"], persona["puesto"], persona["salario"],
                persona["departamento"], persona["fecha_nacimiento"],
                "Sí" if persona["activo"] else "No",
                "Si" if persona["preferent"] else "No"
            ))

    carregar_dades()

    # Finestra d'edició
    def obrir_finestra_edicio(event):
        seleccionat = personal_tree.selection()
        if not seleccionat:
            return
        dades = personal_tree.item(seleccionat[0], "values")
        personal_id = dades[0]

        # Crear la finestra emergent
        finestra_edicio = tk.Toplevel()
        finestra_edicio.title(f"Editar Personal ID: {personal_id}")
        finestra_edicio.geometry("500x750")
        finestra_edicio.configure(bg="#e6f7ff")

        # Marc per als camps d'entrada
        marc = tk.Frame(finestra_edicio, pady=10, padx=10, bg="#e6f7ff")
        marc.pack(fill="both", expand=True)

        camps = ["Nom", "Cognoms", "DNI", "Email", "Telèfon", "Data Contractació",
                 "Puesto", "Salari", "Departament", "Data Naixement","Data Registre", "Actiu"]
        entrades = {}

        for idx, camp in enumerate(camps):
            tk.Label(marc, text=camp, bg="#e6f7ff", font=("Arial", 10, "bold")).grid(row=idx, column=0, pady=5,
                                                                                     sticky="w")
            entrada = tk.Entry(marc, font=("Arial", 10))
            entrada.grid(row=idx, column=1, pady=5, padx=10, sticky="ew")
            entrada.insert(0, dades[idx + 1])
            entrades[camp] = entrada

        # Checkbox per al camp "Preferent"
        preferent_var = tk.BooleanVar()
        tk.Label(marc, text="Preferent", bg="#e6f7ff", font=("Arial", 10, "bold")).grid(row=len(camps), column=0, pady=5, sticky="w")
        preferent_checkbox = tk.Checkbutton(marc, variable=preferent_var, bg="#e6f7ff")
        preferent_checkbox.grid(row=len(camps), column=1, pady=5, padx=10, sticky="w")

        # Marc per la foto
        foto_marc = tk.Frame(finestra_edicio, bg="#e6f7ff", pady=10)
        foto_marc.pack(fill="x")
        tk.Label(foto_marc, text="Foto", bg="#e6f7ff", font=("Arial", 10, "bold")).pack()

        foto_path = tk.StringVar()
        foto_label = tk.Label(foto_marc)
        foto_label.pack()

        def carregar_foto():
            arxiu = filedialog.askopenfilename(filetypes=[("Imatges", "*.png;*.jpg;*.jpeg")])
            if arxiu:
                foto_path.set(arxiu)
                imatge = Image.open(arxiu)
                imatge.thumbnail((150, 150))
                foto = ImageTk.PhotoImage(imatge)
                foto_label.config(image=foto)
                foto_label.image = foto

        tk.Button(foto_marc, text="Carregar Foto", command=carregar_foto, bg="#007bff", fg="white").pack(pady=5)

        # Funció per carregar el registre anterior i següent
        def carregar_registre(id_actual, moviment="actual"):
            registre = obtenir_registre(id_actual, moviment)
            if registre:
                nonlocal personal_id
                personal_id = registre["id_personal"]
                camps = {
                    "Nom": "nombre",
                    "Cognoms": "apellidos",
                    "DNI": "dni",
                    "Email": "email",
                    "Telèfon": "telefono",
                    "Data Contractació": "fecha_contratacion",
                    "Puesto": "puesto",
                    "Salari": "salario",
                    "Departament": "departamento",
                    "Data Naixement": "fecha_nacimiento",
                    "Actiu": "activo"
                }
                for camp, entrada in entrades.items():
                    valor = registre.get(camps.get(camp, ""),"")
                    entrada.delete(0, "end")
                    entrada.insert(0, valor if valor is not None else "")
                btn_anterior.config(state="normal")
                btn_seguent.config(state="normal")
            else:
                if moviment == "anterior":
                    btn_anterior.config(state="disabled")
                elif moviment == "seguent":
                    btn_seguent.config(state="disabled")

        # Funcions per gestionar els botons
        navegacio_frame = tk.Frame(finestra_edicio, bg="#e6f7ff")
        navegacio_frame.pack(pady=10)

        btn_anterior = tk.Button(navegacio_frame, text="Anterior", bg="#ffc107", fg="black",
                                 command=lambda: carregar_registre(personal_id, "anterior"))
        btn_anterior.pack(side="left", padx=10)

        btn_seguent = tk.Button(navegacio_frame, text="Següent", bg="#007bff", fg="white",
                                command=lambda: carregar_registre(personal_id, "següent"))
        btn_seguent.pack(side="right", padx=10)

        # Guardar canvis
        def guardar_canvis():
            valors = {camp: entrada.get() for camp, entrada in entrades.items()}
            valors["Actiu"] = 1 if valors["Actiu"].lower() in ["sí", "1", "true", "actiu"] else 0
            valors["Foto"] = foto_path.get()
            valors["Preferent"] = 1 if preferent_var.get() else 0

            # Crida a la funció del fitxer 'database.py'
            guardar_canvis_personal(personal_id, valors)
            messagebox.showinfo("Èxit", "Dades actualitzades correctament.")
            finestra_edicio.destroy()
            carregar_dades()

        tk.Button(finestra_edicio, text="Guardar Canvis", command=guardar_canvis, bg="#28a745", fg="white").pack(
            pady=10)

    # Vincular doble clic al Treeview
    personal_tree.bind("<Double-1>", obrir_finestra_edicio)

    # Botó de refresc
    btn_refrescar = tk.Button(main_frame, text="Refrescar llista", command=carregar_dades, bg="#17a2b8", fg="white")
    btn_refrescar.pack(pady=10)
