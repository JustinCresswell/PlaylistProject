from manager import Manager
from util import FileUtil



def main():
    my_song_util = FileUtil()
    song_pool = my_song_util.load_songs_from_csv("song_list.csv")
    my_manager = Manager()
    running = 1
    while running:
        print("1. select playlist\n2. add songs\n3. remove songs\n4. play songs\n5. exit")
        choice = input("What do you want to do? ")
        if choice == "1":
            my_manager.select_or_create_playlist()
        if choice == "2":
            new_song = input("what song would you like to add? ")
            my_manager.add_song_to_playlist_by_name_or_id(new_song, song_pool)
        if choice == "3":
            my_manager.remove_song_by_index_or_name()
        if choice == "4":
            my_manager.play_current_song()
        if choice == "5":
            running -= 1

    print("done.")


if __name__ == "__main__":
    main()