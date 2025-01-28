import streamlit as st

st.title("🎈 My test")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

def main():
    # Titre principal de l'application
    st.title("API Simple avec Streamlit")
    
    # Section pour l'endpoint "sum"
    st.header("Endpoint : /sum")
    
    # Entrées des paramètres
    param1 = st.text_input("Paramètre 1 (a)", "0")
    param2 = st.text_input("Paramètre 2 (b)", "0")
    
    # Calcul de la somme
    try:
        a = float(param1)
        b = float(param2)
        result = {"sum": a + b}
    except ValueError:
        result = {"error": "Veuillez fournir des nombres valides."}
    
    # Afficher le résultat sous forme JSON
    st.json(result)
    
    # Informations pour les appels d'API
    st.subheader("Comment appeler cette API ?")
    st.write("Vous pouvez appeler cette API avec des outils comme Postman ou cURL.")
    st.code("""
    curl -X POST -H "Content-Type: application/json" \\
         -d '{"a":1, "b":2}' \\
         https://<votre-url-streamlit>/sum
    """)

# Exécution de la fonction principale
if __name__ == "__main__":
    main()
