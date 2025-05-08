import streamlit as st
from PIL import Image
from io import BytesIO
import requests
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models

st.set_page_config(page_title="Zīmējuma stilizācija", layout="centered")
st.title("🎨 Pārvērt savu zīmējumu par mākslas darbu!")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------- Palīgfunkcijas ----------
def load_image(image, max_size=512):
    image = image.convert('RGB')
    size = max_size if max(image.size) > max_size else max(image.size)
    transform = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor()
    ])
    image = transform(image).unsqueeze(0)
    return image.to(device)

def im_convert(tensor):
    image = tensor.to("cpu").clone().detach()
    image = image.squeeze(0)
    image = transforms.ToPILImage()(image)
    return image

def get_image_from_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# ---------- Neirontīkls ----------
def get_features(image, model, layers=None):
    if layers is None:
        layers = {
            '0': 'conv1_1',
            '5': 'conv2_1',
            '10': 'conv3_1',
            '19': 'conv4_1',
            '21': 'conv4_2',  # content
            '28': 'conv5_1'
        }
    features = {}
    x = image
    for name, layer in model._modules.items():
        x = layer(x)
        if name in layers:
            features[layers[name]] = x
    return features

def gram_matrix(tensor):
    b, c, h, w = tensor.size()
    tensor = tensor.view(c, h * w)
    gram = torch.mm(tensor, tensor.t())
    return gram

def run_style_transfer(content_img, style_img, model, steps=300, style_weight=1e6, content_weight=1e0):
    content_features = get_features(content_img, model)
    style_features = get_features(style_img, model)
    style_grams = {layer: gram_matrix(style_features[layer]) for layer in style_features}

    target = content_img.clone().requires_grad_(True).to(device)
    optimizer = torch.optim.Adam([target], lr=0.003)

    for i in range(steps):
        target_features = get_features(target, model)
        content_loss = torch.mean((target_features['conv4_2'] - content_features['conv4_2']) ** 2)

        style_loss = 0
        for layer in style_grams:
            target_feat = target_features[layer]
            target_gram = gram_matrix(target_feat)
            style_gram = style_grams[layer]
            layer_loss = torch.mean((target_gram - style_gram) ** 2)
            style_loss += layer_loss / (target_feat.shape[1]**2)

        total_loss = content_weight * content_loss + style_weight * style_loss
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()

    return target

# ---------- Stila URL vārdnīca ----------
style_urls = {
    "Van Gogh": "https://upload.wikimedia.org/wikipedia/commons/4/47/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
    "Anime": "https://huggingface.co/datasets/Narsil/anime/resolve/main/00000.png",
    "Watercolor": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Watercolor_painting_of_a_flower.jpg"
}

# ---------- Interfeiss ----------
uploaded_file = st.file_uploader("📄 Augšupielādē savu zīmējumu (JPG/PNG)", type=["jpg", "jpeg", "png"])
style_option = st.selectbox("🖼️ Izvēlies stilu:", list(style_urls.keys()))

if uploaded_file:
    st.image(uploaded_file, caption="Oriģinālais zīmējums", use_container_width=True)

    if st.button("🎬 Stilizēt!"):
        with st.spinner("🔧 Ģenerē... Lūdzu uzgaidi ~30s"):
            content = load_image(Image.open(uploaded_file))
            style_image = get_image_from_url(style_urls[style_option])
            style = load_image(style_image)

            vgg = models.vgg19(pretrained=True).features.to(device).eval()
            for param in vgg.parameters():
                param.requires_grad = False

            output = run_style_transfer(content, style, vgg)
            result = im_convert(output)

            st.image(result, caption="🎉 Rezultāts", use_container_width=True)
            st.download_button("⬇️ Lejupielādēt", result.tobytes(), file_name="stylized.png", mime="image/png")
