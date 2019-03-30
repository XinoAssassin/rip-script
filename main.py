# -*- coding: UTF-8 –*-
import os
from multiprocessing import cpu_count

threads = cpu_count()
x264_bin_path: str = r"T:\MeGUI\tools\x264\x264.exe"
default_x264_command: str = r" --demuxer y4m - --level 4.1 --preset slow --tune film --crf 23 --deblock 0:0 --keyint 480 --min-keyint 1 --open-gop --b-adapt 2 --qpmax 36 --qcomp 0.8 --rc-lookahead 90 --merange 24 --me umh --nr 150 --subme 10 --psy-rd 1.10:0.15 --input-depth 16 -o "
mp4box_path = r"T:\MeGUI\tools\mp4box\mp4box.exe"
video_exts: list = [".mp4", ".mkv", ".m2ts", ".ts", ".mov", ".avi", ".wmv", ".flv"]


def get_file_list(path=""):
    if path == "":
        path = os.path.split(os.path.realpath(__file__))[0]
    return os.listdir(path)

def generate_vpy_scripts(filename: str):
    filename_without_ext = os.path.splitext(filename)[0]  # 单文件名，不存在后缀以及路径
    file_ext: str = os.path.splitext(filename)[1] # 扩展名
    filename = os.path.realpath(filename)  # 为了在vpy中写入绝对路径，将filename变更为绝对路径
    vpy_template_path = ""
    if file_ext.lower() == ".m2ts":
        vpy_template_path = os.path.split(os.path.realpath(__file__))[0] + "\\template_m2ts.vpy"
    elif file_ext.lower() == ".mov":
        vpy_template_path = os.path.split(os.path.realpath(__file__))[0] + "\\template_mov.vpy"
    else:
        vpy_template_path = os.path.split(os.path.realpath(__file__))[0] + "\\template.vpy"

    with open(vpy_template_path, "r", encoding="utf-8") as file:
        vpy_template_text: str = file.read()
    file.close()

        # 文本替换
    vpy_script_text = vpy_template_text.replace("__threads__", str(threads))
    vpy_script_text = vpy_script_text.replace("__filename__", filename)

        # 写入到新vpy文件中
    with open(filename_without_ext + ".vpy", "w+", encoding="utf-8") as file:
        file.write(vpy_script_text)
    file.close()

    return

""" def get_video_info(filename):
    MI = MediaInfoDLL3.MediaInfo()
    MI.Open(filename)
    info = MI.Inform()
    print(info)
    return """

def generate_encode_commandline(filename):
    if os.path.exists(os.environ["ProgramFiles"] + r"\VapourSynth\core64\vspipe.exe"):
        vspipe_bin_path = r"{}\VapourSynth\core64\vspipe.exe".format(os.environ["ProgramFiles"])
    else:
        vspipe_bin_path = r"{}\VapourSynth\core64\vspipe.exe".format(os.environ["ProgramFiles(x86)"])
    
    vspipe_command ='"{}" --y4m  {}.vpy - |'.format(vspipe_bin_path, os.path.splitext(filename)[0])

    x264_command = '"{}"{}{}.264'.format(x264_bin_path, default_x264_command, os.path.splitext(filename)[0])
    
    return "{}{}".format(vspipe_command, x264_command)

def generate_post_process_commandline(filename):
    filename_without_ext = os.path.splitext(filename)[0]
    if os.path.exists(filename_without_ext + ".m2ts"):
        audio_command = "ffmpeg -i {0}.m2ts -vn -acodec aac {0}.aac".format(filename_without_ext)
    elif os.path.exists(filename_without_ext + ".mov"):
        audio_command = "ffmpeg -i {0}.mov -vn -acodec aac {0}.aac".format(filename_without_ext)
    mp4box_command = r"{0} -add {1}.264 -add {1}.aac -new encoded\{1}.mp4".format("mp4box", filename_without_ext)
    return "{} \r\n {}".format(audio_command, mp4box_command)


# Main Program
for filename in get_file_list():
    if os.path.splitext(filename)[1].lower() in video_exts: # 扩展名匹配
        generate_vpy_scripts(filename) # 生成对应vpy
        if os.path.exists(os.path.realpath(os.path.splitext(filename)[0]+".vpy")): # 如果有了对应的vpy则可以写入 encode.bat
            if not os.path.exists("encode.bat"): # 如果没有 encode.bat 则新建一个，如果有则追加写入
                with open("encode.bat", "w+", encoding="utf-8") as file:
                    file.write(generate_encode_commandline(filename))
                file.close()
            else:
                with open("encode.bat", "a", encoding="utf-8", newline="\r\n") as file:
                    file.write("\r\n" + generate_encode_commandline(filename))
                file.close()
    elif os.path.splitext(filename)[1].lower() == ".264": # 如遇到 .264 文件则进入后处理
        if not os.path.exists("postProcess.bat"):
            with open("postProcess.bat", "w+", encoding="utf-8") as file:
                file.write(generate_post_process_commandline(filename))
            file.close()
        else:
            with open("postProcess.bat", "a", encoding="utf-8", newline="\r\n") as file:
                file.write("\r\n" + generate_post_process_commandline(filename))
            file.close()