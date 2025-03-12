import streamlit as st

# Définition des coûts de transport selon la zone géographique
transport_costs = {
    "Europe proche (Belgique, Allemagne)": 2,
    "Europe éloignée (Turquie, Grèce)": 5,
    "Amérique du Nord": 7,
    "Amérique du Sud": 8,
    "Japon - Corée du Sud - Chine - Taiwan": 10,
    "Asie du Sud-Est": 12,
    "Océanie - Australie - Nouvelle-Zélande": 15
}

# Définition des incoterms et de leurs coûts supplémentaires
incoterm_costs = {
    "DAP (Transport inclus)": "transport",
    "EXW (Acheteur prend tout en charge)": 0,
    "FOB (Transport jusqu'au port exportation)": 1,
    "CIF (FOB + Assurance & Fret)": 3,
    "DDP (CIF + Droits de douane et taxes)": 5
}

def calculate_price(pr, transport_cost, incoterm, agent=False, commission_rate=10, tva=0):
    results = {}
    margins = [0.5, 0.4, 0.3, 0.25]
    recommended_margin = 0.5 if pr > 15 else (0.6 if pr * 1.6 <= 30 else 0.5)
    
    # Gestion du coût d'incoterm
    if incoterm_costs[incoterm] == "transport":
        incoterm_cost = transport_cost
    else:
        incoterm_cost = incoterm_costs[incoterm]
    
    for margin in margins:
        base_pv = pr / (1 - margin)
        if agent:
            base_pv /= (1 - commission_rate / 100)
        pv = base_pv + incoterm_cost
        
        highlight = "(Recommandé)" if margin == recommended_margin else ""
        results[f'PV avec {int(margin * 100)}% de marge et {commission_rate}% de commission {highlight}'] = pv * (1 + tva / 100)
    
    return results, incoterm_cost

# Streamlit App
st.title("Calculateur de Prix de Vente")

product_name = st.text_input("Nom du Produit")
pr = st.number_input("Prix de Revient (PR) en €", min_value=0.0, step=0.1)

# Sélection de la zone de transport
transport_zone = st.selectbox("Zone de livraison", list(transport_costs.keys()))
transport_cost = transport_costs[transport_zone]

# Sélection de l'Incoterm
incoterm = st.selectbox("Incoterm", list(incoterm_costs.keys()))

# Présence d'un agent ou d'un importateur
agent = st.radio("Présence d'un agent ou d'un importateur ?", ["Non", "Oui"]) == "Oui"
commission_rate = st.number_input("Commission de l'agent ou marge de l'importateur en %", min_value=0, max_value=50, value=10) if agent else 0

# Ajout d'une TVA en option
tva = st.number_input("TVA en %", min_value=0, max_value=30, value=0)

if st.button("Calculer"):
    results, incoterm_cost = calculate_price(pr, transport_cost, incoterm, agent, commission_rate, tva)
    st.write(f"### Résultat pour {product_name} en {incoterm}, Destination : {transport_zone}")
    st.write(f"- PR : {pr} €")
    if incoterm_costs[incoterm] == "transport":
        st.write(f"- Transport inclus dans l'incoterm : {transport_cost} €/kg")
    else:
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


