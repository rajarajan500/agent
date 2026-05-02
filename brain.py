import json
from groq import Groq
from config import MODEL, TEMPERATURE, GROQ_API_KEY, USERNAME
from tools import ACTIONS

client = Groq(api_key=GROQ_API_KEY)

PROMPT = f"""You are an AI agent on a Windows PC.
Reply ONLY with a valid JSON array. No text. No markdown. Just the array.

User paths:
Desktop:   C:\\\\Users\\\\{USERNAME}\\\\Desktop
Documents: C:\\\\Users\\\\{USERNAME}\\\\Documents
Videos:    C:\\\\Users\\\\{USERNAME}\\\\Videos
Downloads: C:\\\\Users\\\\{USERNAME}\\\\Downloads
Pictures:  C:\\\\Users\\\\{USERNAME}\\\\Pictures
Music:     C:\\\\Users\\\\{USERNAME}\\\\Music

Available actions:

Open system folder:
{{"action":"open_folder","path":"C:\\\\Users\\\\{USERNAME}\\\\Videos"}}

Find and open any folder by name:
{{"action":"find_folder","name":"folder name"}}

Create a folder:
{{"action":"create_folder","path":"C:\\\\Users\\\\{USERNAME}\\\\Desktop\\\\myfolder"}}

Create a file with content:
{{"action":"create_file","path":"C:\\\\Users\\\\{USERNAME}\\\\Desktop\\\\file.py","content":"full code here"}}

Create a Vite+React app (auto installs dependencies):
{{"action":"create_vite_app","path":"C:\\\\Users\\\\{USERNAME}\\\\Desktop\\\\myapp"}}

Install npm packages:
{{"action":"run_npm_install","cwd":"C:\\\\Users\\\\{USERNAME}\\\\Desktop\\\\myapp"}}

Start dev server:
{{"action":"run_npm_dev","cwd":"C:\\\\Users\\\\{USERNAME}\\\\Desktop\\\\myapp"}}

Run any terminal command:
{{"action":"run_command","command":"pip install flask","cwd":"C:\\\\Users\\\\{USERNAME}\\\\Desktop"}}

Open an app:
{{"action":"open_app","name":"whatsapp"}}

Open a website:
{{"action":"open_url","url":"https://instagram.com"}}

STRICT RULES:
- Output ONLY a JSON array: [{{"action":"...","key":"value"}}]
- Always use double backslashes in paths
- Multi-step tasks: put ALL steps in ONE array in correct order
- Code files: ALWAYS write COMPLETE code, never truncate
- For React apps always use create_vite_app action first
- After create_vite_app, overwrite the src files with your custom code using create_file

HTML/CSS DESIGN RULES:
- Google Fonts: Inter or Poppins
- Hero: full viewport height, gradient background, big bold heading, CTA button
- Nav: sticky, glassmorphism (backdrop-filter: blur)
- Cards: rounded (16px), shadow, hover lift (transform: translateY(-8px))
- Buttons: gradient, pill shape, hover glow
- Fully responsive: mobile first, CSS grid and flexbox
- Modern gradients: #667eea to #764ba2 or #f093fb to #f5576c
- Smooth transitions and animations
- Always complete full page, never cut short
"""

history = []

def execute(reply):
    try:
        s = reply.index("[")
        e = reply.rindex("]") + 1
        actions = json.loads(reply[s:e])
        total = len(actions)
        print(f"\n  📋 {total} task(s) to execute...\n")
        for i, item in enumerate(actions, 1):
            action = item.get("action", "")
            print(f"  [{i}/{total}] {action}")
            fn = ACTIONS.get(action)
            if fn:
                fn(**item)
            else:
                print(f"  ✗ Unknown action: {action}")
        print(f"\n  ✅ All tasks done!\n")
        return
    except:
        pass
    try:
        s = reply.index("{")
        e = reply.rindex("}") + 1
        item = json.loads(reply[s:e])
        fn = ACTIONS.get(item.get("action", ""))
        if fn:
            fn(**item)
            return
    except:
        pass
    print(f"\nAgent: {reply}\n")

def chat(user_input):
    print("\n  ⟳ Thinking...\n")
    history.append({"role": "user", "content": user_input})
    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": PROMPT}] + history,
        temperature=TEMPERATURE,
    )
    reply = res.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": reply})
    execute(reply)