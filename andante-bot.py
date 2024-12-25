import tracemalloc, multiprocessing, os, dotenv
from src import parser, tgbot

def check():
    if 'data/users' not in os.listdir():
        with open("data/users", "w") as f:
            f.write("")
    if 'data/links' not in os.listdir():
        with open("data/links", "w") as f:
            f.write("")
    if '.env' not in os.listdir():
        with open(".env", "w") as f:
            f.write("TOKEN=\nLINKS=\n")
    if 'videos' not in os.listdir():
        os.makedirs("videos")
    dotenv.load_dotenv()
    if not os.getenv('TOKEN') or not os.getenv('LINKS'):
        print("Please, fill in the .env file with the TOKEN and LINKS values!")
        return False
    return True

if __name__ == "__main__":
    if check():
        tracemalloc.start()
        parser_process = multiprocessing.Process(target=parser.main, args=(), daemon=True)
        tgbot_process = multiprocessing.Process(target=tgbot.main, args=(), daemon=True)
        parser_process.start()
        tgbot_process.start()
        parser_process.join()
        tgbot_process.join()
