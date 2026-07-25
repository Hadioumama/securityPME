import mysql.connector
from mysql.connector import Error
import bcrypt
CONFIG_DB={
    "host":"127.0.0.1",
    "port":3307,
    "user":"root",
    "password":"",
    "database":"security_pme"
}
def connecter():
    try:
        connexion = mysql.connector.connect(**CONFIG_DB)
        return connexion
    except Error as e:
        print(f"Erreur de connexion à MySQL : {e}")
        try:
            import streamlit as st
            st.error(f"🔴 Erreur MySQL détaillée : {e}")
        except Exception:
            pass
        return None

def hacher_mot_de_passe(mot_de_passe):
    sel=bcrypt.gensalt()
    hash_bytes=bcrypt.hashpw(mot_de_passe.encode("utf-8"),sel)
    return hash_bytes.decode("utf-8")



def verifier_mot_de_passe(mot_de_passe_saisi,hash_stocke):
    return bcrypt.checkpw(mot_de_passe_saisi.encode("utf-8"), hash_stocke.encode("utf-8"))

def inscrire_pme(nom,email,mot_de_passe,secteur="",ville=""):
    connexion=connecter()
    if connexion is None:
        return False,"impossible de se connecter a la base de donnée",None
    try:
        curseur=connexion.cursor()
        curseur.execute("SELECT id FROM pme WHERE email=%s",(email,))
        if curseur.fetchone():
            return False,"un compte existe deja avec cet email",None
        mot_de_passe_hash=hacher_mot_de_passe(mot_de_passe)
        curseur.execute(
            """INSERT INTO pme (nom, email, mot_de_passe, secteur, ville)
               VALUES ( %s, %s, %s, %s, %s)""",
            (nom, email, mot_de_passe_hash, secteur, ville)
        )
        connexion.commit()
        pme_id=curseur.lastrowid

        return True,"Compte créé avec succés.",pme_id

    except Error as e:
        return False, f"Erreur lors de l'inscription : {e}", None
    finally:
        curseur.close()
        connexion.close()

def connecter_pme(email,mot_de_passe):
    connexion=connecter()
    if connexion is None:
        return False,"Impossile de se connecter a la base de données.",None

    try:
        curseur=connexion.cursor(dictionary=True)
        curseur.execute("SELECT id ,nom,email,mot_de_passe,secteur,ville FROM pme WHERE email=%s",
                        (email,)
        )
        pme=curseur.fetchone()
        if pme is None:
            return False,"Aucun compte ne correspond a cet email",None
        if not verifier_mot_de_passe(mot_de_passe,pme["mot_de_passe"]):
            return False,"Mot de passe invalide.",None
        pme.pop("mot_de_passe")
        return True,"Connexion réussie.",pme
    except Error as e:
        return False,f"Erreur lors de la connexion: {e}",None
    finally:
        curseur.close()
        connexion.close()


def enregistrer_evaluation_complete(pme_id,resultats,reponses):
    connexion=connecter()
    if connexion is None:
        return None
    try:
        curseur=connexion.cursor()
        curseur.execute(
            """INSERT INTO diagnostic (pme_id, score_global, niveau)
               VALUES (%s, %s, %s)""",
            (pme_id, resultats["score_global"], resultats["niveau_maturite"])
        )
        connexion.commit()
        evaluation_id = curseur.lastrowid
        for categorie_id, data in resultats["scores_categories"].items():
           curseur.execute(
            """INSERT INTO score_categorie (diagnostic_id, categorie_id, categorie_nom, score)
               VALUES (%s, %s, %s, %s)""",
            (evaluation_id, categorie_id, data["nom"], data["score"])

           )
        for question_id,score_obtenu in reponses.items():
            curseur.execute("INSERT INTO reponse(diagnostic_id,question_id,score) VALUES (%s,%s,%s)"
                            (evaluation_id, question_id, score_obtenu)
                            )
        connexion.commit()
        return evaluation_id
    except Error as e:
        print(f"Erreur lors de l'enregistrement de l'évaluation :{e}")
        connexion.rollback()
        return None
    finally:
        curseur.close()
        connexion.close()

def recupurer_historique_pme(pme_id):
    connexion=connecter()
    if connexion is None:
        return []
    try:
        curseur=connexion.cursor(dictionary=True)
        curseur.execute(
        """SELECT id, date_diagnostic, score_global, niveau
           FROM diagnostic
           WHERE pme_id = %s
           ORDER BY date_diagnostic DESC""",
        (pme_id,)
    )
        return curseur.fetchall()
    except Error as e:
        print(f"Erreur lors de la récuperation de l'historique :{e}")
    finally:
        curseur.close()
        connexion.close()
















































