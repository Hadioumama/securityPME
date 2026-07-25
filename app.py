"""
app.py
------
Interface Streamlit du questionnaire d'auto-évaluation de maturité cyber.

IMPORTANT : chaque question affiche SES PROPRES options de réponse (texte
différent d'une question à l'autre), comme défini dans questions.json.
Il n'y a plus de "Oui / Partiellement / Non" générique.

Fonctionnement :
1. Écran d'accueil (nom de la PME).
2. Une catégorie de questions par écran (navigation Suivant / Précédent).
3. Écran final : calcul et affichage du score + niveau de maturité.

Lancer avec : streamlit run app.py
"""

import streamlit as st
import pandas as pd
from scoring import charger_questions, calculer_scores_globaux, identifier_categories_faibles
from db import inscrire_pme, connecter_pme, enregistrer_evaluation_complete

# ----------------------------------------------------------------------
# Configuration de la page
# ----------------------------------------------------------------------
st.set_page_config(page_title="Diagnostic Maturité Cyber PME", page_icon="🛡️", layout="centered")

# ----------------------------------------------------------------------
# Chargement des questions (une seule fois, mis en cache)
# ----------------------------------------------------------------------
@st.cache_data
def get_categories():
    return charger_questions("data/questions.json")

categories = get_categories()
nb_categories = len(categories)

# ----------------------------------------------------------------------
# Initialisation de l'état de session (mémoire entre les écrans)
# ----------------------------------------------------------------------
if "etape" not in st.session_state:
    st.session_state.etape = 0  # 0 = accueil, 1..N = catégories, N+1 = résultats

if "reponses" not in st.session_state:
    # dict { question_id: score_de_l_option_choisie }
    st.session_state.reponses = {}

if "nom_pme" not in st.session_state:
    st.session_state.nom_pme = ""

if "authentifie" not in st.session_state:
    st.session_state.authentifie = False

if "pme" not in st.session_state:
    st.session_state.pme = None  # dict avec id, nom, email, secteur_activite, taille_entreprise, ville


def etape_suivante():
    st.session_state.etape += 1


def etape_precedente():
    st.session_state.etape -= 1


# ----------------------------------------------------------------------
# ÉCRAN D'AUTHENTIFICATION — bloque l'accès au reste tant que non connecté
# ----------------------------------------------------------------------
if not st.session_state.authentifie:
    st.title("🛡️ Diagnostic de maturité cybersécurité")
    st.write("Connectez-vous ou créez un compte pour accéder au diagnostic.")

    onglet_connexion, onglet_inscription = st.tabs(["Connexion", "Créer un compte"])

    # ---------------- Onglet Connexion ----------------
    with onglet_connexion:
        with st.form("form_connexion"):
            email_connexion = st.text_input("Email", key="email_connexion")
            mdp_connexion = st.text_input("Mot de passe", type="password", key="mdp_connexion")
            bouton_connexion = st.form_submit_button("Se connecter")

        if bouton_connexion:
            if email_connexion.strip() == "" or mdp_connexion.strip() == "":
                st.warning("Merci de renseigner l'email et le mot de passe.")
            else:
                succes, message, pme = connecter_pme(email_connexion.strip(), mdp_connexion)
                if succes:
                    st.session_state.authentifie = True
                    st.session_state.pme = pme
                    st.session_state.nom_pme = pme["nom"]
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    # ---------------- Onglet Inscription ----------------
    with onglet_inscription:
        with st.form("form_inscription"):
            nom_entreprise = st.text_input("Nom de l'entreprise", key="nom_inscription")
            email_inscription = st.text_input("Email", key="email_inscription")
            mdp_inscription = st.text_input("Mot de passe", type="password", key="mdp_inscription")
            mdp_confirmation = st.text_input("Confirmer le mot de passe", type="password", key="mdp_confirmation")
            secteur_activite = st.text_input("Secteur d'activité", key="secteur_inscription")
            taille_entreprise = st.selectbox(
                "Taille de l'entreprise",
                options=["1-10 employés", "11-50 employés", "51-250 employés", "250+ employés"],
                key="taille_inscription"
            )
            ville = st.text_input("Ville", key="ville_inscription")
            bouton_inscription = st.form_submit_button("Créer mon compte")

        if bouton_inscription:
            if nom_entreprise.strip() == "" or email_inscription.strip() == "" or mdp_inscription == "":
                st.warning("Merci de remplir au minimum le nom, l'email et le mot de passe.")
            elif mdp_inscription != mdp_confirmation:
                st.warning("Les deux mots de passe ne correspondent pas.")
            elif len(mdp_inscription) < 8:
                st.warning("Le mot de passe doit contenir au moins 8 caractères.")
            else:
                succes, message, pme_id = inscrire_pme(
                    nom=nom_entreprise.strip(),
                    email=email_inscription.strip(),
                    mot_de_passe=mdp_inscription,
                    secteur=secteur_activite,
                    ville=ville
                )
                if succes:
                    st.success(f"{message} Vous pouvez maintenant vous connecter dans l'onglet 'Connexion'.")
                else:
                    st.error(message)

    # Empêche l'exécution du reste du script tant que l'utilisateur n'est pas connecté
    st.stop()

