import streamlit as st
import openai
from PIL import Image
import io
import base64
import os

# Ielādē API atslēgu droši
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# Lietotnes galvene
st.set_page_config(page_title="Zīmējums kļūst reāls", layout="centered")
st.title("🎨 No bērna zīmējuma uz 3D reālistisku attēlu")

# Lietotāja instrukcija
st.markdown("**1.** Augšupielādē bērna zīmējumu (JPG/PNG).  
**2.** Noklikšķini uz 'Ģenerēt attēlu', lai pārvērstu to fotoreālistiskā vai 3D renderētā versijā.")

# Augšupielāde
uploaded_file = st.file_uploader("Augšupielādē zīmējumu:", type=["jpg", "jpeg", "png"])

# Promts (nemaināms, kā lietotājs norādījis)
default_prompt = """
Take this drawing created by my child and transform it into a photorealistic image or realistic 3D render. I don't know what it's supposed to be — it could be a creature, object, or something completely from their imagination. Keep the original shape, proportions, line lengths, and all imperfections exactly as they are in the drawing — including any slanted eyes, uneven lines, or strange markings. Do not correct, smooth out, or change any details of their design.
Make it look like this thing exists in the real world, with realistic textures (skin, fur, metal, etc.) and natural lighting.
You can add realistic shadows and an environment or background that fits the feel of the drawing, but don't change anything about the form or details of what they created. No pencil crayon textures or hand-drawn styles — this must look like a photo or CGI render, but staying true to their imagination.
"""

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Oriģinālais zīmējums", use_column_width=True)

    if st.button("🎬 Ģenerēt attēlu"):
        with st.spinner("Sūta uz OpenAI..."):
            try:
                # Attēla kodēšana uz base64
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_bytes = buffered.getvalue()
                b64_image = base64.b64encode(img_bytes).decode()

                # OpenAI API izsaukums (DALL-E 3 renderēšana)
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=default_prompt,
                    n=1,
                    size="1024x1024",
                    response_format="url"
                )

                # Parāda rezultātu
                image_url = response["data"][0]["url"]
                st.success("Attēls ģenerēts!")
                st.image(image_url, caption="Fotoreālistisks rezultāts", use_column_width=True)

            except Exception as e:
                st.error(f"Notika kļūda: {e}")
