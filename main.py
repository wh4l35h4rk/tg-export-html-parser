import os
import subprocess


def make_folders_hidden(path):
    subprocess.check_call(["attrib", "+H", os.path.join(path, "css")])
    subprocess.check_call(["attrib", "+H", os.path.join(path, "images")])
    subprocess.check_call(["attrib", "+H", os.path.join(path, "js")])
    if os.path.exists(os.path.join(path, "stickers")):
        subprocess.check_call(["attrib", "+H", os.path.join(path, "stickers")])
    if os.path.exists(os.path.join(path, "contacts")):
        subprocess.check_call(["attrib", "+H", os.path.join(path, "contacts")])


def move_thumbs(path):
    ph_path = os.path.join(path, "photos")
    th_path = os.path.join(path, "thumbs")
    photos_list = os.listdir(ph_path)

    for name in photos_list:
        if name.endswith("_thumb.jpg"):
            os.rename(os.path.join(ph_path, name),
                      os.path.join(th_path, name))


def replaced_lines(path):
    p = open(path, mode='r', encoding="utf-8")
    line_list = []

    for line in p:
        if line.find("_thumb.jpg") != -1:
            line = "\n" + line.replace("photos/", "thumbs/")
        line_list.append(line)
    p.close()
    return line_list


if __name__ == '__main__':
    dir_path = input("paste absolute path of your chat directory here:\n")
    subdir_list = os.listdir(dir_path)

    if "photos" not in subdir_list:
        print("are you sure you haven't picked the wrong folder?")
        exit()

    make_folders_hidden(dir_path)

    if "thumbs" not in subdir_list:
        os.makedirs(os.path.join(dir_path, "thumbs"))
        subprocess.check_call(["attrib", "+H", os.path.join(dir_path, "thumbs")])
        move_thumbs(dir_path)

    for name in subdir_list:
        file_path = os.path.join(dir_path, name)
        if os.path.isfile(file_path) and name.endswith(".html"):
            new_lines = replaced_lines(file_path)

            fp = open(file_path, mode='w', encoding="utf-8")
            fp.writelines(new_lines)
            fp.close()

    print("process finished!")
