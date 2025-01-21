import mysql.connector
from tkinter import messagebox

def connectar_bbdd():
    """Connecta a la base de dades MySQL i retorna la connexió."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="crm",
            user="root",
            password="root")
        return connection
    except mysql.connector.Error as error:
        messagebox.showerror("Error de Connexió", f"No s'ha pogut connectar a la base de dades:\n{error}")
        return None

def obtenir_personal():
    connexio = connectar_bbdd()
    cursor = connexio.cursor(dictionary=True)
    cursor.execute("SELECT * FROM personal")
    personal = cursor.fetchall()
    connexio.close()
    return personal

def actualitzar_preferent(personal_id, preferent):
    connexio = connectar_bbdd()
    cursor = connexio.cursor(dictionary=True)
    query = "UPDATE personal SET preferent = %s WHERE id_personal = %s"
    cursor.execute(query, (1 if preferent else 0, personal_id))
    connexio.commit()
    connexio.close()


def guardar_canvis_personal(personal_id, valors):
    try:
        connexio = connectar_bbdd()
        cursor = connexio.cursor()

        query = """
        UPDATE personal
        SET nombre = %s, apellidos = %s, dni = %s, email = %s, telefono = %s,
            fecha_contratacion = %s, puesto = %s, salario = %s, departamento = %s,
            fecha_nacimiento = %s, activo = %s, preferent = %s
        WHERE id_personal = %s
        """

        data = (
            valors["Nom"], valors["Cognoms"], valors["DNI"], valors["Email"], valors["Telèfon"],
            valors["Data Contractació"], valors["Puesto"], valors["Salari"], valors["Departament"],
            valors["Data Naixement"], valors["Actiu"], valors["Preferent"], personal_id
        )

        cursor.execute(query, data)
        connexio.commit()
    finally:
        connexio.close()


def obtenir_clients_empreses():
    connexio = connectar_bbdd()
    cursor = connexio.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients_empreses")
    clients_empreses = cursor.fetchall()
    connexio.close()
    return clients_empreses

def obtenir_clients_particulars():
    connexio = connectar_bbdd()
    cursor = connexio.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients_particulars")
    clients_particulars = cursor.fetchall()
    connexio.close()
    return clients_particulars

def actualitzar_clients_empreses (id_empresa, valors):
    try:
        connexio = connectar_bbdd()
        cursor = connexio.cursor()

        query = """
        UPDATE clients_empreses
        SET nom_empresa = %s, cif = %s, email_empresa = %s, telefon_empresa = %s,
            direccio_empresa = %s, data_registre = %s, actiu = %s, comentaris = %s
        WHERE id_empresa = %s
        """

        data = (
            valors["nom_empresa"], valors["cif"], valors["email_empresa"], valors["telefon_empresa"],
            valors["direccio_empresa"], valors["data_registre"], valors["actiu"], valors["comentaris"], id_empresa
        )
        cursor.execute(query, data)
        connexio.commit()
    finally:
        connexio.close()

def actualitzar_clients_particulars(id_client, valors):
    try:
        connexio = connectar_bbdd()
        cursor = connexio.cursor()

        query = """
        UPDATE clients_particulars
        SET nom = %s, cognoms = %s, dni = %s, email = %s, telefon = %s,
            direccio = %s, data_registre = %s, actiu = %s, comentaris = %s
        WHERE id_client = %s
        """

        data = (
            valors["Nom"], valors["Cognoms"], valors["DNI"], valors["Email"],
            valors["Telèfon"], valors["Adreça"], valors["Data Registre"], valors["Actiu"],
            valors["Comentaris"],
            id_client
        )
        cursor.execute(query, data)

        connexio.commit()
    finally:
        connexio.close()

def obtenir_registre(actual_id, direccio):
    """
    Obté el registre anterior o següent basat en l'ID actual i la direcció.
    :param actual_id: ID del registre actual.
    :param direccio: 'anterior' o 'següent'.
    :return: Un diccionari amb el registre adjacent o None si no hi ha més registres.
    """
    connexio = connectar_bbdd()
    if connexio:
        cursor = connexio.cursor(dictionary=True)
        if direccio == "anterior":
            query = "SELECT * FROM personal WHERE id_personal < %s ORDER BY id_personal DESC LIMIT 1"
        elif direccio == "següent":
            query = "SELECT * FROM personal WHERE id_personal > %s ORDER BY id_personal ASC LIMIT 1"
        else:
            return None
        cursor.execute(query, (actual_id,))
        registre = cursor.fetchone()
        cursor.close()
        connexio.close()
        return registre
    return None

def obtenir_inventari():
    """Obté totes les dades de l'inventari."""
    connexio = connectar_bbdd()
    cursor = connexio.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventari")
    inventari = cursor.fetchall()
    connexio.close()
    return inventari

def obtenir_vendes_particulars():
    """Obté totes les dades de l'inventari."""
    connexio = connectar_bbdd()
    cursor = connexio.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vendes_particulars")
    inventari = cursor.fetchall()
    connexio.close()
    return vendes
