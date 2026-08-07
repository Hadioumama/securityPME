from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
   SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,PageBreak)



RECOMMANDATION_PAR_MOT_CLE={
    "gouvernance":("Mettez en place une politique de cybersécurité écrite, "
                   "et désignez un resposable clair au sein de l'entreprise."
    ),

    "sensibilisation":("Organisez une courte session de sensibilisation pour vos employés sur"
                        "les risques courants qui pouvant affecter  votre entreprise (phishing, ransomware,mots de passe faibles)."
                       ),
    "risque":("Réalisez un inventaire simple des riques principaux (perte de données,"
              "panne,piratage) et notez un plan d'action pour chacun."
              ),
    "donnée":("Identifiez les données sensibles de votre entreprise, limitez leur accès aux seules personnes autorisées"
              "et mettez en place des sauvegardes régulières afin de prévenir toute perte ou fruite de données."
              ),
    "protection":("Renforcez la protection de vos données sensibles (chiffrement,accès "
                  "restreint) et documentez qui peut y accéder ."
                  ),
    "développement":("Intégrez une vérification de sécurité de base  à chaque nouveau projet "
                     "informatique, avant sa mise en production."
                     ),
    "contexte":("Clarifiez l'importance réelle de votre systéme d'information pour"
                "l'activité, afin de prioriser vos investissement en sécurité."
                ),


}
RECOMMANDATION_GENERIQUE =(
    "Cette catégorie nécessite une attention particulière:identifiez les"
    "actions correctives prioritaires avec votre équipe ou un prestataire"
    "spécialisé en cybersécurité."
)

def generer_recommandations_simple(scores_categories,nb_max=3):
    categories_triees=sorted(scores_categories.values(),key=lambda d: d["score"])
    recommandations=[]
    for data in categories_triees[:nb_max]:
        nom_categorie= data["nom"]
        nom_minuscule= nom_categorie.lower()
        texte=RECOMMANDATION_GENERIQUE
        for mot_cle, conseil in RECOMMANDATION_PAR_MOT_CLE.items():
            if mot_cle in nom_minuscule:
                texte=conseil
                break
        recommandations.append((nom_categorie, texte, data["score"]))

    return recommandations

def generer_rapport_pdf(chemin_sortie,nom_pme,secteur_activite,resultats,recommandations_ia=None):
    doc=SimpleDocTemplate(
        chemin_sortie,
        pagesize=A4,
        topMargin=2*cm,
        bottomMargin=2*cm,
        leftMargin=2*cm,
        rightMargin=2*cm
    )

    styles=getSampleStyleSheet()
    style_titre=ParagraphStyle(
        "TitreRapport",parent=styles["Title"],fontSize=20,spaceAfter=6
    )
    style_soustitre=ParagraphStyle(
        "Soustitre",parent=styles["Normal"],fontSize=11,
        textColor=colors.grey, alignement=TA_CENTER, spaceAfter=20
    )
    style_section=ParagraphStyle(
        "Section",parent=styles["Heading2"],fontSize=14,
        spaceBefore=16, spaceAfter=8, textColor=colors.HexColor("#1F3864")
    )
    style_normal=styles["Normal"]
    style_recommandation_titre=ParagraphStyle(
        "RecoTitre",parent=styles["Normal"],fontSize=11,spaceBefore=10,
        textColor=colors.HexColor("#1F3864"),fontName="Helvetica-Bold"
    )
    elements=[]
    elements.append(Paragraph("Rapport de diagnostic de maturité cybersécurité",style_titre))
    elements.append(Paragraph(
        f"Généré le {datetime.now().strftime('%d/%m/%y à %H:%M')}",style_soustitre
    ))
    #information sur l'entreprise
    elements.append(Paragraph("Entreprise évaluée",style_section))
    infos_entreprise=[
        ["Nom de l'entreprise",nom_pme],
        ["Secteur d'activité",secteur_activite or "Non renseigné"],

    ]
    table_infos=Table(infos_entreprise,colWidths=[6*cm,10*cm])
    table_infos.setStyle(TableStyle([
        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),10),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("LINEBELOW",(0,0),(-1,-1),0.5,colors.lightgrey),
    ]))
    elements.append(table_infos)

    #Score global
    score_global=resultats["score_global"]
    niveau=resultats["niveau_maturite"]

    couleur_niveau={
        "Faible": colors.HexColor("#D9534F"),
        "Moyen": colors.HexColor("#F0AD4E"),
        "Bon": colors.HexColor("#5CB85C"),
        "Excellent": colors.HexColor("#5CB85C"),
    }
    couleur_niveau=couleur_niveau.get(niveau,colors.grey)
    #get(cle,valeur_par_defaut)
    elements.append(Paragraph("Score global de maturité",style_section))

    style_score=ParagraphStyle(
        "Score",parent=styles["Normal"],fontSize=28,fontName="Helvetica-Bold",
        textColor=couleur_niveau,spaceAfter=10,leading=34
    )
    elements.append(Paragraph(f"{score_global}/100",style_score))
    elements.append(Paragraph(f"Niveau de maturité: <b>{niveau}</b>",style_normal))

    elements.append(Paragraph("Détail par catégorie",style_section))

    donnees_tableau=[["Catégorie","Score (%)"]]
    for data in resultats ["scores_categories"].values():
        donnees_tableau.append([data["nom"],f"{data['score']:.1f}"])

    table_categories=Table(donnees_tableau,colWidths=[12*cm,4*cm])
    table_categories.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1F3864")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),10),
        ("ALIGN",(1,0),(1,-1),"CENTER"),
        ("GRID",(0,0),(-1,-1),0.5,colors.lightgrey),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F5F5F5")]),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    elements.append(table_categories)
    #Recommandation prioritaire basé sur les catégories faibles

    elements.append(Paragraph("Recommandations prioritaire",style_section))
    recommandations =generer_recommandations_simple(resultats["scores_categories"],nb_max=3)
    for i,(nom_categorie,texte,score_cat) in enumerate(recommandations,start=1):
        elements.append(Paragraph(f"{i}.{nom_categorie} (score : {score_cat:.1f}%)",style_recommandation_titre))
        elements.append(Paragraph(texte,style_normal))
        elements.append(Spacer(1,6))

        doc.build(elements)
        return chemin_sortie



