# image-scrape-and-clean

A beginner-friendly image dataset pipeline for scraping, cleaning, labeling, and processing images for machine learning projects.

---

## What This Does

This project helps you build a clean, labeled image dataset from scratch. You scrape images using the Unsplash API, manually clean and filter them through a simple UI, label them by category, and then apply basic image processing to make them model-ready.

---

## Pipeline Order

Run the scripts in this order:

```
1. create_local_structure.py   →   sets up all folders
2. scrape_real.py              →   downloads real images via Unsplash API
3. scrape_animated.py          →   downloads animated images via Unsplash API
4. manual_cleaning.py          →   review and filter raw images (Streamlit UI)
5. image_labeling.py           →   label cleaned images by category (Streamlit UI)
6. image_processing.py         →   resize, sharpen, brightness-correct all images
```

---

## Folder Structure

```
project/
├── downloads_temp/          # raw scraped images land here
├── current_batch/
│   └── SAFE/                # manually cleaned and accepted images
├── cleaned_batch/
│   └── SAFE/                # labeled images with renamed files
├── kaggle_upload/
│   └── SAFE/                # final images ready for upload
├── kaggle_output/           # model output
├── logs/
│   └── rejection_log.txt    # all rejected images with reasons
└── processed/
    └── SAFE/                # processed model-ready images
```

---

## Setup

### 1. Install dependencies

```bash
pip install requests streamlit opencv-python numpy python-dotenv
```

### 2. Add your Unsplash API key

Create a `.env` file in the root of the project:

```
UNSPLASH_ACCESS_KEY=your_key_here
```

Get a free key at [unsplash.com/developers](https://unsplash.com/developers)

### 3. Create folder structure

```bash
python create_local_structure.py
```

---

## Scripts

### scrape_real.py & scrape_animated.py
Scrapes images from Unsplash using keyword search. Real images use everyday life keywords (people, nature, animals etc.). Animated images use illustration/cartoon keywords. Downloads 10 images per keyword and saves them to `downloads_temp/`.

### manual_cleaning.py
Streamlit UI to review raw images one by one. You can accept them as REAL or ANIMATED, or reject with a reason (Blurry, Duplicate, Low Quality, Irrelevant, Meme). Stops automatically at 100 images (85 real + 15 animated). All rejections are logged.

### image_labeling.py
Streamlit UI to label cleaned images into four categories: REAL, ANIMATED, GAME, or FICTIONAL. Auto-renames files as `[label]_safe_[counter].[ext]` and copies them to `cleaned_batch/SAFE/`.

### image_processing.py
Applies OpenCV processing to all labeled images — resizes to 224x224, mild brightness/contrast boost, and sharpening. Saves output to `processed/SAFE/`.

---

## Avoiding Duplicates

**Within a batch:** Compute MD5 hash of each image before accepting it. Skip if hash already seen in current session.

**Across batches:** Maintain a `seen_hashes.txt` file that persists across sessions. Check every new image against it before accepting. Append new hashes after acceptance.

---

## .gitignore

Make sure your `.gitignore` includes:

```
.env
downloads_temp/
current_batch/
cleaned_batch/
processed/
kaggle_upload/
kaggle_output/
```

---

## Requirements

- Python 3.8+
- Unsplash API key (free)
- Libraries: `requests`, `streamlit`, `opencv-python`, `numpy`, `python-dotenv`
