from config import PATHS
from brain import chat

print("=== AI Agent Ready ===")
print(f"Desktop: {PATHS['desktop']}\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() == "exit":
        print("Bye!")
        break
    chat(user_input)
    print()