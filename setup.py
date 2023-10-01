import os
import subprocess
import gettext


def compile_translations(localedir):
    for language in os.listdir(localedir):
        lang_dir = os.path.join(localedir, language)
        if os.path.isdir(lang_dir):
            mo_dir = os.path.join(lang_dir, 'LC_MESSAGES')
            os.makedirs(mo_dir, exist_ok=True)
            mo_file = os.path.join(mo_dir, 'messages.mo')
            po_file = os.path.join(lang_dir, 'messages.po')
            subprocess.run(['msgfmt', '-o', mo_file, po_file])



def install_requirements():
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])

def main():
    install_requirements()

    language = input("Select your preferred language (en/ru): ").strip()

    localedir = os.path.join(os.path.dirname(__file__), 'locales')
    compile_translations(localedir)

    lang = gettext.translation('messages', localedir, languages=[language])
    lang.install()

    bot_token = input(("Enter your Telegram bot token: ")).strip()
    developer_id = input(("Enter your developer chat ID: ")).strip()

    with open('bot.py', 'r') as f:
        content = f.read()
    content = content.replace('YOUR_API_TOKEN', bot_token)
    content = content.replace('YOUR_ID', developer_id) 
    with open('bot.py', 'w') as f:
        f.write(content)

    subprocess.Popen(['python3', 'bot.py'])

    print(("Bot setup completed and bot started!"))

if __name__ == "__main__":
    main()
