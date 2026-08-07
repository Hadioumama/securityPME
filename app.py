import streamlit as st
import pandas as pd


from scoring import charger_questions,calculer_scores_globaux,identifier_categories_faibles
from db import inscrire_pme,connecter_pme,enregistrer_evaluation_complete
from assistant_ai import generer_recommandations
from db import enregistrer_recommandation, recuperer_recommandation
from rapport_pdf import generer_rapport_pdf
import tempfile
import os
st.set_page_config(page_title="Diagnostic Maturité Cyber PME", page_icon="🛡️", layout="centered")
@st.cache_data
def get_categories():
    return charger_questions("data/questions.json")

categories=get_categories()
nb_categories=len(categories)

if "etape" not in st.session_state:
    st.session_state.etape=0

if "reponses" not in st.session_state:
    st.session_state.reponses={}
if "nom_pme" not in st.session_state:
    st.session_state.nom_pme=""
if "authentifie" not in st.session_state:
    st.session_state.authentifie=False
if "pme" not in st.session_state:
    st.session_state.pme=None

def etape_suivante():
    st.session_state.etape +=1

def etape_precedente():
    st.session_state.etape -=1

if not st.session_state.authentifie:
    st.title("🛡️ Diagnostic de maturité cybersécurité")
    st.write("Connectez-vous ou créez un compte pour accéder au diagnostic .")
    onglet_connexion,onglet_inscription=st.tabs(["Connexion","Créer un compte"])

    #Onglet Connexion
    with onglet_connexion:
        with st.form("form_connexion"):
            email_connexion = st.text_input("Email", key="email_connexion")
            mdp_connexion = st.text_input("Mot de passe", type="password", key="mdp_connexion")
            bouton_connexion=st.form_submit_button("Se connecter")
            if bouton_connexion:
                if email_connexion.strip() == "" or mdp_connexion.strip() == "":
                    st.warning("Merci de remplir les champs email et mot de passe")
                else:
                    succes,message,pme=connecter_pme(email_connexion.strip(),mdp_connexion)
                    if succes:
                        st.session_state.authentifie= True
                        st.session_state.pme=pme
                        st.session_state.nom_pme=pme["nom"]
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    #onglet Inscription
    with onglet_inscription:
        with st.form("form_inscription"):
            nom_entreprise = st.text_input("Nom de l'entreprise", key="nom_inscription")
            email_inscription = st.text_input("Email", key="email_inscription")
            mdp_inscription = st.text_input("Mot de passe", type="password", key="mdp_inscription")
            mdp_confirmation = st.text_input("Confirmer le mot de passe", type="password", key="mdp_confirmation")
            secteur_activite = st.text_input("Secteur d'activité", key="secteur_inscription")
            ville = st.text_input("Ville", key="ville_inscription")
            bouton_inscription = st.form_submit_button("Créer mon compte")

        if bouton_inscription:
            if nom_entreprise.strip() == "" or email_inscription.strip() == "" or mdp_inscription.strip() == "":
                st.warning("Merci de remplir le nom,l'email et le mot de passe.")
            elif mdp_inscription != mdp_confirmation:
                st.warning("Les deux mots de passe ne correspondent pas.")
            elif len(mdp_inscription)<8:
                st.warning("Le mot de passe doit contenir au moins 8 caractères.")
            else:
                succes,message,pme_id=inscrire_pme(
                    nom=nom_entreprise.strip(),
                    email=email_inscription.strip(),
                    mot_de_passe=mdp_inscription,
                    secteur= secteur_activite,
                    ville=ville
                )
                if succes:
                    st.success(f"{message} Vous pouvez maintenant vous connecter dans l'onglet 'Connexion'.")
    st.stop()

if st.session_state.etape==0:
    st.title("🛡️ Diagnostic de maturité cybersécurité")
    st.write(f"Bienvenue **{st.session_state.pme['nom']}** ")
    st.write("Ce questionnaire évalue le niveau de maturité en cybersécurité de votre entreprise selon plusieurs critéres.")
    if st.button("Commencer le diagnostic ➜"):
        etape_suivante()
        st.rerun()
    st.divider()
    if st.button("Se déconnecter"):
        for cle in ["authentifie","pme","nom_pme","etape","reponses","deja_enregistre"]:
            st.session_state.pop(cle,None)
        st.rerun()

elif 1<= st.session_state.etape <= nb_categories:
    index_categorie =st.session_state.etape - 1
    categorie =categories[index_categorie]

    #Barre de progression
    progression= st.session_state.etape /(nb_categories +1)
    st.progress(progression)
    st.caption(f"étape {st.session_state.etape}/{nb_categories}")
    st.header(categorie["nom"])

    for question in categorie["questions"]:
        q_id=question["id"]
        option=question["options"]
        textes_options=[opt["texte"] for opt in option]

        index_par_defaut=None

        if q_id in st.session_state.reponses:
            score_precedent = st.session_state.reponses[q_id]
            for i,opt in enumerate(option):
                if opt["score"] == score_precedent:
                    index_par_defaut=i
                    break

        st.markdown(
            f"<h4>{question['libelle']}</h4>",
            unsafe_allow_html=True
        )
        choix_texte = st.radio(
            label="",
            options=textes_options,
            index=index_par_defaut,
            key=f"radio_{q_id}",
            label_visibility="collapsed"
        )
        if choix_texte is not None:
            score_choisi=next(opt["score"] for opt in option if opt["texte"]==choix_texte)
            st.session_state.reponses[q_id]=score_choisi

        st.divider()

    questions_repondues = all(
        q["id"] in st.session_state.reponses for q in categorie["questions"]
    )
    col1,col2=st.columns(2)
    with col1:
        if st.session_state.etape >1:
            if st.button("⬅ Précédent"):
                etape_precedente()


    with col2:
        label_bouton="Voir mes résultats ➜" if st.session_state.etape == nb_categories else  "Suivant ➜"
        if st.button(label_bouton,disabled=not questions_repondues):
            etape_suivante()
            st.rerun()

    if not questions_repondues:
        st.info("Merci de répondre à toutes les questions de cette section avant de continuer.")


