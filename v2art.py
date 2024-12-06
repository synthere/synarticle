#coding=utf-8
import whisper
import argparse
import config
import os
import uuid
from pydub import AudioSegment, silence
from moviepy.editor import VideoFileClip, AudioFileClip

from tqdm import tqdm
import tempfile
import re
import edge_tts
import asyncio
import librosa
import soundfile as sf
import time
import utili

import time
def save_audio_to_file(audio, filename):
    try:
        #audio.export(filename, format="wav")
        sf.write(filename, audio, 16000)
        print(f"Audio track with translation only saved to {filename}")
    except Exception as e:
        print(f"Error saving audio to file: {e}")

def audio_pos(ms, sr):
    return int(ms *sr / 1000)

class Video2Art():
    def __init__(self):
        self.translate_percent = 0.0
        self.download_percent = 20
        self.translate_cost = 60
        self.art_cost = 20
    
    def update_progress(self, increse_percent):
        #print("increese:", increse_percent)
        self.translate_percent += increse_percent
        if self.translate_percent > 100:
            self.translate_percent = 100
    
    def trans(self, video_file, source_lang, target_lang, api_key, target_path):
        start_time = time.time()
        #check url or path
        video_file_fin = video_file
        if utili.is_url(video_file):
            video_file_fin = utili.download_file(video_file, target_path)
            print("url file download finish")
        
        audio_file = utili.split_audio_from_video(video_file_fin)
        if audio_file is None:
            config.logger.info('no audio file in video')
            return
 
        self.update_progress(self.download_percent)

        txt_source, txt_fin = self.translate_audio_files(source_lang, target_lang, audio_file)
        
        basn = os.path.splitext(os.path.basename(video_file_fin))[0]

        with open(os.path.join(target_path,  basn + '_origin.txt'), 'w', encoding='utf-8') as file:
            file.write(txt_source)    
        
        translated_file = os.path.join(target_path,  basn + '_translated.txt') 
        with open(translated_file, 'w', encoding='utf-8') as file:
            file.write(txt_fin)
        
        self.transcript_to_article(video_file_fin, translated_file, api_key, target_path)
        self.update_progress(100)
    
    def read_subtitle_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def transcript_to_article(self, video_file, srt_file, api_key,target_path):
        import json
        from zhipuai import ZhipuAI
        client = ZhipuAI(api_key=api_key)

        srt = self.read_subtitle_file(srt_file)

        prompt = f"这是视频字幕文本，SRT格式：\n{srt}。 请把字幕内容转成文章的格式，要求尽可能完整真实地包含原有内容，去除不必要的词，\
                进行2到3个层级的段落层次划分，\
                 并以markdown格式返回内容，使用<br>表示换行，不要使用\n,\
                请只将markdown内容作为响应，不包含其他内容\n"

        message = [
            {"role": "system", "content": "您是文章写作的得力助手，善于理解和总结。\
                    您完整阅读并准确理解字幕内容\
                "},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=message,
        )
        result_file = os.path.join(target_path, 'result.md')
        md_content = response.choices[0].message.content
        md_content = md_content.replace("```markdown", '')
        #insert pic
        pic_name = utili.select_pic(video_file, target_path, 5000)
        pic_content = ''
        if pic_name != '':
            pic_content = "![outline](" + pic_name +') '
        
        print("picname:", pic_name)

        new_md_content = utili.replace_markdown_headers(md_content, pic_content)#insert pic after header

        made_content = "  \n\n  Made with [SynthereArt](https://www.synthere.com)"

        with open(result_file, 'w', encoding='utf-8') as file:
            file.write(new_md_content)
            file.write(made_content)

    def translate_audio_files(self, source_language, target_language, audio_file):
        if 1:#try           
            transcription = utili.transcribe_audio(audio_file, source_language)
            print("transc:", transcription)

            print("Composing sentences:", len(transcription["segments"]))
            sent_source = ""
            sentences = []
            sentence = ""
            for segment in tqdm(transcription["segments"]):
                if segment["text"].isupper():
                    continue
                #print("seg start end:", segment["start"], segment["end"])
                for i, word in enumerate(segment["words"]):
                    if not utili.ISWORD.search(word["word"]):
                        continue

                    if word["word"].startswith("-"):
                        sentence = sentence[:-1] + word["word"] + " "
                    else:
                        sentence += word["word"] + " "

                    if word["word"].endswith(".") or word["word"].endswith(","):
                        #print("sentence:", sentence, sent_start, word["end"])
                        sentences.append(sentence)
                        sent_start = 0
                        sent_source += sentence
                        sentence = ""
            

            txt_final = ""
            # translate sentences in chunks of 128
            print("Translating sentences, len:", len(sentences))
            translated_texts = []
            for i in tqdm(range(0, len(sentences), 128)):
                chunk = sentences[i:i + 128]# 128 sentences not words
                #print("chunk to:", i, chunk)
                translated_chunk = utili.translate_text(chunk, target_language)
                if translated_chunk is None:
                    raise Exception("Translation failed")
                print("chunk:", translated_chunk)
                translated_texts.extend(translated_chunk)
                txt_final += translated_chunk[0]
                pg = int(self.translate_cost * 128/ len(sentences))
                #print("progress:", pg)
                self.update_progress(pg)

            print("Creating translated audio track:", translated_texts)

            return sent_source, txt_final
        else:#except Exception as e:
            print(f"Error merging audio files: {e}")
            config.logger.info(f"Error merg audio files: {e}")
            return None
  
def main():
    va = Video2Art()
    video_file_fin = "The AI Future Has ArrivedHere's What You Should Do About It.mp4"
    translated_file = "./tmp/The AI Future Has ArrivedHere's What You Should Do About It_translated.txt"
    api_key = ""
    target_path = "./tmp"
    va.transcript_to_article(video_file_fin, translated_file, api_key, target_path)

if __name__ == "__main__":
    main()
