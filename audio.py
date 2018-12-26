# -*- coding: utf-8 -*-
import os
import tempfile
from gtts import gTTS
from pydub import AudioSegment
from pygame import mixer, display, time, event

def getContent(txtfile):
    # 讀 output.txt
    #with open(txtfile, encoding = 'utf-8-sig') as f:
    with open(txtfile, encoding='utf-8-sig', errors='ignore') as f:
        content = f.read().strip()
    #content = content.replace('________________', '')
    #print(content)
    return content

# txt's word to voice
def outcome(txtfile):
    
    
    if os.path.isfile(txtfile):
        word = getContent(txtfile)
        #print(word)
        """
            with open(txtfile, 'r') as f:
            word = f.read()
            #print(word)
            """
    else:
        print("\n[INFO] 沒有可讀取檔案.")
    
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=word, lang='zh-TW')
        tts.save('./result/outcome.mp3')
    
    sound = AudioSegment.from_mp3('./result/outcome.mp3')
    sound.export('./result/outcome.wav', format='wav')
    
    mixer.init()
    mixer.music.load('./result/outcome.wav')
    print("\n\n[INFO] 開始播放")
    screen=display.set_mode([200,50])
    mixer.music.play(0)
    clock= time.Clock()
    clock.tick(10)
    while mixer.music.get_busy():
        event.poll()
        clock.tick(10)


#outcome('./result/outcome.txt')
