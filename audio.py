# -*- coding: utf-8 -*-
import os
import tempfile
from gtts import gTTS
from pydub import AudioSegment

def getContent(txtfile):
    # 讀 output.txt
    #with open(txtfile, encoding = 'utf-8-sig') as f:
    with open(txtfile, encoding='utf-8') as f:
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
        print("[INFO] 圖像無法識別請於提示音後重新操作.")
    
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=word, lang='zh-TW')
        tts.save('./result/outcome.mp3')
    
    sound = AudioSegment.from_mp3('./result/outcome.mp3')
    sound.export('./result/outcome.wav', format='wav')


#outcome('./result/outcome.txt')
