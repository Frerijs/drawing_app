import streamlit as st
from PIL import Image
from openai import OpenAI
import base64
import io

# 🔐 API atslēga no Streamlit secrets
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="Zīmējuma pārvēršana", layout="centered")
st.title("🧒✏️ ➜ 🖼️ No bērna zīmējuma uz fotoreālistisku attēlu")

st.markdown("""
**1.** Augšupielādē bērna zīmējumu (JPG/PNG)  
**2.** GPT-4o aprakstīs attēlu  
**3.** Mēs to kombinēsim ar tavu fiksēto promtu  
**4.** DALL·E 3 izveidos fotoreālistisku versiju
""")

uploaded_file = st.file_uploader("Augšupielādē attēlu:", type=["jpg", "jpeg", "png"])

# Tava fiksētā norāde (nemainīga)
fixed_prompt = """
Take this drawing created by my child and transform it into a photorealistic image or realistic 3D render. I don't know what it's supposed to be — it could be a creature, object, or something completely from their imagination. Keep the original shape, proportions, line lengths, and all imperfections exactly as they are in the drawing — including any slanted eyes, uneven lines, or strange markings. Do not correct, smooth out, or change any details of their design.
Make it look like this thing exists in the real world, with realistic textures (skin, fur, metal, etc.) and natural lighting.
You can add realistic shadows and an environment or background that fits the feel of the drawing, but don't change anything about the form or details of what they created. No pencil crayon textures or hand-drawn styles — this must look like a photo or CGI render, but staying true to their imagination.
"""

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📄 Augšupielādētais zīmējums", use_container_width=True)

    # Pārvērš attēlu uz base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    if st.button("🧠 Aprakstīt un ģenerēt attēlu"):
        with st.spinner("GPT-4o analizē zīmējumu..."):
            try:
                vision_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Describe this drawing so it can be turned into a photorealistic 3D render. Focus on shape, texture, and key visual elements."},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                            ]
                        }
                    ],
                    max_tokens=500
                )
                drawing_description = vision_response.choices[0].message.content.strip()
                st.success("✅ Zīmējuma apraksts izveidots")
                st.markdown(f"> {drawing_description}")
            except Exception as e:
                st.error(f"❌ GPT-4o kļūda: {e}")
                st.stop()

        full_prompt = f"{fixed_prompt}\n\nDrawing description: {drawing_description}"

        with st.spinner("🎨 DALL·E 3 ģenerē attēlu..."):
            try:
                dalle_response = client.images.generate(
                    model="dall-e-3",
                    prompt=full_prompt,
                    n=1,
                    size="1024x1024",
                    response_format="url"
                )
                result_url = dalle_response.data[0].url
                st.success("🖼️ Attēls veiksmīgi ģenerēts!")
                st.image(result_url, caption="Rezultāts", use_container_width=True)
            except Exception as e:
                st.error(f"❌ DALL·E kļūda: {e}")
