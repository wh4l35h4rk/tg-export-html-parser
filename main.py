import os
import subprocess


def make_folders_hidden(path):
    folder_list = ["css", "images", "js", "stickers", "contacts"]
    for item in folder_list:
        if os.path.exists(os.path.join(path, item)):
            subprocess.check_call(["attrib", "+H", os.path.join(path, item)])


def move_thumbs(path, old, new):
    old_path = os.path.join(path, old)
    th_path = os.path.join(path, new)
    photos_list = os.listdir(old_path)

    for name in photos_list:
        if name.endswith("_thumb.jpg"):
            os.rename(os.path.join(old_path, name),
                      os.path.join(th_path, name))


def replace_lines(path):
    p = open(path, mode='r', encoding="utf-8")
    type_list = ["photos", "video_files", "round_video_messages", "files"]
    line_list = []

    for line in p:
        if line.find("_thumb.jpg") != -1:
            for ttype in type_list:
                if line.find("thumbs/") != -1:
                    line = "\n" + line.replace(f"{ttype}/thumbs/", f"{ttype}/")
                if line.find(ttype) != -1:
                    line = "\n" + line.replace(f"{ttype}/", f"{ttype}/thumbs/")
                    break
        line_list.append(line)
    p.close()

    return line_list


if __name__ == '__main__':
    dir_path = input("paste absolute path of your chat directory here:\n")
    subdir_list = os.listdir(dir_path)

    make_folders_hidden(dir_path)

    media_type_list = ["photos", "video_files", "round_video_messages", "files"]
    for item in media_type_list:
        item_dir = os.path.join(dir_path, item)
        if not os.path.exists(item_dir):
            continue

        media_dir_list = os.listdir(item_dir)
        if "thumbs" not in media_dir_list:
            os.makedirs(os.path.join(item_dir, "thumbs"))
            subprocess.check_call(["attrib", "+H", os.path.join(item_dir, "thumbs")])
            move_thumbs(dir_path, item, os.path.join(item, "thumbs"))

    for name in subdir_list:
        file_path = os.path.join(dir_path, name)
        if os.path.isfile(file_path) and name.endswith(".html"):
            new_lines = replace_lines(file_path)

            fp = open(file_path, mode='w', encoding="utf-8")
            fp.writelines(new_lines)
            fp.close()

    print("process finished!")
