import json

def charger_questions(chemin_fichier="data/questions.json"):
    with open(chemin_fichier,"r",encoding="utf-8") as f:
        data=json.load(f)
    return data["categories"]


def calculer_score_categorie(categorie,reponses):
    total_score_max = 0
    total_score_obtenu = 0
    for question in categorie["questions"]:
        q_id=question["id"]
        score_max=question["score_max"]
        if q_id not in reponses:
            continue

        score_obtenu = reponses[q_id]
        score_max = question["score_max"]

        total_score_obtenu += score_obtenu
        total_score_max += score_max


    if total_score_max == 0:
         return 0.0

    return round((total_score_obtenu / total_score_max) * 100, 1)


def calculer_scores_globaux(categories, reponses):

    scores_categories = {}
    total_score_max_global = 0
    total_score_obtenu_global = 0

    for categorie in categories:
        score_cat = calculer_score_categorie(categorie, reponses)
        scores_categories[categorie["id"]] = {
            "nom": categorie["nom"],
            "score": score_cat
        }


        for question in categorie["questions"]:
            q_id = question["id"]
            if q_id not in reponses:
                continue
                
            total_score_obtenu_global += reponses[q_id]
            total_score_max_global += question["score_max"]

    score_global = 0.0
    if total_score_max_global > 0:
        score_global = round((total_score_obtenu_global / total_score_max_global) * 100, 1)

    niveau = determiner_niveau_maturite(score_global)

    return {
        "scores_categories": scores_categories,
        "score_global": score_global,
        "niveau_maturite": niveau
    }

def determiner_niveau_maturite(score_global):
        if score_global < 40:
           return "Faible"
        elif score_global < 65:
            return "Moyen"
        elif score_global <85:
            return "Bon"
        else:
            return "Excellent"

def identifier_categories_faibles(scores_categories,seuil=60):
    faibles=[]
    for cat_id,data in scores_categories.items():
        if data["score"] < seuil:
            faibles.append(data["nom"])
    return faibles