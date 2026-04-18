import streamlit as st
import os
import shutil
import random

base_dir = 'downloads_temp/'
destination_dir = 'current_batch/SAFE'

os.makedirs(destination_dir, exist_ok=True)
os.makedirs("logs", exist_ok=True)

valid_ext = (".jpg", ".jpeg", ".png")

# Load images
images = [img for img in os.listdir(base_dir) if img.lower().endswith(valid_ext)]


if "shuffled" not in st.session_state:
    random.shuffle(images)
    st.session_state.shuffled = True

# SESSION STATE 
if "index" not in st.session_state:
    st.session_state.index = 0

if "accepted_count" not in st.session_state:
    st.session_state.accepted_count = 0

if "real_count" not in st.session_state:
    st.session_state.real_count = 0

if "animated_count" not in st.session_state:
    st.session_state.animated_count = 0

# STOP CONDITIONS 
if st.session_state.accepted_count >= 100:
    st.success("100 images collected!")
    st.stop()

if st.session_state.index >= len(images):
    st.warning("All images reviewed but 100 not reached!")
    st.stop()

#CURRENT IMAGE 
current_img = images[st.session_state.index]
img_path = os.path.join(base_dir, current_img)


st.write(f"Total: {st.session_state.accepted_count}/100")
st.write(f"Real: {st.session_state.real_count}/85")
st.write(f"Animated: {st.session_state.animated_count}/15")

st.write("Image: ",current_img)
st.image(img_path)

# Guidance
if st.session_state.animated_count < 15:
    st.info("Need more ANIMATED images")
elif st.session_state.real_count < 85:
    st.info("Need more REAL images")


if st.button("KEEP REAL"):

    if st.session_state.real_count >= 85:
        st.warning("Real image limit reached!")
    else:
        shutil.copy(img_path, os.path.join(destination_dir, f"{current_img}"))

        st.session_state.real_count += 1
        st.session_state.accepted_count += 1
        st.session_state.index += 1

        st.rerun()


if st.button("KEEP ANIMATED"):

    if st.session_state.animated_count >= 15:
        st.warning("Animated limit reached!")
    else:
        shutil.copy(img_path, os.path.join(destination_dir, f"{current_img}"))

        st.session_state.animated_count += 1
        st.session_state.accepted_count += 1
        st.session_state.index += 1

        st.rerun()



if "reason_select" not in st.session_state:
    st.session_state.reason_select = "-- Select reason --"

reason = st.selectbox(
    "Select reason",
    ["-- Select reason --", "Blurry", "Duplicate", "Low Quality", "Irrelevant", "Meme"],
    key="reason_select"
)

# REJECT
if st.button("REJECT"):

    if reason == "-- Select reason --":
        st.warning("Please select a reason first!")

    else:
        with open("logs/rejection_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{current_img} -> {reason}\n")

        st.session_state.index += 1

        # Reset selectbox safely
        del st.session_state["reason_select"]

        st.rerun()