import os
os.environ["PYTHONWARNINGS"] = "ignore"

import streamlit as st
import cv2
import torch
import numpy as np
import logging

from utils.csrnet_model import CSRNet
from utils.preprocess import preprocess_frame
from utils.heatmap import generate_heatmap
from email_alert import send_email_alert

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)

# ---------------- SECRETS HELPER ----------------
def get_secret(key, default=None):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, default)

EMAIL_SENDER = get_secret("EMAIL_SENDER")
EMAIL_PASSWORD = get_secret("EMAIL_PASSWORD")
EMAIL_RECEIVERS = get_secret("EMAIL_RECEIVERS")

EMAIL_CONFIGURED = all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVERS])

# ---------------- CONFIG ----------------
MODEL_PATH = "models/best_csrnet_partB.pth"
ALERT_THRESHOLD = 150

st.set_page_config(page_title="AI-DeepVision", layout="wide")
st.title("AI-DeepVision | Crowd Monitoring Dashboard")

# ---------------- SIDEBAR ----------------
st.sidebar.header("📧 Email Status")

def mask_email(addr):
    if not addr or "@" not in addr:
        return "(not set)"
    local, domain = addr.split("@", 1)
    return local[0] + "***@" + domain

if EMAIL_CONFIGURED:
    st.sidebar.success(f"Email alerts enabled — sender: {mask_email(EMAIL_SENDER)}")
    st.sidebar.write(f"Recipients: {EMAIL_RECEIVERS}")
else:
    st.sidebar.warning("Email alerts are disabled")

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    model = CSRNet()
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()
    return model

model = load_model()

# ---------------- IMAGE UPLOAD ----------------
uploaded = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded is not None:
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(image, channels="BGR", caption="Uploaded Image")

    input_tensor = preprocess_frame(image)

    with torch.no_grad():
        density_map = model(input_tensor)
        crowd_count = int(density_map.sum().item())

    st.metric("👥 Predicted Crowd Count", crowd_count)

    # ---------------- ALERT ----------------
    if crowd_count > ALERT_THRESHOLD:
        st.error("🚨 Overcrowding Detected")

        if EMAIL_CONFIGURED:
            try:
                send_email_alert(crowd_count)
                st.success("✅ Email alert sent")
            except Exception as e:
                st.error("❌ Failed to send email alert")
                st.text(str(e))
        else:
            st.info("📧 Email alerts are disabled")
    else:
        st.success("✅ Crowd Level Normal")

    # ---------------- HEATMAP ----------------
    heatmap = generate_heatmap(image, density_map)
    heatmap_rgb = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    st.image(heatmap_rgb, caption="Heatmap", width=image.shape[1])
