import tkinter as tk
from tkinter import ttk
from database import obtenir_inventari

def mostrar_seccio_inventari(main_frame):
    """Mostra una finestra de només lectura per consultar l'inventari amb ordenació."""
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Configuració de l'encapçalñament
    header_frame = tk.Frame(main_frame, bg="#2C3E50", padx=10, pady=10)
    header_frame.pack(fill="x")
    tk.Label(
        header_frame, text="Gestió d'Inventari", fg="white", bg="#2C3E50",
        font=("Helvetica", 20, "bold")
    ).pack()

    # Creació del marc principal
    inventari_frame = tk.Frame(main_frame, padx=10, pady=10)
    inventari_frame.pack(fill="both", expand=True)

    # Scrollbars horitzontal i vertical
    scrollbar_vertical = ttk.Scrollbar(inventari_frame, orient="vertical")
    scrollbar_horizontal = ttk.Scrollbar(inventari_frame, orient="horizontal")
    scrollbar_vertical.pack(side="right", fill="y")
    scrollbar_horizontal.pack(side="bottom", fill="x")

    # Taula de només lectura
    columnes = ("ID", "Nom del Producte", "Descripció", "Categoria", "Preu", "Quantitat", "Estoc Mínim")
    tree = ttk.Treeview(
        inventari_frame, columns=columnes, show="headings",
        yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set
    )

    # Configuració dels encapçalaments
    for col in columnes:
        tree.heading(col, text=col, anchor="center", command=lambda c=col: ordenar_columnes(tree, c, False))
        tree.column(col, anchor="center", width=150)

    tree.pack(fill="both", expand=True)
    scrollbar_vertical.config(command=tree.yview)
    scrollbar_horizontal.config(command=tree.xview)

    # Funció per carregar les dades
    def carregar_dades():
        """Carrega els productes de la base de dades amb colors alternats i text canviant."""
        tree.delete(*tree.get_children())  # Netejar la taula abans de carregar
        dades = obtenir_inventari()

        for i, producte in enumerate(dades):
            color_fila = "#f2f2f2" if i % 2 == 0 else "#e6e6e6"  # Colors alternats
            color_text = "black" if i % 2 == 0 else "blue"  # Canvi de color del text
            tree.insert(
                "", "end", values=(
                    producte['id'], producte['nom_producte'], producte['descripcio'],
                    producte['categoria'], f"{producte['preu']} €", producte['quantitat'],
                    producte['estoc_minim']
                ),
                tags=("oddrow" if i % 2 == 0 else "evenrow",)
            )

        # Configuració de colors per a les etiquetes
        tree.tag_configure("oddrow", background="#f2f2f2", foreground="black", font=("Helvetica", 10, "bold"))
        tree.tag_configure("evenrow", background="#e6e6e6", foreground="blue", font=("Helvetica", 10, "bold"))

    # Funció per ordenar les columnes
    def ordenar_columnes(treeview, col, descendent):
        """Ordena les dades del Treeview per la columna seleccionada."""
        dades = [(treeview.set(child, col), child) for child in treeview.get_children("")]
        try:
            dades.sort(reverse=descendent, key=lambda x: float(x[0].replace("€", "").replace(",", ".")))
        except ValueError:
            dades.sort(reverse=descendent)

        for index, (_, child) in enumerate(dades):
            treeview.move(child, "", index)

        # Actualitza la funció de l'encapçalament per alternar ascendent/descendent
        treeview.heading(col, command=lambda: ordenar_columnes(treeview, col, not descendent))

    # Crida inicial per carregar les dades
    carregar_dades()

    # Peu de pàgina informatiu
    footer_frame = tk.Frame(main_frame, bg="#f4f4f4", padx=10, pady=5)
    footer_frame.pack(fill="x")
    tk.Label(
        footer_frame, text="Llista de productes disponibles. Mode consulta.",
        font=("Helvetica", 10), bg="#f4f4f4", fg="#7f8c8d"
    ).pack()
