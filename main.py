import streamlit as st
from PIL import Image
from openai import OpenAI
import io

# 🚨 Izmanto slepeno API atslēgu no .streamlit/secrets.toml
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Lietotnes konfigurācija
st.set_page_config(page_title="Bērna zīmējuma 3D pārvēršana", layout="centered")
st.title("🎨 Bērna zīmējuma pārvēršana par fotoreālistisku 3D tēlu")

st.markdown("""
**1.** Augšupielādē bērna zīmējumu (JPG/PNG).  
**2.** Noklikšķini uz **'Ģenerēt attēlu'**, lai radītu reālistisku vai 3D renderētu tēlu!
""")

# Zīmējuma augšupielāde
uploaded_file = st.file_uploader("Augšupielādē attēlu:", type=["jpg", "jpeg", "png"])

# Stingri definētais promts no tavas iepriekšējās instrukcijas
default_prompt = """
Take this drawing created by my child and transform it into a photorealistic image or realistic 3D render. I don't know what it's supposed to be — it could be a creature, object, or something completely from their imagination. Keep the original shape, proportions, line lengths, and all imperfections exactly as they are in the drawing — including any slanted eyes, uneven lines, or strange markings. Do not correct, smooth out, or change any details of their design.
Make it look like this thing exists in the real world, with realistic textures (skin, fur, metal, etc.) and natural lighting.
You can add realistic shadows and an environment or background that fits the feel of the drawing, but don't change anything about the form or details of what they created. No pencil crayon textures or hand-drawn styles — this must look like a photo or CGI render, but staying true to their imagination.
"""

# Attēla apstrāde
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📄 Augšupielādētais zīmējums", use_container_width=True)

    if st.button("🎬 Ģenerēt attēlu"):
        with st.spinner("⏳ Ģenerē ar DALL·E 3..."):
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
