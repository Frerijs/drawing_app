import streamlit as st
import openai
from PIL import Image

# Izveido OpenAI klientu ar slepeno API atslēgu
client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="Zīmējuma pārvēršana", layout="centered")
st.title("🧒➡️🖼️ Zīmējuma pārvēršana par fotoreālistisku tēlu")

uploaded_file = st.file_uploader("Augšupielādē bērna zīmējumu", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Oriģinālais zīmējums", use_container_width=True)

    default_prompt = (
        "A photorealistic render of a creature or object based exactly on a child's drawing. "
        "Keep the exact shape, slanted eyes, uneven lines, and imperfections. "
        "Do not alter the design, just make it look like it exists in the real world with realistic materials, textures, and lighting."
    )

    user_prompt = st.text_area("Apraksts ģenerēšanai (neobligāti):", default_prompt, height=200)

    if st.button("🎨 Ģenerēt attēlu"):
        with st.spinner("Lūdzu uzgaidi..."):
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=user_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                image_url = response.data[0].url
                st.image(image_url, caption="Rezultāts (fotoreālistisks)", use_container_width=True)
                st.success("✅ Attēls veiksmīgi ģenerēts!")
                st.markdown(f"[⬇️ Lejupielādēt attēlu]({image_url})")

            except Exception as e:
                st.error(f"⚠️ Kļūda: {str(e)}")
