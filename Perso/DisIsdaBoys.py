import os
import random
import pygame
import time

#Uncomment to select test folder
FOLDER_PATH = r"C:\00_PYCHARM\DisIsdaBoys\Perso\000_Focus"
#FOLDER_PATH = r"C:\00_PYCHARM\DisIsdaBoys\Perso\1_TestDriveCommands"

MAX_REACTION_TIME = 10

def get_mp3_files(folder):
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(".mp3")
    ]

def wait_for_keypress():
    key = input("\n\n\nPress ENTER to play next track or 'q' to quit: ").strip().lower()
    if key == 'q':
        print("Exiting player...")
        exit()


def play_mp3_files_randomly(folder):
    mp3_files = get_mp3_files(folder)

    if not mp3_files:
        print("No MP3 files found.")
        return

    random.shuffle(mp3_files)
    pygame.mixer.init()

    for file in mp3_files:
        wait_for_keypress()
        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.5)
            print(f"{os.path.basename(file)}")
        except pygame.error as e:
            print(f"Skipping file due to error: {file}\n  Error: {e}")

    print("All files have been played.")


def play_mp3_files_sequentially(folder):
    mp3_files = get_mp3_files(folder)

    if not mp3_files:
        print("No MP3 files found.")
        return

    mp3_files.sort()  # ensures deterministic order (e.g., alphabetical)

    pygame.mixer.init()

    for file in mp3_files:
        wait_for_keypress()
        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.5)
            print(f"{os.path.basename(file)}")
        except pygame.error as e:
            print(f"Skipping file due to error: {file}\n  Error: {e}")

    print("All files have been played.")


def exam_mode(folder):
    mp3_files = get_mp3_files(folder)
    if not mp3_files:
        print("No MP3 files found.")
        return

    # Pick a random file for the exam
    file_path = random.choice(mp3_files)
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    start_time = time.time()
    input("REACTION: Press Enter as soon as you understand the command!")
    end_time = time.time()

    reaction = end_time - start_time
    print(f"Reaction time: {reaction:.2f} seconds")

    if reaction > MAX_REACTION_TIME:
        print("⚠️ TOO SLOW! In the exam, this might cause a late turn.")
    else:
        print("✅ Good reaction!")

    print(f"{os.path.basename(file_path)}")
    print(f"\n\n\n")

if __name__ == "__main__":
    exam_mode(FOLDER_PATH)
#    play_mp3_files_randomly(FOLDER_PATH)
    play_mp3_files_sequentially(FOLDER_PATH)
