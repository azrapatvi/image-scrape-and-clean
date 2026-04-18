import streamlit as st
import os
import shutil
import random

base_dir = 'current_batch/SAFE'
destination_dir = 'cleaned_batch/SAFE'

# create destination folder
os.makedirs(destination_dir, exist_ok=True)

valid_ext = (".jpg", ".jpeg", ".png")

# LOAD IMAGES FROM BASE DIR
images = [img for img in os.listdir(base_dir) if img.lower().endswith(valid_ext)]

# SHUFFLE ONLY ONCE
if "shuffled" not in st.session_state:
    random.shuffle(images)
    st.session_state.images = images
    st.session_state.shuffled = True

images = st.session_state.images

# SESSION STATE INIT
if "index" not in st.session_state:
    st.session_state.index = 0

if "accepted_count" not in st.session_state:
    st.session_state.accepted_count = 0

if "real_count" not in st.session_state:
    st.session_state.real_count = 0

if "animated_count" not in st.session_state:
    st.session_state.animated_count = 0

if "game_count" not in st.session_state:
    st.session_state.game_count = 0

if "fictional_count" not in st.session_state:
    st.session_state.fictional_count = 0

# STOP CONDITION
if st.session_state.index >= len(images):
    st.warning("All images reviewed!")
    st.stop()

# CURRENT IMAGE
current_img = images[st.session_state.index]
img_path = os.path.join(base_dir, current_img)

# DISPLAY
st.title("Image Labeling Tool")

st.write(f"Total Selected: {st.session_state.accepted_count}")
st.write(f"Real: {st.session_state.real_count}")
st.write(f"Animated: {st.session_state.animated_count}")
st.write(f"Game: {st.session_state.game_count}")
st.write(f"Fictional: {st.session_state.fictional_count}")

st.image(img_path, caption=current_img)

# GET EXTENSION
ext = current_img.split('.')[-1]


def move_and_rename(prefix, counter_key):
    while True:
        st.session_state[counter_key] += 1
        new_name = f"{prefix}_safe_{st.session_state[counter_key]}.{ext}"
        new_path = os.path.join(destination_dir, new_name)

        # avoid overwrite
        if not os.path.exists(new_path):
            break

    shutil.copy(img_path, new_path)

    st.session_state.accepted_count += 1
    st.session_state.index += 1
    st.rerun()


# BUTTONS

if st.button("KEEP REAL"):
    move_and_rename("real", "real_count")

if st.button("KEEP ANIMATED"):
    move_and_rename("animated", "animated_count")

if st.button("KEEP GAME"):
    move_and_rename("game", "game_count")

if st.button("KEEP FICTIONAL"):
    move_and_rename("fictional", "fictional_count")