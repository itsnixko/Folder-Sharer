import os

# returns directories of all files in parent folder from parent folder
def get_files(directory):
    out = []
    for item in os.listdir(directory):
        item_dir = f'{directory}/{item}'
        if os.path.isfile(item_dir):
            out.append(item_dir)
        else:
            for i in get_files(item_dir):
                out.append(i)
    return out

if __name__ == "__main__":
    print(get_files("C:/Users/Nicko/Documents/Programming/Python/File_Share"))
