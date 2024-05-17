import streamlit as st
import qrcode
import io
import numpy as np
from PIL import Image
from io import BytesIO
import requests
from sklearn.cluster import KMeans

def extract_colors(image, num_colors):
    resized_image = image.resize((200, 200))
    rgb_image = resized_image.convert("RGB")
    image_array = np.array(rgb_image)
    pixels = image_array.reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_
    return colors

def couleur_image():
    st.title("Couleurs d'une image")

    option = st.radio("Sélectionner l'option", ("Fichier", "URL"))

    if option == "Fichier":
        uploaded_image = st.file_uploader("Choisissez une image", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            image = Image.open(uploaded_image).resize((200, 200))
            st.image(image, caption="Image originale", use_column_width=True)
            num_colors = st.slider("Nombre de couleurs", min_value=1, max_value=10, value=5, step=1)
            colors = extract_colors(image, num_colors)
            st.title("Palette de couleurs")
            for i, color in enumerate(colors):
                color_rgb = tuple(color.astype(int))
                st.write(f"Couleur {i+1}: RGB{color_rgb}")
                st.write(f"<div style='background-color:rgb{color_rgb};width:100px;height:40px;margin:10px'></div>", unsafe_allow_html=True)

    elif option == "URL":
        image_url = st.text_input("Entrez l'URL de l'image")
        if image_url:
            try:
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content)).resize((200, 200))
                st.image(image, caption="Image originale", use_column_width=True)
                num_colors = st.slider("Nombre de couleurs", min_value=1, max_value=10, value=5, step=1)
                colors = extract_colors(image, num_colors)
                st.title("Palette de couleurs")
                for i, color in enumerate(colors):
                    color_rgb = tuple(color.astype(int))
                    st.write(f"Couleur {i+1}: RGB{color_rgb}")
                    st.write(f"<div style='background-color:rgb{color_rgb};width:100px;height:40px;margin:10px'></div>", unsafe_allow_html=True)
            except Exception as e:
                st.write("Erreur lors du chargement de l'image. Veuillez vérifier l'URL fournie.")

def generate_qr_code(link):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(link)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')
    return qr_img

def page_accueil():
    st.header("Accueil")
    st.write("Bienvenue dans l'application  !")
    st.write("Sélectionnez une option dans le menu pour teste notre application.")

# Interface utilisateur Streamlit
st.title("Application Multitache")

menu_options = ["Accueil", "Couleurs d'une image", "Générer QR Code"]
page_selectionnee = st.sidebar.selectbox("Menu", menu_options)

if page_selectionnee == "Accueil":
    page_accueil()
elif page_selectionnee == "Couleurs d'une image":
    couleur_image()
elif page_selectionnee == "Générer QR Code":
    st.header("Générateur de QR Code")

    link = st.text_input("Entrez le lien :")

    if link:
        qr_code = generate_qr_code(link)

        qr_code_bytes = io.BytesIO()
        qr_code.save(qr_code_bytes, format='PNG')

        st.image(qr_code_bytes, caption="QR Code", use_column_width=True)

        st.download_button(
            label="Télécharger QR Code",
            data=qr_code_bytes.getvalue(),
            file_name="qr_code.png",
            mime="image/png"
        )
