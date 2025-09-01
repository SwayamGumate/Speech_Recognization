import speech_recognition as sr
import time

recognizer = sr.Recognizer()

# Hindi Numbers
hindi_number_map = {
    "शून्य": 0, "एक": 1, "दो": 2, "तीन": 3, "चार": 4, "पांच": 5,
    "छह": 6, "सात": 7, "आठ": 8, "नौ": 9, "दस": 10,
    "ग्यारह": 11, "बारह": 12, "तेरह": 13, "चौदह": 14, "पंद्रह": 15,
    "सोलह": 16, "सत्रह": 17, "अठारह": 18, "उन्नीस": 19,
    "बीस": 20, "इक्कीस": 21, "बाईस": 22, "तेइस": 23,
    "चौबीस": 24, "पच्चीस": 25, "छब्बीस": 26, "सत्ताईस": 27,
    "अट्ठाईस": 28, "उनतीस": 29, "तीस": 30,
    "इकत्तीस": 31, "बत्तीस": 32, "तैंतीस": 33, "चौंतीस": 34,
    "पैंतीस": 35, "छत्तीस": 36, "सैंतीस": 37, "अड़तीस": 38, "उनचालीस": 39,
    "चालीस": 40, "इकतालीस": 41, "बेचालिस": 42, "तैंतालीस": 43,
}

# Marathi Numbers
marathi_number_map = {
    "शून्य": 0, "एक": 1, "दोन": 2, "तीन": 3, "चार": 4, "पाच": 5,
    "सहा": 6, "सात": 7, "आठ": 8, "नऊ": 9, "दहा": 10,
    "अकरा": 11, "बारा": 12, "तेरा": 13, "चौदा": 14, "पंधरा": 15,
    "सोळा": 16, "सतरा": 17, "अठरा": 18, "एकोणीस": 19,
    "वीस": 20, "एकवीस": 21, "बावीस": 22, "तेवीस": 23,
    "चोवीस": 24, "पंचवीस": 25, "सव्वीस": 26, "सत्तावीस": 27,
    "अठ्ठावीस": 28, "एकोणतीस": 29, "तीस": 30,
    "एकतीस": 31, "बत्तीस": 32, "तेहतीस": 33, "चौतीस": 34,
    "पस्तीस": 35, "छत्तीस": 36, "सदतीस": 37, "अडतीस": 38, "एकोणचाळीस": 39,
    "चाळीस": 40, "एक्केचाळीस": 41, "बेचाळीस": 42, "त्रेचाळीस": 43,
}

# -------------------------
# Listen & Recognize
# -------------------------
def listen_and_recognize(lang="mr-IN"):
    with sr.Microphone() as source:
        print(f"\n🎤 Speak a number in {'Hindi' if lang=='hi-IN' else 'Marathi'} (say 'stop' to exit)...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=lang)
        print("✅ You said:", text)
        return text.strip().lower()
    except Exception as e:
        print("❌ Error:", e)
        return None

# -------------------------
# Convert text → number
# -------------------------
def convert_to_number(text):
    if text.isdigit():  # Case 1: Pure digits
        return text

    # Case 2: Multi-word numbers ("तेईस चार सात" → 237)
    parts = text.split()
    digits = []
    for part in parts:
        if part.isdigit():
            digits.append(part)
        elif part in hindi_number_map:
            digits.append(str(hindi_number_map[part]))
        elif part in marathi_number_map:
            digits.append(str(marathi_number_map[part]))
        else:
            return None
    return "".join(digits) if digits else None

# -------------------------
# Auto-Save Contact
# -------------------------
def save_to_contact(number):
    name = f"Contact_{int(time.time())}"  
    filename = f"{name}.vcf"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("BEGIN:VCARD\n")
        f.write("VERSION:3.0\n")
        f.write(f"FN:{name}\n")
        f.write(f"TEL:{number}\n")
        f.write("END:VCARD\n")

    print(f"📂 Saved {number} as {filename}")

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    while True:
        spoken_text = listen_and_recognize(lang="mr-IN")  # change to "hi-IN" for Hindi
        if spoken_text in ["stop", "स्टॉप", "रुको"]:  # exit words
            print("👋 Stopping...")
            break

        if spoken_text:
            number = convert_to_number(spoken_text)
            if number:
                print("🔢 Converted:", number)
                save_to_contact(number)
            else:
                print("❌ Could not recognize number")
