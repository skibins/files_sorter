import os
import shutil


class FileOrganizer:
    def __init__(self):
        # Initialize variables to store user's desktop path, list of files, folders, and other necessary lists
        self.user_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.files_list = os.listdir(self.user_desktop)
        self.folder_list = []
        self.sorted_files_list = []
        self.edited_folders = []
        self.sort_by_letters = False  # Flag to indicate whether sorting by letters is required
        self.are_there_files = False  # Flag to check if there are files to sort

    def get_folders(self):
        """Collects folders based on user input."""
        # Ask the user for sorting preference
        sort_type = input(
            "If you want to sort by numbers press 'enter'. If you want to sort by letters type anything: ")

        # Iterate through the files on the desktop
        for file in self.files_list:
            # Get the file (desirable folder) path and extension
            file_path = os.path.splitext(self.user_desktop + '/' + file)

            # Check user input and add folders to the folder list accordingly
            if sort_type == '':
                if not file_path[1] and file[0].isnumeric():
                    self.folder_list.append(file)
            else:
                if not file_path[1] and not file[0].isnumeric():
                    self.folder_list.append(file)
                    self.sort_by_letters = True

    def sort_files_to_folders(self):
        """Sorts files into folders."""
        # Iterate through the files on the desktop
        for file in self.files_list:
            # Get the file path and extension
            file_path = os.path.splitext(self.user_desktop + '/' + file)
            file_first_char = file[0]

            # Check if the file is not 'desktop.ini' (Windows) and has an extension (i.e., it's a file, not a folder)
            if file_path[1] and file != 'desktop.ini':
                self.are_there_files = True
                # Iterate through the folder list to find the appropriate folder for the file
                for folder in self.folder_list:
                    folder_first_char = folder[0]
                    if self.sort_by_letters:
                        # Convert characters to uppercase for sorting by letters
                        file_first_char = file_first_char.upper()
                        folder_first_char = folder_first_char.upper()

                    # Move the file to the appropriate folder
                    if file_first_char == folder_first_char:
                        shutil.move(self.user_desktop + '/' + file, self.user_desktop + '/' + folder + '/' + file)
                        self.sorted_files_list.append(file)
                        self.edited_folders.append(folder)

        # Check if there are sorted files and ask the user if they want to rename them
        if not self.are_there_files:
            print('There are no files to sort.')
        else:
            change_names = input('Do you want to delete the first character from the sorted files? (Y/n): ')
            if change_names == 'Y' or change_names == 'y':
                self.del_from_files()

    def del_from_files(self):
        """Deletes characters from file names."""
        # Iterate through the folder list
        for folder in self.folder_list:
            # Check if the folder has been edited
            if folder in self.edited_folders:
                # Ask the user if they want to delete the first character from file names in the folder
                want_to_del = input(
                    f'Do you want to delete first character from every new file in folder {folder}? (Y/n): ')

                if want_to_del == 'Y' or want_to_del == 'y':
                    # Iterate through the files in the folder
                    files_in_folder = os.listdir(self.user_desktop + '/' + folder)
                    for file in files_in_folder:
                        # Check if the file has been sorted
                        if file in self.sorted_files_list:
                            # Rename the file by removing the first character
                            old_file_name = (self.user_desktop + '/' + folder + '/' + file)
                            new_file_name = (self.user_desktop + '/' + folder + '/' + file[1:])
                            os.rename(old_file_name, new_file_name)


if __name__ == '__main__':
    # Create an instance of FileOrganizer
    file_organizer = FileOrganizer()

    organize_files_question = input('Do you want to sort files from desktop into folders? (Y/n): ')

    if organize_files_question == 'Y' or organize_files_question == 'y':
        # Call methods to organize files
        file_organizer.get_folders()

        # Checks if there are folders that can be used to sort
        if not file_organizer.folder_list:
            print('Valid folders not found.')
        else:
            file_organizer.sort_files_to_folders()
    else:
        print('Exiting.')
