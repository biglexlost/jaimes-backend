import os
import re

# Define bad characters and their clean replacements
REPLACEMENTS = {
    '“': '"',
    '”': '"',
    '‘': "'",
    '’': "'",
    '—': '-',  # em dash
    '–': '-',  # en dash
    '…': '...',  # ellipsis
}

# Set directory you want to sanitize
SOURCE_DIR = "./"  # current directory

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for bad_char, good_char in REPLACEMENTS.items():
        content = content.replace(bad_char, good_char)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Cleaned: {filepath}")
    else:
        print(f"👍 Already clean: {filepath}")

def main():
    print("🔍 Scanning Python files for funky characters...")
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".py"):
                clean_file(os.path.join(root, file))

def sanitize_prompt_text(prompt):
    for bad_char, good_char in REPLACEMENTS.items():
        prompt = prompt.replace(bad_char, good_char)
    return prompt
    
def generate_diagnosis(prompt):
    prompt = sanitize_prompt_text(prompt)
    # then send to Groq like before...

if __name__ == "__main__":
    main()