# ----------------------------------------------------------------------
# ÉCRAN 0 : Accueil (uniquement affiché une fois connecté)
# ----------------------------------------------------------------------
if st.session_state.etape == 0:
    st.title("🛡️ Diagnostic de maturité cybersécurité")
    st.write(f"Bienvenue **{st.session_state.pme['nom']}** 👋")
    st.write(
        "Ce questionnaire évalue le niveau de maturité cybersécurité de votre "
        "entreprise selon plusieurs catégories (contexte, protection des données, "
        "gestion des risques, gouvernance...)."
    )

    if st.button("Commencer le diagnostic ➜"):
        etape_suivante()
        st.rerun()

    st.divider()
    if st.button("Se déconnecter"):
        for cle in ["authentifie", "pme", "nom_pme", "etape", "reponses", "deja_enregistre"]:
            st.session_state.pop(cle, None)
        st.rerun()

# ----------------------------------------------------------------------
# ÉCRANS 1 à N : une catégorie de questions par écran
# ----------------------------------------------------------------------
elif 1 <= st.session_state.etape <= nb_categories:

    index_categorie = st.session_state.etape - 1
    categorie = categories[index_categorie]

    # Barre de progression
    progression = st.session_state.etape / (nb_categories + 1)
    st.progress(progression)
    st.caption(f"Étape {st.session_state.etape} / {nb_categories}")

    st.header(categorie["nom"])

    # Affiche chaque question avec SES PROPRES options (texte + score)
    for question in categorie["questions"]:
        q_id = question["id"]
        options = question["options"]  # liste de {"texte": ..., "score": ...}
        textes_options = [opt["texte"] for opt in options]

        # Retrouver l'index déjà sélectionné (si l'utilisateur revient en arrière)
        # index_par_defaut = None => aucune option cochée tant que l'utilisateur
        # n'a pas répondu explicitement.
        index_par_defaut = None
        if q_id in st.session_state.reponses:
            score_precedent = st.session_state.reponses[q_id]
            for i, opt in enumerate(options):
                if opt["score"] == score_precedent:
                    index_par_defaut = i
                    break

        choix_texte = st.radio(
            label=question["libelle"],
            options=textes_options,
            index=index_par_defaut,
            key=f"radio_{q_id}"
        )

        # Tant que l'utilisateur n'a rien coché, choix_texte vaut None :
        # on ne stocke rien dans ce cas (on ne peut pas calculer de score).
        if choix_texte is not None:
            score_choisi = next(opt["score"] for opt in options if opt["texte"] == choix_texte)
            st.session_state.reponses[q_id] = score_choisi

        st.divider()

    # Vérifie que toutes les questions de CETTE catégorie ont une réponse
    # avant d'autoriser à passer à l'écran suivant.
    questions_repondues = all(
        q["id"] in st.session_state.reponses for q in categorie["questions"]
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.etape > 1:
            if st.button("⬅ Précédent"):
                etape_precedente()
                st.rerun()
    with col2:
        label_bouton = "Voir mes résultats ➜" if st.session_state.etape == nb_categories else "Suivant ➜"
        if st.button(label_bouton, disabled=not questions_repondues):
            etape_suivante()
            st.rerun()

    if not questions_repondues:
        st.info("Merci de répondre à toutes les questions de cette section avant de continuer.")

# ----------------------------------------------------------------------
# ÉCRAN FINAL : Résultats
# ----------------------------------------------------------------------
else:
    st.title("📊 Résultats de votre diagnostic")
    st.subheader(f"Entreprise : {st.session_state.nom_pme}")

    resultats = calculer_scores_globaux(categories, st.session_state.reponses)

    score_global = resultats["score_global"]
    niveau = resultats["niveau_maturite"]

    # ------------------------------------------------------------------
    # Sauvegarde automatique en base MySQL — une seule fois par diagnostic
    # (on utilise un indicateur en session pour éviter de ré-enregistrer
    # à chaque rafraîchissement de la page). La PME est déjà identifiée
    # via l'authentification (st.session_state.pme).
    # ------------------------------------------------------------------
    if "deja_enregistre" not in st.session_state:
        pme_id = st.session_state.pme["id"]

        evaluation_id = enregistrer_evaluation_complete(
            pme_id=pme_id,
            resultats=resultats,
            reponses=st.session_state.reponses
        )
        if evaluation_id is not None:
            st.session_state.deja_enregistre = True
            st.toast("✅ Résultats enregistrés dans la base de données", icon="💾")
        else:
            st.warning("⚠️ Impossible d'enregistrer les résultats en base (voir la console pour le détail).")

    couleurs_niveau = {
        "Faible": "🔴",
        "Moyen": "🟠",
        "Bon": "🟢",
        "Excellent": "🟢"
    }

    st.metric(label="Score global de maturité", value=f"{score_global} / 100")
    st.markdown(f"### Niveau de maturité : {couleurs_niveau[niveau]} **{niveau}**")

    st.divider()
    st.subheader("Détail par catégorie")

    noms_categories = [d["nom"] for d in resultats["scores_categories"].values()]
    scores = [d["score"] for d in resultats["scores_categories"].values()]

    df_scores = pd.DataFrame({"Catégorie": noms_categories, "Score": scores}).set_index("Catégorie")
    st.bar_chart(df_scores)

    st.dataframe(df_scores, use_container_width=True)

    st.divider()
    st.subheader("Points à améliorer en priorité")

    categories_faibles = identifier_categories_faibles(resultats["scores_categories"], seuil=60)

    if categories_faibles:
        for cat in categories_faibles:
            st.write(f"⚠️ **{cat}** — nécessite des actions correctives")
    else:
        st.success("Aucune catégorie critique détectée. Continuez sur cette lancée !")

    st.divider()
    if st.button("🔄 Refaire le diagnostic"):
        st.session_state.etape = 0
        st.session_state.reponses = {}
        st.session_state.nom_pme = ""
        st.session_state.pop("deja_enregistre", None)
        st.rerun()