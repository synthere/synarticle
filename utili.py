# -*- coding: utf-8 -*-

from pydub import AudioSegment, silence
from moviepy.editor import VideoFileClip, AudioFileClip

import uuid

from tqdm import tqdm
import tempfile
import edge_tts
import asyncio
import soundfile as sf
import re

import requests
import config
import whisper
import spacy


def is_url(url):
    # 定义 URL 正则表达式模式
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// 或 https:// 或 ftp:// 或 ftps://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # 域名
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IP 地址
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6 地址
        r'(?::\d+)?'  # 可选端口号
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(url_pattern, url) is not None

"""
def is_valid_url(url):
    from urllib.parse import urlparse
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
"""
def set_proxy(set_val=''):
    if set_val == 'del':
        config.proxy = None
        # del
        if os.environ.get('http_proxy'):
            os.environ.pop('http_proxy')
        if os.environ.get('https_proxy'):
            os.environ.pop('https_proxy')
        return None
    if set_val:
        # set 
        if not set_val.startswith("http") and not set_val.startswith('sock'):
            set_val = f"http://{set_val}"
        config.proxy = set_val
        os.environ['http_proxy']=set_val
        os.environ['https_proxy']=set_val
        os.environ['all_proxy']=set_val
        return set_val

    # get proxy
    http_proxy = config.proxy or os.environ.get('http_proxy') or os.environ.get('https_proxy')
    if http_proxy:
        if not http_proxy.startswith("http") and not http_proxy.startswith('sock'):
            http_proxy = f"http://{http_proxy}"
        return http_proxy
    if sys.platform != 'win32':
        return None
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r'Software\Microsoft\Windows\CurrentVersion\Internet Settings') as key:

            proxy_enable, _ = winreg.QueryValueEx(key, 'ProxyEnable')
            proxy_server, _ = winreg.QueryValueEx(key, 'ProxyServer')
            if proxy_server:
                if not proxy_server.startswith("http") and not proxy_server.startswith('sock'):
                    proxy_server = "http://" + proxy_server
                try:
                    requests.head(proxy_server, proxies={"http": "", "https": ""})
                except Exception:
                    return None
                return proxy_server
    except Exception as e:
        pass
    return None


ISWORD = re.compile(r'.*\w.*')
import sys, os
def get_base_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return base_path
def split_audio_from_video(video_file):
    try:
        print("Extracting audio track")
        video = VideoFileClip(video_file, audio=True)
        audio = video.audio
        audio_file = os.path.splitext(video_file)[0] + ".wav"
        audio.write_audiofile(audio_file, logger=None)
        return audio_file
    except Exception as e:
        print(f"Error extracting audio from video: {e}")
        config.logger.info(f"Error extracting audio from video: {e}")
        return None

import numpy as np

def transcribe_audio(audio_file, source_language):
    try:
        print("Transcribing audio track")
        model_dir = os.path.join(get_base_path(),"./models/whisper/tiny.pt")
        model = whisper.load_model(model_dir)#large
        #model = whisper.load_model("tiny", download_root="./models/whisper")  # large
        trans = model.transcribe(audio_file, language=source_language, verbose=False, word_timestamps=True)
        return trans
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None


def translate_text(texts, target_language):
    from microsoft import trans
    target_language = 'zh-Hans'
    text = ''.join(texts)
    #print(" to translate:", text)
    try:
        results = trans(text, target_language, inst=None, source_code="")
        #print("trans result:", results)
        return [results]  # [result['translatedText'] for result in results]
    except Exception as e:
        print(f"Error translating texts: {e}")
        return None

import zhconv

def save_audio_to_file(audio, filename):
    try:
        #audio.export(filename, format="wav")
        sf.write(filename, audio, 16000)
        print(f"Audio track with translation only saved to {filename}")
    except Exception as e:
        print(f"Error saving audio to file: {e}")

def format_selector(ctx):
    """ not handle all cases """

    # formats are already sorted worst to best
    formats = ctx.get('formats')[::-1]
    #print("formats:", formats)
    # acodec='none' means there is no audio
    best_video = next(f for f in formats
                      if f['vcodec'] != 'none' and f['acodec'] == 'none')

    # find compatible audio extension
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    # vcodec='none' means there is no video
    best_audio = next(f for f in formats if (
        f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))
    print(f"best vide:{best_video}, audio_ex:{audio_ext}, best_audio:{best_audio}")
    # These are the minimum required fields for a merged format
    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        # Must be + separated list of protocols
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }

def download_file(url, path):
    path_file = os.path.join(path, 'tmpyt.mp4')

    ydl_opts = {
        'format-sort': '+size',
        'format': format_selector,
        'outtmpl': path_file,
    }
    from yt_dlp import YoutubeDL
    urls = [url]
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
    return path_file

def makedir(dir_path):
    dir_path=os.path.dirname(dir_path)#获取路径名，删掉文件名
    bool=os.path.exists(dir_path)#存在返回True，不存在返回False
    if bool:
        pass
    else:
        os.makedirs(dir_path)
# select_pic_ts unit:ms, 从视频开始计算
def select_pic(input_video_path, md_path, select_pic_ts):
    print("very start")
    import cv2
    cap = cv2.VideoCapture(input_video_path, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    dsize = (640, int(original_height * 640/original_width))
    sel_cnt = int(select_pic_ts * fps /1000)
    pic_file_name = './pic/tmppic.png'
    pic_name = ''
    for cnt in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        if cnt == sel_cnt:
            frame_re = cv2.resize(frame, dsize)
            pic_name = os.path.join(md_path, pic_file_name)
            makedir(pic_name)
            cv2.imwrite(pic_name, frame_re)
            print("find the target pic")
            break

    cap.release()
    return pic_file_name

import re
 
def replace_markdown_headers(markdown_text, new_content):
    # 使用正则表达式匹配Markdown标题
    headers_pattern = re.compile(r'(#{1,6})\s+(.*)')
    # 替换标题的函数
    def replace_header(match):
        current_level = len(match.group(1))
        print("current leve:", current_level, match.group(0))
        if current_level == 1:
            return match.group(0) + '  \n\n  ' + new_content + '\n\n  '
        else:
            return match.group(0)  # 保留原有标题
    # 应用替换函数到所有标题
    new_text = headers_pattern.sub(replace_header, markdown_text)
    return new_text
def replace_first_h1(markdown, new_title):
    # 正则表达式匹配Markdown格式的一级标题
    pattern = r"^(#\s.+?)$"
    # 使用sub函数替换，count=1确保只替换一次
    new_markdown = re.sub(pattern, f"#{new_title}\n", markdown, count=1)
    return new_markdown

if __name__ == '__main__':
    print("very starttt")
    file_path = './tmp/result.md'
    content = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    print("cont:", content)
    new_md = content.replace("```markdown", '')
    print("new content:", new_md)
    result_file = 'newly.md'
    with open(result_file, 'w', encoding='utf-8') as file:
        file.write(new_md)
    #select_pic('The AI Future Has ArrivedHere\'s What You Should Do About It.mp4', './tmp', 5000)


