import streamlit as st
import openai
from PIL import Image
import io
import base64

# Ievieto šeit savu OpenAI API atslēgu
openai.api_key = "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"

st.title("Zīmējuma pārvēršana par fotoreālistisku attēlu 🧠🎨")

uploaded_file = st.file_uploader("Augšupielādē bērna zīmējumu", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Oriģinālais zīmējums", use_column_width=True)

    if st.button("Ģenerēt fotoreālistisku versiju"):
        # Konvertē attēlu uz base64 (kā prasa OpenAI)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        response = openai.images.generate(
            model="dall-e-3",
            prompt=(
                "Transform this exact child drawing into a photorealistic or realistic CGI render. "
                "Preserve all proportions, shapes, uneven lines, and imperfections exactly as drawn. "
                "Make it look like a real-world object or creature with natural lighting, shadows, and realistic textures like skin, metal, or fur. "
                "Do not fix or change anything in the design, only translate it to look real."
            ),
            image=img_str,
            n=1,
            size="1024x1024"
        )

        image_url = response.data[0].url
        st.image(image_url, caption="Fotoreālistiska versija", use_column_width=True)
        st.markdown(f"[Lejupielādēt attēlu]({image_url})")