else:
    st.title("📊 Résultats de votre diagnostic")
    st.subheader(f"Entreprise: {st.session_state.pme['nom']}")

    resultats=calculer_scores_globaux(categories,st.session_state.reponses)
    score_global=resultats["score_global"]
    niveau=resultats["niveau_maturite"]
    if "deja_enregistre" not in st.session_state:
        pme_id = st.session_state.pme["id"]
        diagnostic_id = enregistrer_evaluation_complete(
            pme_id=pme_id,
            resultats=resultats,
            reponses=st.session_state.reponses
        )

        if diagnostic_id is not None:
            st.session_state.deja_enregistre = True
            st.session_state.diagnostic_id = diagnostic_id
            st.toast("✅ Résultats enregistrés dans la base de données", icon="💾")
        else:
            st.warning("⚠️ Impossible d'enregistrer les résultats en base (voir la console pour le détail).")
    couleurs_niveau = {
        "Faible": "🔴",
        "Moyen": "🟠",
        "Bon": "🟢",
        "Excellent": "🟢"
    }
    st.metric(label="Score global de maturité", value=f"{score_global}/100")
    st.markdown(f"Niveau de maturité :{couleurs_niveau[niveau]} **{niveau}**")




    st.divider()
    st.subheader("Détail par catégorie")

    noms_categories = [d["nom"] for d in resultats["scores_categories"].values()]
    scores=[d["score"] for d in resultats["scores_categories"].values()]

    df_scores = pd.DataFrame({"Catégorie": noms_categories, "Score": scores}).set_index("Catégorie")
    st.bar_chart(df_scores)

    st.dataframe(df_scores,use_container_width=True)

    st.divider()
    st.subheader("Points à améliorer en priorité")

    categories_faibles=identifier_categories_faibles(resultats["scores_categories"],seuil=60)

    if categories_faibles:
        for cat in categories_faibles:
            st.write(f"⚠️ **{cat}** — nécessite des actions correctives")
    else:
        st.success("Aucune catégorie critique détectée.")
    categories_faibles = identifier_categories_faibles(resultats["scores_categories"], seuil=60)

    st.divider()
    st.subheader("🤖 Recommandations personnalisées")

    if "diagnostic_id" in st.session_state:
        if "recommandation_texte" not in st.session_state:
            recommandation_existante = recuperer_recommandation(st.session_state.diagnostic_id)
            if recommandation_existante:
                st.session_state.recommandation_texte = recommandation_existante
            else:
                with st.spinner("Génération des recommandations en cours..."):
                    succes, texte = generer_recommandations(
                        nom_pme=st.session_state.pme["nom"],
                        secteur_activite=st.session_state.pme.get("secteur", ""),
                        resultats=resultats,
                        categories_faibles=categories_faibles,
                        categories=categories,
                        reponses=st.session_state.reponses
                    )
                if succes:
                    st.session_state.recommandation_texte = texte
                    enregistrer_recommandation(st.session_state.diagnostic_id, texte)
                else:
                    st.session_state.recommandation_texte = None
                    st.error(f"Impossible de générer les recommandations : {texte}")

        if st.session_state.get("recommandation_texte"):
            st.markdown(st.session_state.recommandation_texte)
        else:
            st.info("Les recommandations n'ont pas pu être générées pour ce diagnostic.")

    st.divider()
    if st.button("🔄 Refaire le diagnostic"):
        st.session_state.pop("diagnostic_id", None)
        st.session_state.pop("recommandation_texte", None)
        st.session_state.etape = 0
        st.session_state.reponses={}
        st.session_state.nom_pme=""
        st.session_state.pop("deja_enregistre",None)

st.divider()
st.subheader("📄 Télécharger le rapport")

if st.button("Générer le rapport PDF"):
    with st.spinner("Génération du PDF en cours...."):
        chemin_temp=os.path.join(tempfile.gettempdir(),"rapport_diagnostic.pdf")
        generer_rapport_pdf(
            chemin_sortie=chemin_temp,
            nom_pme=st.session_state.pme["nom"],
            secteur_activite=st.session_state.pme.get("secteur",""),
            resultats=resultats,
        )
        with open(chemin_temp,"rb") as f:
            st.session_state.pdf_bytes=f.read()


if "pdf_bytes" in st.session_state:
    nom_fichier = f"rapport_maturite_{st.session_state.pme['nom'].replace(' ', '_')}.pdf"
    st.download_button(
        label="⬇️ Télécharger le rapport PDF",
        data=st.session_state.pdf_bytes,
        file_name=nom_fichier,
        mime="application/pdf"
    )