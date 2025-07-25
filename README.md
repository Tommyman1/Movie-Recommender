# 🎬 Movie Recommender System

> Personalized film suggestions based on your taste and watch history using Python & Machine Learning.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🧠 How It Works

This project uses **k-Nearest Neighbors (k-NN)** to recommend movies based on:

- Your **watch history**
- Your **personal genre preferences**
- Data from a curated movie dataset (`movie.csv`)

It scales and analyzes features like:
- 🎞️ `startYear`
- ⭐ `averageRating`
- ⏱️ `runtimeMinutes`
- 🎭 Genre-based user scores

---

## 🚀 Features

✅ Import movie dataset & watchlist  
✅ Personalized genre rating system  
✅ Store preferences with JSON  
✅ Recommend top 10 similar films  
✅ Save updated watchlist  

---

## 📦 Requirements

```bash
pip install pandas scikit-learn

📂 Your Project
│
├── main.py              # Main logic for recommendations
├── movie.csv            # Movie database
├── watchlist.csv        # Your saved watchlist
├── personal.json        # Your saved genre preferences
└── README.md            # This file

🛠️ Usage:

Input movies you've recently watched 🎥

Rate genres (1–10) on your first run ⭐

Get instant recommendations based on your last movie 🍿

Optionally save your updated watchlist 📝
