import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODELE_IA = "llama-3.3-70b-versatile"


def construire_prompt(nom_pme, secteur_activite, resultats, categories_faibles, categories, reponses):
    question_a_risque = []
    for categorie in categories:
        for question in categorie["questions"]:
            q_id = question["id"]
            if q_id in reponses:
                score_obtenu = reponses[q_id]
                score_max = question["score_max"]
                if score_max > 0 and (score_obtenu / score_max) < 0.5:
                    question_a_risque.append(f"- {question['libelle']}")

    text_question_risque = "\n".join(question_a_risque) if question_a_risque else "Aucune question critique identifiée."

    prompt = f"""Tu es un expert en cybersécurité spécialisé dans l'accompagnement des PME marocaines.

Voici les résultats du diagnostic de maturité en cybersécurité d'une entreprise:
- Nom de l'entreprise: {nom_pme}
- Secteur d'activité: {secteur_activite or "non renseigné"}
- Score global de maturité: {resultats['score_global']}/100
- Niveau de maturité: {resultats['niveau_maturite']}

Catégories nécessitant une attention particulière (score < 60%):
{', '.join(categories_faibles) if categories_faibles else "Aucune catégorie critique"}

Points précis à risque identifiés dans le questionnaire:
{text_question_risque}

Consigne:
Rédige un plan d'action correctif personnalisé et concret pour cette entreprise, adapté au
contexte marocain (PME, ressources limitées). Structure ta réponse ainsi:
1. Un résumé en 2-3 phrases de la situation générale
2. Les 3 priorités d'action les plus importantes (classées par ordre d'urgence), avec pour
   chacune : l'action concrète à mener et pourquoi c'est important
3. Une recommandation générale d'organisation

Reste concret, évite le jargon technique inutile, et adapte le ton pour un dirigeant de PME
qui n'est pas un expert en cybersécurité. Sois bref et concis."""

    return prompt


def generer_recommandations(nom_pme, secteur_activite, resultats, categories_faibles, categories, reponses):
    """
    Appelle l'API Groq pour générer des recommandations personnalisées.
    Retourne un tuple (succes: bool, texte_ou_erreur: str).
    """
    cle_api = os.getenv("GROQ_API_KEY")

    if not cle_api:
        return False, (
            "Clé API introuvable. Vérifie que le fichier .env existe et contient "
            "GROQ_API_KEY=ta_cle."
        )

    try:
        client = Groq(api_key=cle_api)

        prompt = construire_prompt(
            nom_pme=nom_pme,
            secteur_activite=secteur_activite,
            resultats=resultats,
            categories_faibles=categories_faibles,
            categories=categories,
            reponses=reponses
        )

        reponse = client.chat.completions.create(
            model=MODELE_IA,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        texte_genere = reponse.choices[0].message.content
        return True, texte_genere

    except Exception as e:
        return False, f"Erreur lors de la génération des recommandations: {e}"