# tts mp3 파일 생성하는 코드
from gtts import gTTS

"""
def save_voice(text, filename):
    tts = gTTS(text=text, lang='ko')
    tts.save(filename)

save_voice('느려요', 'voice/slow.mp3')
save_voice('빨라요', 'voice/fast.mp3')
save_voice('좋아요', 'voice/good.mp3')
"""

korean = ['하나', '둘', '셋', '넷', '다섯', '여섯', '일곱', '여덟', '아홉', '열']
english = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']


for index, value in enumerate(korean):
    tts = gTTS(text=value, lang='ko')
    tts.save(f'voice/{index + 1}.mp3')