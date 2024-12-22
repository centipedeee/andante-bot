import tracemalloc
from src import parser, tgbot
import multiprocessing

if __name__ == "__main__":
    tracemalloc.start()
    parser_process = multiprocessing.Process(target=parser.main, args=(), daemon=True)
    tgbot_process = multiprocessing.Process(target=tgbot.main, args=(), daemon=True)
    parser_process.start()
    tgbot_process.start()
    parser_process.join()
    tgbot_process.join()