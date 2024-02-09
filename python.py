import os
import customtkinter as customtkinter
from tkinter import filedialog

def choose_directory_dialog(result_var, title):
    directory_path = filedialog.askdirectory(title=title)
    print(f"Selected {title.lower()} directory: {directory_path}")
    result_var.set(directory_path)

def diff_path(vid_path, sub_path, feedback_label):
    vidFiles = [name for name in os.listdir(vid_path) if name.lower().endswith(('.mp4', '.mkv', '.avi'))]
    subFiles = [name for name in os.listdir(sub_path) if name.lower().endswith(('.srt', '.sub', '.ssa', '.ass', '.vtt'))]

    vidFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    subFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    os.chdir(sub_path)

    try:
        assert len(subFiles) == len(vidFiles)
        for i, vname in enumerate(vidFiles):
            original_subtitle_path = os.path.join(sub_path, subFiles[i])
            subtitle_name, subtitle_extension = os.path.splitext(subFiles[i])
            new_subtitle_name = f"{os.path.splitext(vname)[0]}{subtitle_extension}"
            new_subtitle_path = os.path.join(sub_path, new_subtitle_name)
            
            print(f"{subFiles[i]} renamed to {new_subtitle_name}")
            os.rename(original_subtitle_path, new_subtitle_path)

        feedback_label.configure(text="Subtitle files successfully renamed!", fg_color="green")
    except AssertionError:
        feedback_label.configure(text="Error: Mismatched number of video and subtitle files", fg_color="red")


def on_video_button_click():
    choose_directory_dialog(vid_resulted_path, "Video")

def on_subtitle_button_click():
    choose_directory_dialog(sub_resulted_path, "Subtitle")

def on_rename_button_click(feedback_label):
    diff_path(vid_resulted_path.get(), sub_resulted_path.get(), feedback_label)
    
def end_process():
    root.destroy()  # Close the main window


# Create the main window
root = customtkinter.CTk()
root.geometry("600x500") 
root.title("Subtitle Rename App")

# Create a label
label = customtkinter.CTkLabel(root, text="Subtitle Rename App", font=("Helvetica", 16))
label.pack(pady=10)

# Create "Choose Video" button
choose_video_button = customtkinter.CTkButton(root, text="Choose Video Directory", command=on_video_button_click)
choose_video_button.pack(pady=10)

# Create "Choose Subtitle" button
choose_subtitle_button = customtkinter.CTkButton(root, text="Choose Subtitle Directory", command=on_subtitle_button_click)
choose_subtitle_button.pack(pady=10)

# Create StringVar to store the video and subtitle paths
vid_resulted_path = customtkinter.StringVar()
sub_resulted_path = customtkinter.StringVar()

# Create labels to display paths
video_path_label = customtkinter.CTkLabel(root, textvariable=vid_resulted_path, wraplength=400, justify="center", font=("Helvetica", 10))
video_path_label.pack(pady=10)

subtitle_path_label = customtkinter.CTkLabel(root, textvariable=sub_resulted_path, wraplength=400, justify="center", font=("Helvetica", 10))
subtitle_path_label.pack(pady=10)

# Create "Rename" button
rename_button = customtkinter.CTkButton(root, text="Rename Subtitles", command=lambda: on_rename_button_click(feedback_label))
rename_button.pack(pady=20)

# Create feedback label
feedback_label = customtkinter.CTkLabel(root, text="", font=("Helvetica", 12))
feedback_label.pack(pady=10)

# Create "End Process" button
end_process_button = customtkinter.CTkButton(root, text="End Process", command=end_process)
end_process_button.pack(pady=20)

# Start the customtkinter event loop
#root = App()
root.mainloop()