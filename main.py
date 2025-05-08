import streamlit as st
import openai
from PIL import Image
from io import BytesIO

# 🚨 Izmanto slepeno API atslēgu no .streamlit/secrets.toml
client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

# 🌐 Lapas iestatījumi
st.set_page_config(page_title="Zīmējuma pārvēršana", layout="centered")
st.title("🧒➡️🖼️ Zīmējuma pārvēršana par fotoreālistisku tēlu")

# 📤 Augšupielāde
uploaded_file = st.file_uploader("Augšupielādē bērna zīmējumu", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Oriģinālais zīmējums", use_container_width=True)

    # 📝 Jaunais uzlabotais promts
    default_prompt = (
        "Take this drawing created by my child and transform it into a photorealistic image or realistic 3D render. "
        "I don't know what it's supposed to be — it could be a creature, object, or something completely from their imagination. "
        "Keep the original shape, proportions, line lengths, and all imperfections exactly as they are in the drawing — "
        "including any slanted eyes, uneven lines, or strange markings. Do not correct, smooth out, or change any details of their design. "
        "Make it look like this thing exists in the real world, with realistic textures (skin, fur, metal, etc.) and natural lighting. "
        "You can add realistic shadows and an environment or background that fits the feel of the drawing, but don't change anything about "
        "the form or details of what they created. No pencil crayon textures or hand-drawn styles — this must look like a photo or CGI render, "
        "but staying true to their imagination."
    )

    # ✏️ Lietotāja apraksts (ja nepieciešams)
    user_prompt = st.text_area("Apraksts ģenerēšanai (neobligāti):", default_prompt, height=250)

    # Attēla sagatavošana
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_data = buffer.getvalue()

    if st.button("🎨 Ģenerēt attēlu"):
        with st.spinner("Lūdzu uzgaidi..."):
            try:
                # Nosūtot attēlu uz OpenAI
                response = client.images.create_edit(
                    image=image_data,
                    prompt=user_prompt,
                    n=1,
                    size="1024x1024"
                )
                image_url = response.data[0].url
                st.image(image_url, caption="Rezultāts (fotoreālistisks)", use_container_width=True)
                st.success("✅ Attēls veiksmīgi ģenerēts!")
                st.markdown(f"[⬇️ Lejupielādēt attēlu]({image_url})")
            except Exception as e:
                st.error(f"⚠️ Kļūda: {str(e)}")
