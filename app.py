import streamlit as st

def calculate_price(pr, incoterm_cost, agent=False, commission_rate=10, tva=0):
    results = {}
    margins = [0.5, 0.4, 0.3, 0.25]
    recommended_margin = 0.5 if pr > 15 else (0.6 if pr * 1.6 <= 30 else 0.5)
    
    for margin in margins:
        if agent:
            pv = (pr / (1 - margin)) / (1 - commission_rate / 100) + incoterm_cost
        else:
            pv = (pr / (1 - margin)) + incoterm_cost
        
        highlight = "(Recommandé)" if margin == recommended_margin else ""
        results[f'PV avec {int(margin * 100)}% de marge et {commission_rate}% de commission {highlight}'] = pv * (1 + tva / 100)
    
    return results

# Streamlit App
st.title("Calculateur de Prix de Vente")

product_name = st.text_input("Nom du Produit")
pr = st.number_input("Prix de Revient (PR) en €", min_value=0.0, step=0.1)

# Sélection de l'Incoterm avec description
incoterm = st.selectbox("Incoterm (par défaut DAP, avec impact des frais inclus)", [
    "DAP (Transport inclus) - Coût du transport inclus", 
    "EXW (Acheteur prend tout en charge) - Aucun coût", 
    "FOB (Transport jusqu'au port exportation) - 1€/kg", 
    "CIF (FOB + Assurance & Fret) - 3€/kg", 
    "DDP (CIF + Droits de douane et taxes) - 5€/kg"
])

# Définition des coûts supplémentaires en fonction de l'incoterm
incoterm_costs = {
    "DAP (Transport inclus) - Coût du transport inclus": 0,  
    "EXW (Acheteur prend tout en charge) - Aucun coût": 0,  
    "FOB (Transport jusqu'au port exportation) - 1€/kg": 1,  
    "CIF (FOB + Assurance & Fret) - 3€/kg": 3,  
    "DDP (CIF + Droits de douane et taxes) - 5€/kg": 5  
}
incoterm_cost = incoterm_costs[incoterm]

# Présence d'un agent ou d'un importateur
agent = st.radio("Présence d'un agent ou d'un importateur ?", ["Non", "Oui"]) == "Oui"
commission_rate = st.number_input("Commission de l'agent ou marge de l'importateur en %", min_value=0, max_value=50, value=10) if agent else 0

# Ajout d'une TVA en option
tva = st.number_input("TVA en %", min_value=0, max_value=30, value=0)

if st.button("Calculer"):
    results = calculate_price(pr, incoterm_cost, agent, commission_rate, tva)
    st.write(f"### Résultat pour {product_name} en {incoterm}")
    st.write(f"- PR : {pr} €")
    st.write(f"- Coût Incoterm ({incoterm}) : {incoterm_cost} €/kg")
    if agent:
        st.write(f"- Commission de l'agent : {commission_rate}%")
    if tva > 0:
        st.write(f"- TVA appliquée : {tva}%")
    
    st.write("### Propositions de Prix")
    for key, value in results.items():
        if "(Recommandé)" in key:
            st.markdown(f"<p style='color:red; font-weight:bold;'>{key} : {value:.2f} €/kg</p>", unsafe_allow_html=True)
        else:
            st.write(f"{key} : {value:.2f} €/kg")
