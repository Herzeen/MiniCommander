import os

base_path = "test_folder"

# struktura plików
files = {
    "obrazy": ["photo1.jpg", "image.png", "grafika.jpeg"],
    "dokumenty": ["plik.pdf", "raport.docx", "notatki.txt"],
    "inne": ["video.mp4", "muzyka.mp3", "archiwum.zip"]
}

# utwórz folder główny
os.makedirs(base_path, exist_ok=True)

# twórz pliki
for category, filenames in files.items():
    for filename in filenames:
        path = os.path.join(base_path, filename)
        with open(path, "w") as f:
            f.write(f"Testowy plik: {filename}")

print("✅ Utworzono folder testowy:", base_path)