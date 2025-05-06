import streamlit as st
import openai

# ⚠️ TESTĒŠANAS NOLŪKOS — Nomaini pēc tam uz drošāku variantu!
openai.api_key = "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"

st.title("Zīmējuma pārvēršana par fotoreālistisku attēlu 🧠🎨")

uploaded_file = st.file_uploader("Augšupielādē bērna zīmējumu", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Oriģinālais zīmējums", use_container_width=True)

    default_prompt = (
        "A photorealistic render of a creature or object based exactly on a child's drawing. "
        "Keep the exact shape, slanted eyes, uneven lines, and imperfections. "
        "Do not alter the design, just make it look like it exists in the real world with realistic materials, textures, and lighting."
    )

    user_prompt = st.text_area("Papildus apraksts (neobligāti)", default_prompt, height=200)

    if st.button("Ģenerēt attēlu"):
        with st.spinner("Ģenerēju..."):
            response = openai.images.generate(
                model="dall-e-3",
                prompt=user_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url
            st.image(image_url, caption="Fotoreālistiska versija", use_container_width=True)
            st.markdown(f"[Lejupielādēt attēlu]({image_url})")
