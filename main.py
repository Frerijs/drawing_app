import streamlit as st
from PIL import Image
from openai import OpenAI
import base64
import io

# 🔐 Izmanto OpenAI API atslēgu no Streamlit secrets
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="Zīmējuma pārveide uz 3D", layout="centered")
st.title("🧒✏️ ➜ 🖼️ No bērna zīmējuma uz fotoreālistisku attēlu")

st.markdown("""
**1.** Augšupielādē bērna zīmējumu (JPG/PNG)  
**2.** Mēs analizēsim zīmējumu ar GPT-4 Vision  
**3.** Tad izmantosim šo aprakstu, lai ģenerētu 3D attēlu ar DALL·E 3
""")

uploaded_file = st.file_uploader("Augšupielādē attēlu:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📄 Augšupielādētais zīmējums", use_container_width=True)

    # Pārvērš attēlu uz base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    if st.button("🔍 Analizēt & ģenerēt attēlu"):
        with st.spinner("🧠 GPT-4 analizē zīmējumu..."):
            try:
                vision_response = client.chat.completions.create(
                    model="gpt-4-vision-preview",
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

                drawing_description = vision_response.choices[0].message.content
                st.success("✅ Zīmējuma apraksts izveidots:")
                st.markdown(f"> {drawing_description}")

            except Exception as e:
                st.error(f"❌ GPT-4 Vision kļūda: {e}")
                st.stop()

        with st.spinner("🎨 Ģenerējam attēlu ar DALL·E 3..."):
            try:
                dalle_response = client.images.generate(
                    model="dall-e-3",
                    prompt=f"Photorealistic 3D render of the following concept: {drawing_description}",
                    n=1,
                    size="1024x1024",
                    response_format="url"
                )
                result_url = dalle_response.data[0].url
                st.success("🖼️ Attēls veiksmīgi ģenerēts!")
                st.image(result_url, caption="🧠 DALL·E rezultāts", use_container_width=True)
            except Exception as e:
                st.error(f"❌ DALL·E kļūda: {e}")
