import streamlit as st
from PIL import Image
from openai import OpenAI
import io
import os

# API atslēga no Streamlit secrets vai OS vidi
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OPENAI_API_KEY nav iestatīts. Lūdzu, pievieno to secrets.toml vai .env failā.")
    st.stop()

# Inicializē klientu
client = OpenAI(api_key=api_key)

# Lapas konfigurācija
st.set_page_config(page_title="Bērna zīmējuma 3D pārvēršana", layout="centered")
st.title("🧒🎨 Bērna zīmējuma pārvēršana par fotoreālistisku 3D tēlu")

st.markdown("""
**1.** Augšupielādē bērna zīmējumu (JPG/PNG).  
**2.** Noklikšķini uz **'Ģenerēt attēlu'**, lai izveidotu fotoreālistisku vai 3D renderētu tēlu no viņa iztēles!
""")

# Zīmējuma augšupielāde
uploaded_file = st.file_uploader("Augšupielādē attēlu:", type=["jpg", "jpeg", "png"])

# Promts — stingri nemaināms, pēc tava lūguma
default_prompt = """
Take this drawing created by my child and transform it into a photorealistic image or realistic 3D render. I don't know what it's supposed to be — it could be a creature, object, or something completely from their imagination. Keep the original shape, proportions, line lengths, and all imperfections exactly as they are in the drawing — including any slanted eyes, uneven lines, or strange markings. Do not correct, smooth out, or change any details of their design.
Make it look like this thing exists in the real world, with realistic textures (skin, fur, metal, etc.) and natural lighting.
You can add realistic shadows and an environment or background that fits the feel of the drawing, but don't change anything about the form or details of what they created. No pencil crayon textures or hand-drawn styles — this must look like a photo or CGI render, but staying true to their imagination.
"""

# Ģenerēšanas darbība
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📄 Augšupielādētais zīmējums", use_container_width=True)

    if st.button("🎬 Ģenerēt attēlu"):
        with st.spinner("⏳ Ģenerē..."):
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=default_prompt,
                    n=1,
                    size="1024x1024",
                    response_format="url"
                )
                image_url = response.data[0].url
                st.success("✅ Attēls veiksmīgi ģenerēts!")
                st.image(image_url, caption="🖼️ Rezultāts", use_container_width=True)
            except Exception as e:
                st.error(f"❌ Kļūda: {e}")
else:
    st.info("⬆️ Lūdzu, augšupielādē zīmējumu, lai turpinātu.")
