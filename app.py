import streamlit as st
import pandas as pd
from streamlit_scroll_to_top import scroll_to_here
import streamlit.components.v1 as components
from scoring import charger_questions,calculer_scores_globaux,identifier_categories_faibles
from db import inscrire_pme,connecter_pme,enregistrer_evaluation_complete
from assistant_ai import generer_recommandations
from db import enregistrer_recommandation, recuperer_recommandation
from rapport_pdf import generer_rapport_pdf
import tempfile
import os
import base64
from pathlib import Path
import plotly.express as px
def scroll_en_haut():
    components.html("""
        <script>
            function allerEnHaut() {
                var marqueur = window.parent.document.getElementById('haut-page');
                if (marqueur) {
                    marqueur.scrollIntoView({behavior: 'instant', block: 'start'});
                }
            }
            allerEnHaut();
            setTimeout(allerEnHaut, 100);
            setTimeout(allerEnHaut, 300);
            setTimeout(allerEnHaut, 600);
            setTimeout(allerEnHaut, 1000);
        </script>
    """, height=0)

def wrap_label(texte, largeur=18):
    mots=texte.split(" ")
    lignes, ligne_actuelle= [],""
    for mot in mots:
        if len(ligne_actuelle + " " +mot) <= largeur:
            ligne_actuelle =(ligne_actuelle + " " +mot).strip()
        else:
            lignes.append(ligne_actuelle)
            ligne_actuelle=mot
    lignes.append(ligne_actuelle)
    return "<br>".join(lignes)
CHEMIN_LOGO=Path(__file__).resolve().parent / "static" / "logo.jpg"
with open(CHEMIN_LOGO,"rb") as f:
    logo=base64.b64encode(f.read()).decode()
st.set_page_config(page_title="Diagnostic Maturité Cyber PME", page_icon="🛡️", layout="centered")
with open("static/logo.jpg", "rb") as f:
    logo=base64.b64encode(f.read()).decode()
st.markdown("""
<style>
.stMainBlockContainer {
    max-width: 2000px !important;
    width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

.stApp {
  background: radial-gradient(
    circle at top,
    #BFDCD2 0%,
    #7BB5A1 50%,
    #365F51 100%
);

}
div[data-testid="stForm"]{
background-color:#FFFFFF;
width: 100% !important;
max-width: none !important;
border-radius:16px;
padding:2rem 2rem 1rem 2rem;
box-shadow:0 8px 30px rgba(0,0,0,0.35);
}
.bloc-auth h1, .bloc-auth h2, .bloc-auth h3, bloc-auth p,bloc-auth span{
color: #FFFFFF !important;
}
.stButton button, .stFormSubmitButton button{
border-raduis: 8px;
font-weight: 600 !important;
background-color: #365F51;
font-size: 15px !important;
}
</style>""",unsafe_allow_html=True)
@st.cache_data
def get_categories():
    return charger_questions("data/questions.json")

categories=get_categories()
nb_categories=len(categories)
toutes_questions=[]
for categorie in categories:
    for question in categorie["questions"]:
        toutes_questions.append({
            "categorie_nom":categorie["nom"],
            "question":question
        })
nb_total_questions=len(toutes_questions)
if "page_accueil_vue" not in st.session_state:
    st.session_state.page_accueil_vue=False

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
if "scroll_en_haut" not in st.session_state:
    st.session_state.scroll_en_haut=False
if st.session_state.scroll_en_haut:
    scroll_to_here(0, key="haut")
    st.session_state.scroll_en_haut = False

def etape_suivante():
    st.session_state.etape +=1

def etape_precedente():
    st.session_state.etape -=1
