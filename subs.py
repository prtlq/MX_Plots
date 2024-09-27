import os
import imageio
from PIL import Image
from kivy.clock import Clock
from PIL import ImageDraw, ImageFont
from collections import defaultdict


class AppInteraction:
    @staticmethod
    def toggle_action(instance):
        if instance.state == 'down':
            instance.text = 'Terminal Mode'
        else:
            instance.text = 'Parent Mode'

class ExecuteFunctions:
    @staticmethod
    def filter_directory_content(selected_directory):
        dirs_count = 0
        png_files = []
        try:
            for item in os.scandir(selected_directory):
                if item.is_dir():
                    dirs_count += 1
                elif item.name.lower().endswith('.png'):
                    png_files.append(item.name)
        except FileNotFoundError:
            pass
        return dirs_count, sorted(png_files), os.path.basename(selected_directory)
    
    @staticmethod
    def create_master_tif(master_tif_list, parent_directory, num_terminal_folders, terminal_dir_names, save_in_result_folder=False, result_folder_name="result_1", base_directory=None):
        if not master_tif_list or len(terminal_dir_names) != num_terminal_folders:
            return

        num_rows = num_terminal_folders
        num_columns = len(master_tif_list) // num_rows
        row_margin = 20
        font_size = 120
        font = ImageFont.truetype("arial.ttf", font_size)
        title_height = font_size + 10

        max_images_per_row = len(master_tif_list) // num_rows
        row_heights = [max(image.height for image in master_tif_list[i:i+max_images_per_row]) for i in range(0, len(master_tif_list), max_images_per_row)]

        column_width = max(image.width for image in master_tif_list)
        total_width = column_width * num_columns
        total_height = sum(row_heights) + (num_rows - 1) * row_margin + num_rows * title_height

        master_tif = Image.new("RGB", (total_width, total_height))
        y_offset = 0
        draw = ImageDraw.Draw(master_tif)

        for i, img in enumerate(master_tif_list):
            column_index = i % max_images_per_row
            row_index = i // max_images_per_row
            x_offset = column_index * column_width

            if column_index == 0:  
                if row_index < len(terminal_dir_names):  
                    draw.text((10, y_offset), terminal_dir_names[row_index], font=font, fill=(255, 255, 255))
                y_offset += title_height

            master_tif.paste(img, (x_offset, y_offset))
            y_offset += row_heights[row_index] + row_margin if column_index == max_images_per_row - 1 else 0

        if save_in_result_folder:
            if base_directory is None:
                base_directory = os.path.dirname(os.path.dirname(parent_directory))
            result_directory = os.path.join(base_directory, result_folder_name)
            if not os.path.exists(result_directory):
                os.makedirs(result_directory)
            master_tif_filename = os.path.join(result_directory, f"{os.path.basename(parent_directory)}_master.tif")
        else:
            master_tif_filename = os.path.join(os.path.dirname(parent_directory), f"{os.path.basename(parent_directory)}_master.tif")

        master_tif.save(master_tif_filename)


    @staticmethod
    def execute_action(file_chooser, result_label, mode):
        current_directory = os.getcwd()
        result_folder_name = 'dir_master'

        if mode == "Terminal Mode":
            parent_folders = []
            for root, dirs, _ in os.walk(file_chooser.path):
                if dirs:
                    parent_folders.append(root)

            def process_parent_folders(parent_index):
                if parent_index >= len(parent_folders):
                    result_label.text += "\nTerminal Mode processing completed."
                    return

                parent_root = parent_folders[parent_index]
                terminal_folders = []

                for root, dirs, _ in os.walk(parent_root):
                    if not dirs:
                        terminal_folders.append(root)

                master_tif_list = []
                num_rows = len(terminal_folders)

                terminal_dir_names = [os.path.basename(terminal_folder) for terminal_folder in terminal_folders]

                if num_rows == 0:
                    print(f"No terminal folders found under {parent_root}")
                    return

                for terminal_root in terminal_folders:
                    dirs_count, png_files, _ = ExecuteFunctions.filter_directory_content(terminal_root)
                    if png_files:
                        for png_file in png_files:
                            img = imageio.imread(os.path.join(terminal_root, png_file))
                            master_tif_list.append(Image.fromarray(img))
                if master_tif_list:
                    ExecuteFunctions.create_master_tif(master_tif_list, parent_root, num_rows, terminal_dir_names, save_in_result_folder=True, result_folder_name=result_folder_name, base_directory=current_directory)
                    result_label.text += f"\nMaster TIF for '{os.path.basename(parent_root)}' generated."
                else:
                    result_label.text += f"\nNo PNG files found in terminals under '{os.path.basename(parent_root)}'."

                Clock.schedule_once(lambda dt: process_parent_folders(parent_index + 1), 0)
            Clock.schedule_once(lambda dt: process_parent_folders(0), 0)

        elif mode == "Parent Mode":
            folder_groups = defaultdict(list)
            grandparent_directory = file_chooser.path

            for parent_dir in os.listdir(grandparent_directory):
                full_parent_path = os.path.join(grandparent_directory, parent_dir)
                if os.path.isdir(full_parent_path):
                    for root, dirs, _ in os.walk(full_parent_path, topdown=True):
                        for dir_name in dirs:
                            folder_groups[dir_name].append((parent_dir, os.path.join(root, dir_name))) 

            def process_folder_group(group_name, folder_data):
                all_images = []
                parent_dir_names = []

                for parent_dir_name, folder in folder_data:
                    _, png_files, _ = ExecuteFunctions.filter_directory_content(folder)
                    parent_dir_names.append(parent_dir_name)

                    for png_file in png_files:
                        img = imageio.imread(os.path.join(folder, png_file))
                        all_images.append(Image.fromarray(img))

                if all_images:
                    ExecuteFunctions.create_master_tif(all_images, folder_data[0][1], len(folder_data), parent_dir_names, save_in_result_folder=True, result_folder_name=result_folder_name, base_directory=current_directory)
                    result_label.text += f"\nMaster TIF for '{group_name}' generated."
                else:
                    result_label.text += f"\nNo PNG files found in '{group_name}'."

            for group_name, folder_data in folder_groups.items():
                process_folder_group(group_name, folder_data)

            result_label.text += "\nParent Mode processing completed."