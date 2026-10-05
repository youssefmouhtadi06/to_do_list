import json
import os
import streamlit as st

FICHIER_TACHES = "taches.json"

def charger_taches():
    if os.path.exists(FICHIER_TACHES):
        with open(FICHIER_TACHES, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_taches(taches):
    with open(FICHIER_TACHES, "w", encoding="utf-8") as f:
        json.dump(taches, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="To do list")
st.title("Organiser vos missions avec To do list")

if "taches" not in st.session_state:
    st.session_state["taches"] = charger_taches()

# Saisie d'une nouvelle tâche
nouvelle_tache = st.text_input("Saisir une nouvelle tâche :")

if st.button("Ajouter la tâche") and nouvelle_tache.strip():
    st.session_state["taches"].append(nouvelle_tache.strip())
    sauvegarder_taches(st.session_state["taches"])
    st.rerun()

st.divider()

# Affichage des tâches enregistrées avec option de suppression
taches = st.session_state["taches"]
total_taches = len(taches)

if total_taches > 0:
    taches_completes = 0

    for i, tache in enumerate(taches):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            if st.checkbox(f"Tâche {i + 1} : {tache}", key=f"tache_{i}"):
                taches_completes += 1

        with col2:
            # Bouton de suppression pour chaque tâche
            if st.button("🗑️ Supprimer", key=f"suppr_{i}"):
                st.session_state["taches"].pop(i)
                sauvegarder_taches(st.session_state["taches"])
                st.rerun()

    pourcentage = (taches_completes / total_taches) * 100
    st.divider()
    st.subheader(f"Vous avez réalisé {pourcentage:.2f} % de vos tâches ({taches_completes}/{total_taches})")
    st.progress(int(pourcentage))
else:
    st.write("Vous n'avez pas encore saisi de tâches.")