if not st.session_state.authentifie and not st.session_state.page_accueil_vue:
    st.markdown("""
    <style>
    .block-container {
    padding-top: 1rem !important;
}
    .hero-soustitre {
          text-align: center;
          font-size: 1.15rem;
          color:  #D9D3E8;
          max-width: 700px;
          margin: 0 auto 2.5rem auto;
    }
     .feature-card {
          border-left: 6px solid #040000;
          background-color: #7BB5A1;
          border-radius: 14px;
          padding: 1.5rem;
          text-align: center;
          box-shadow: 0 6px 20px rgba(0,0,0,0.30);
         min-height: 250px;
         height: 250px;
     }
     div[data-testid="column"] {
    display: flex;
    align-items: stretch;
}

     .feature-icone {
          font-size: 2.5rem;
          margin-bottom: 0.2rem;
     }
     .feature-titre {
          font-weight: 800;
          font-size: 1.05rem;
          margin-bottom: 0.4rem;
          color:#040000;
     }
    </style>
    """, unsafe_allow_html=True)
    st.write("")
    import streamlit.components.v1 as components
    import base64
    from pathlib import Path

    CHEMIN_LOGO = Path(__file__).resolve().parent / "static" / "logo.jpg"
    with open(CHEMIN_LOGO, "rb") as f:
        logo = base64.b64encode(f.read()).decode()

    components.html(f"""
    <div style="
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 12px;
        padding: 1rem 0 1rem 0;
        font-family: 'Source Sans Pro', sans-serif;
    ">
        <img src="data:image/jpeg;base64,{logo}" style="
          width: 80px;
          height: 80px;
          object-fit: contain;
          vertical-align: middle;
          margin-right: 12px;
          border-radius: 1000px;
          display: block;
        ">
        <span style="
            font-size: 2.4rem;
            font-weight: 800;
            color:#040000;
        ">Diagnostic de Maturité Cybersécurité</span>
    </div>
    """, height=110)

    texte_intro = (
        "Une plateforme gratuite pour évaluer en quelques minutes le niveau de sécurité"
        "informatique de votre PME, et recevoir un plan d'action personnalisé  à l'aide de l'IA."
    )
    st.markdown(
        f'<div class="hero-soustitre"{texte_intro}</div>', unsafe_allow_html=True
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("""
        <div class="feature-card">
             <div class="feature-icone">📋</div>
             <div class="feature-titre">Questionnaire ciblé</div>
             <div class="feature-texte">Un diagnostic structuré autour des principaux risques cybersécurité auxquelsfont face les PME marocaines.</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="feature-card">
             <div class="feature-icone">📊</div>
             <div class="feature-titre">Score détaillé</div>
             <div class="feature-texte">Un score global et une analyse par catégorie
             pour identifier préisément vos points faibles.</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown("""
        <div class="feature-card">
                    <div class="feature-icone">🤖</div>
                    <div class="feature-titre">Recommandations IA</div>
                    <div class="feature-texte">Un plan d'action concret et personnalisé,
                    généré automatiquement selon vos résultats.</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    col_gauche, col_bouton, col_droite = st.columns([1.3, 1,1.3])
    with col_bouton:
        st.markdown("""
        <style>
        div.stButton > button{
        background-color:#7BB5A1;
        color: #040000;
       font-size: 1.3rem !important;
       font-weight: 900 !important;
        }
        div.stButton > button p {
    font-size:  1rem !important;
    font-weight: 700 !important;
}
        </style>
        """, unsafe_allow_html=True)
        if st.button("Commencer le diagnostic ➜",width="stretch"):
            st.session_state.page_accueil_vue=True
            st.rerun()

    st.stop()

if not st.session_state.authentifie:
    col_gauche, col_centre, col_droite=st.columns([1,2,1])
    with col_centre:
        st.markdown('<div class="bloc-auth">', unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center;font-size:2rem;'>"
                    f"<img src='data:image/jpeg;base64,{logo}' width='55'  style='vartical-align:middle;border-radius:45px; margin-right:5px;'>"
                    f"Diagnostic de maturité cybersécurité</h1>",
                    unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>Connectez-vous ou créez un compte pour accéder au diagnostic.</p>",unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
        st.markdown("""
        <style>

        /* ===== CONTENEUR DES ONGLETS (ancien + nouveau format) ===== */
        .stTabs [data-baseweb="tab-list"],
        [data-testid="stTabs"] [role="tablist"] {
            gap: 0px !important;
            width: 100% !important;
            background: transparent !important;
            display: flex !important;
        }

        /* ===== TOUS LES ONGLETS (ancien + nouveau format) ===== */
        .stTabs [data-baseweb="tab"],
        [data-testid="stTabs"] button[role="tab"],
        [data-testid="stTab"] {
            flex: 1 !important;
            justify-content: center !important;
            height: 52px !important;
            background-color: #D9EFE8 !important;
            border: 2px solid #7BB5A1 !important;
            border-radius: 8px 8px 0px 0px !important;
            padding: 0px 20px !important;
            font-weight: 600 !important;
        }

        /* ===== TEXTE DES ONGLETS ===== */
        .stTabs [data-baseweb="tab"] p,
        [data-testid="stTabs"] button[role="tab"] p,
        [data-testid="stTab"] p {
            color: #365F51 !important;
            font-weight: 600 !important;
            font-size: 15px !important;
        }

        /* ===== ONGLET ACTIF ===== */
        .stTabs [data-baseweb="tab"][aria-selected="true"],
        [data-testid="stTabs"] button[aria-selected="true"],
        [data-testid="stTab"][aria-selected="true"] {
            background-color: #365F51 !important;
            border-color: #365F51 !important;
        }

        /* Texte onglet actif */
        .stTabs [data-baseweb="tab"][aria-selected="true"] p,
        [data-testid="stTabs"] button[aria-selected="true"] p,
        [data-testid="stTab"][aria-selected="true"] p {
            color: #7BB5A1 !important;
        }

        /* ===== SUPPRIMER L'INDICATEUR / BORDURE PAR DÉFAUT ===== */
        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }

        </style>
        """, unsafe_allow_html=True)
        onglet_connexion,onglet_inscription=st.tabs(["🔒 Connexion","👤 Créer un compte"],width="stretch")

    #Onglet Connexion
    with onglet_connexion:
        with st.form("form_connexion"):
            st.markdown("""
            <style>

            div[data-testid="stTextInput"] input,
            div[data-testid="stTextInput"] input:focus {
                background-color: #E8F2EF !important;
                color: #040000 !important;
                border: 1px solid #7BB5A1 !important;
            }

            div[data-testid="stTextInput"] input:-webkit-autofill,
            div[data-testid="stTextInput"] input:-webkit-autofill:hover,
            div[data-testid="stTextInput"] input:-webkit-autofill:focus {
                -webkit-box-shadow: 0 0 0 1000px #E8F2EF inset !important;
                box-shadow: 0 0 0 1000px #E8F2EF inset !important;
                -webkit-text-fill-color: #040000 !important;
            }

            </style>
            """, unsafe_allow_html=True)
            email_connexion = st.text_input("📧 Email", key="email_connexion",placeholder="****@gmail.com")
            mdp_connexion = st.text_input("🔒 Mot de passe", type="password", key="mdp_connexion",placeholder="*****")
            st.markdown("""
            <style>
            div[data-testid="stFormSubmitButton"] button{
             background-color:  #365F51 !important;
             color: white !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            </style>
            """,unsafe_allow_html=True)
            bouton_connexion=st.form_submit_button("Se connecter",type="primary")
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
        st.caption("Renseignez les informations de votre entreprise pour démarrer")
        with st.form("form_inscription",border=True):
            col1,col2=st.columns(2)
            with col1:
                nom_entreprise = st.text_input("🏢 Nom de l'entreprise", key="nom_inscription")
            with col2:
                email_inscription = st.text_input("📧 Email professionnel", key="email_inscription",placeholder="****@gmail.com")
            col3,col4=st.columns(2)
            with col3:
                secteur_activite = st.text_input("💼 Secteur d'activité", key="secteur_inscription",placeholder="IT,économie,agroalimantaire")
            with col4:
                ville = st.text_input("📍 Ville", key="ville_inscription",placeholder="Casablanca")
            col5,col6=st.columns(2)
            with col5:
                mdp_inscription = st.text_input( "🔒 Mot de passe", type="password", key="mdp_inscription",placeholder="8 caractére minimum")
            with col6:
                mdp_confirmation = st.text_input("🔒 Confirmer le mot de passe", type="password", key="mdp_confirmation",placeholder="Retapez le mot de passe")
            st.write("")
            bouton_inscription = st.form_submit_button("Créer mon compte ➜",width="stretch",type="primary")

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
    st.markdown('<div id="haut-page"></div>', unsafe_allow_html=True)
    scroll_en_haut()
    st.markdown(f"""
    <div style="
        width: 100%;
        display: flex;
        margin-top: -20px;
        justify-content: center;
        align-items: center;
        padding: 0.1rem 0;
        ">
          <div style="display: flex; align-items: center;justify-content:center; gap: 10px;margin-top: -20px; font-weight: 900; font-size: 2rem;
          color: #1F2937;">
          🛡️ Diagnostic de maturité cybersécurité
          </div>
       
    </div>             
""",unsafe_allow_html=True)
    st.divider()
    st.markdown(f"""
         <div style="padding: 0.2rem 0;display:block; justify-items:center;justify-content:center;">
            <h2 style="margin-bottom:0;">Bienvenue {st.session_state.pme['nom']}</h2>
            <p style="color=#374151; font-size:1.05rem;">Évaluez la maturité en cybersécurité de votre entreprise.</p>
         </div>
        """,unsafe_allow_html=True)
    with st.container(border=True):
       st.markdown("""
       <p style="color:black; margin-bottom:1.2rem;justify-content:center; align-items:center;font-size: 1rem;font-weight:600;">
    Un questionnaire structuré couvrant les principaux domaines de la cybersécurité
    pour analyser vos pratiques, évaluer votre niveau de maturité
    et identifier les écarts entre vos pratiques actuelles et les bonnes pratiques de sécurité.
    Les résultats permettent de mettre en évidence vos forces,
    vos faiblesses et vos priorités d’amélioration afin de construire une vision claire de la posture cybersécurité de votre entreprise.     
   </p>
       """, unsafe_allow_html=True)
       st.markdown("""
       <style>

       div.stButton > button {
           background-color: #365F51 !important;
           color: #FFFFFF !important;
           border: 2px solid #7BB5A1 !important;
           border-radius: 10px !important;
           padding: 0.75rem 2rem !important;
           font-size: 1.1rem !important;
           font-weight: 700 !important;
           transition: all 0.25s ease !important;
       }

       div.stButton > button:hover {
           background-color:#365F51 !important;
           color:  #FFFFFF !important;
           border-color: #365F51 !important;
          
           box-shadow: 0 6px 18px rgba(54, 95, 81, 0.30);
       }

       </style>
       """, unsafe_allow_html=True)
       col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 0.5, 1])
       with col3:
           if st.button("🛡️ Commencer le diagnostic ➜"):
               etape_suivante()
               st.rerun()
       st.write()

       col1, col2, col3, col4=st.columns(4)
       icones =[
           (col1, "📋", "Questionnaire"),
           (col2, "📊", "Score"),
           (col3, "🤖", "Assistant IA"),
           (col4, "📑", "Rapport de diagnostic"),
       ]
       for colonne,icone,label in icones:
           with colonne:
               st.markdown(f"""
               <div style="text-align:center; padding:0.8rem 0;">
                    <div style="font-size: 2rem;">{icone}</div>
                    <div style="color:#1F2937; font-weight:700; margin-top:4px;">{label}</div>
               </div>
               """, unsafe_allow_html=True)

       st.divider()
       st.markdown("""
              <style>

              div.stButton > button {
                  background-color: #365F51 !important;
                  color: #FFFFFF !important;
                   transform: translateY(-15px);
                  border: 2px solid #7BB5A1 !important;
                  border-radius: 10px !important;
                  padding: 0.75rem 2rem !important;
                  font-size: 1.1rem !important;
                  font-weight: 700 !important;
                  transition: all 0.25s ease !important;
              }

              div.stButton > button:hover {
                  background-color: #365F51 !important;
                  color: #FFFFFF !important;
                  border-color: #365F51 !important;
                  box-shadow: 0 6px 18px rgba(54, 95, 81, 0.30);
              }

              </style>
              """, unsafe_allow_html=True)
       col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
       with col3:
           if st.button("Se déconnecter"):
             for cle in ["authentifie", "pme", "nom_pme", "etape", "reponses", "deja_enregistre"]:
               st.session_state.pop(cle, None)
           st.rerun()

elif 1<= st.session_state.etape <= nb_total_questions:
    index_question=st.session_state.etape - 1
    element_actuel=toutes_questions[index_question]
    question=element_actuel["question"]
    categorie_nom=element_actuel["categorie_nom"]

    progression=st.session_state.etape/(nb_total_questions + 1)
    st.progress(progression)
    st.caption(f"étape {st.session_state.etape}/{nb_total_questions}")

    st.markdown("""
    <style>
    .categorie-titre{
        text-align: center;
        font-size: 1.9rem;
        font-weight: 800;
        color: #1F2937;
        margin: 1.2rem 0 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="categorie-titre">{categorie_nom}</div>"',unsafe_allow_html=True)
    q_id = question["id"]
    option = question["options"]
    textes_options = [opt["texte"] for opt in option]

    index_par_defaut = None
    if q_id in st.session_state.reponses:
        score_precedent = st.session_state.reponses[q_id]
        for i, opt in enumerate(option):
            if opt["score"] == score_precedent:
                index_par_defaut = i
                break

    st.markdown(f"<h4>{question['libelle']}</h4>", unsafe_allow_html=True)
    choix_texte = st.radio(
        label="",
        options=textes_options,
        index=index_par_defaut,
        key=f"radio_{q_id}",
        label_visibility="collapsed"
    )
    if choix_texte is not None:
        score_choisi = next(opt["score"] for opt in option if opt["texte"] == choix_texte)
        st.session_state.reponses[q_id] = score_choisi

    question_repondue = q_id in st.session_state.reponses

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.etape > 1:
            if st.button("⬅ Précédent"):
                etape_precedente()
                st.rerun()

    with col2:
        label_bouton = "Voir mes résultats ➜" if st.session_state.etape == nb_total_questions else "Suivant ➜"
        if st.button(label_bouton, disabled=not question_repondue):
            etape_suivante()
            st.rerun()

    if not question_repondue:
        st.markdown("""
        <div style="
            background-color: #7BB5A1;
            color: #040000;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.9rem 1.1rem;
        ">
            ℹ️ Merci de répondre à cette question avant de continuer.
        </div>
        """, unsafe_allow_html=True)
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


    noms_categories= [d["nom"] for d in resultats["scores_categories"].values()]
    scores=[d["score"] for d in resultats["scores_categories"].values()]

    labels_multilignes=[wrap_label(n) for n in noms_categories]
    df_scores=pd.DataFrame({"Catégorie":labels_multilignes,"Score":scores})

    fig=px.bar(
        df_scores,
        x="Catégorie",
        y="Score",
        color="Score",
        color_continuous_scale=["#E74C3C", "#F0AD4E", "#27AE60"],
        range_y=[0, 100],
        text="Score"
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        marker_line_width=0,
    )

    fig.update_layout(
        plot_bgcolor="#F0F5F3",
        paper_bgcolor="white",
        font=dict(color="black", size=15),
        xaxis=dict(
            title="",
            tickangle=0,
            tickfont=dict(color="black", size=12)
        ),
        yaxis=dict(
            title="Score (%)",
            title_font=dict(color="black", size=15),
            tickfont=dict(color="black", size=15),
            gridcolor="#E5E7EB"
        ),
        coloraxis_showscale=False,
        margin=dict(t=60, b=100)
    )
    st.plotly_chart(fig, width="stretch")



    st.divider()
    st.subheader("Points à améliorer en priorité")

    categories_faibles=identifier_categories_faibles(resultats["scores_categories"],seuil=60)

    if categories_faibles:
        for cat in categories_faibles:
            st.write(f"⚠️ **{cat}** — nécessite des actions correctives")
    else:
        st.markdown("""
          <div style="
              background-color: #D1FAE5;
              color: #065F46;
              font-weight: 600;
              border-radius: 8px;
              padding: 0.9rem 1.1rem;
              border-left: 5px solid #10B981;
          ">
              ✅ Aucune catégorie critique détectée.
          </div>
          """, unsafe_allow_html=True)
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

    col_pdf, col_refaire = st.columns(2)

    with col_pdf:
        if st.button("Générer le rapport PDF"):
            with st.spinner("Génération du PDF en cours..."):
                chemin_temp = os.path.join(tempfile.gettempdir(), "rapport_diagnostic.pdf")
                generer_rapport_pdf(
                    chemin_sortie=chemin_temp,
                    nom_pme=st.session_state.pme["nom"],
                    secteur_activite=st.session_state.pme.get("secteur", ""),
                    resultats=resultats,
                )
                with open(chemin_temp, "rb") as f:
                    st.session_state.pdf_bytes = f.read()

        if "pdf_bytes" in st.session_state:
            nom_fichier = f"rapport_maturite_{st.session_state.pme['nom'].replace(' ', '_')}.pdf"
            st.download_button(
                label="⬇️ Télécharger le rapport PDF",
                data=st.session_state.pdf_bytes,
                file_name=nom_fichier,
                mime="application/pdf"
            )

    with col_refaire:
        if st.button("🔄 Refaire le diagnostic"):
            st.session_state.pop("diagnostic_id", None)
            st.session_state.pop("recommandation_texte", None)
            st.session_state.pop("pdf_bytes", None)
            st.session_state.etape = 0
            st.session_state.reponses = {}
            st.session_state.nom_pme = ""
            st.session_state.pop("deja_enregistre", None)
            st.session_state.scroll_en_haut = True
            st.rerun()