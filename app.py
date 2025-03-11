import streamlit as st

def calculate_price(pr, transport_cost, agent=False, commission_rate=10):
    results = {}
    
    if pr < 6:
        if agent:
            pv = (pr + 6) / (1 - commission_rate / 100) + transport_cost
        else:
            pv = pr + 6 + transport_cost
        results['PV avec ' + str(commission_rate) + '% Commission'] = pv
    
    elif 6 <= pr <= 15:
        margins = [0.6, 0.5, 0.4]
        for margin in margins:
            if agent:
                pv = (pr / (1 - margin)) / (1 - commission_rate / 100) + transport_cost
            else:
                pv = (pr / (1 - margin)) + transport_cost
            results[f'PV avec {int(margin * 100)}% de marge et {commission_rate}% de commission'] = pv
    
    elif pr > 15:
        margin = 0.6 if pr * 1.6 <= 30 else 0.5
        
        if agent:
            pv = (pr / (1 - margin)) / (1 - commission_rate / 100) + transport_cost
        else:
            pv = (pr / (1 - margin)) + transport_cost
        
        results[f'PV avec {int(margin * 100)}% de marge et {commission_rate}% de commission'] = pv
    
    return results

# Streamlit App
st.title("Calculateur de Prix de Vente")

product_name = st.text_input("Nom du Produit")
pr = st.number_input("Prix de Revient (PR) en €", min_value=0.0, step=0.1)
transport_zone = st.selectbox("Zone de transport", ["Europe proche", "Europe éloignée", "Autre continent"])
agent = st.checkbox("Présence d'un agent")
commission_rate = st.number_input("Commission de l'agent en %", min_value=0, max_value=50, value=10) if agent else 0

transport_costs = {"Europe proche": 2, "Europe éloignée": 5, "Autre continent": 10}
transport_cost = transport_costs[transport_zone]

if st.button("Calculer"):
    results = calculate_price(pr, transport_cost, agent, commission_rate)
    st.write(f"### Résultat pour {product_name} en DAP {transport_zone}")
    st.write(f"- PR : {pr} €")
    st.write(f"- Transport inclus : {transport_cost} €/kg")
    if agent:
        st.write(f"- Commission de l'agent : {commission_rate}%")
    
    st.write("### Propositions de Prix")
    for key, value in results.items():
        st.write(f"{key} : {value:.2f} €/kg")
