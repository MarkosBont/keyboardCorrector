from pynput import keyboard
import pyperclip
import time
from pynput.keyboard import Controller, Key
import threading

eng_to_gre = {
    'q': ';', 'w': 'ς', 'e': 'ε', 'r': 'ρ', 't': 'τ',
    'y': 'υ', 'u': 'θ', 'i': 'ι', 'o': 'ο', 'p': 'π',
    'a': 'α', 's': 'σ', 'd': 'δ', 'f': 'φ', 'g': 'γ',
    'h': 'η', 'j': 'ξ', 'k': 'κ', 'l': 'λ',
    'z': 'ζ', 'x': 'χ', 'c': 'ψ', 'v': 'ω', 'b': 'β',
    'n': 'ν', 'm': 'μ',

    'Q': ':', 'W': 'Σ', 'E': 'Ε', 'R': 'Ρ', 'T': 'Τ',
    'Y': 'Υ', 'U': 'Θ', 'I': 'Ι', 'O': 'Ο', 'P': 'Π',
    'A': 'Α', 'S': 'Σ', 'D': 'Δ', 'F': 'Φ', 'G': 'Γ',
    'H': 'Η', 'J': 'Ξ', 'K': 'Κ', 'L': 'Λ',
    'Z': 'Ζ', 'X': 'Χ', 'C': 'Ψ', 'V': 'Ω', 'B': 'Β',
    'N': 'Ν', 'M': 'Μ',

    ';': '΄',  # (tonos)
    ':': '΅',  # Dialytika tonos
    '\'': '¨',  # Dialytika
    '`': '·'  # Greek middle dot
}

vowels = {
    'a': 'ά', 'e': 'έ', 'h': 'ή', 'i': 'ί', 'o': 'ό', 'u': 'ύ', 'v': 'ώ',
    'A': 'Ά', 'E': 'Έ', 'H': 'Ή', 'I': 'Ί', 'O': 'Ό', 'Y': 'Ύ', 'V': 'Ώ'
}

gre_to_eng = {v: k for k, v in eng_to_gre.items()}  # Reverse dictionary


def greek_eng(text):
    output = ''
    language = ''
    apply_tonos = False

    for character in text:
        if character in eng_to_gre.keys():
            if language == '':
                language = 'eng'
            if language == 'gre' and character != ';':
                return 'Mismatch'
        if character in gre_to_eng.keys():
            if language == '':
                language = 'gre'
            if language == 'eng' and character != ';':
                return 'Mismatch'

    for character in text:
        if language == 'eng':
            if character == ';':
                apply_tonos = True
                continue
            if character in eng_to_gre.keys():
                if apply_tonos:
                    output += vowels[character]
                    apply_tonos = False
                else:
                    output += eng_to_gre[character]
            else:
                output += character
        if language == 'gre':
            if character in gre_to_eng.keys():
                output += gre_to_eng[character]
            else:
                output += character

    return output


def apply_correct_s(text):
    output = ''
    for character in range(0, len(text)):
        if text[character] == 'σ' and ( (character + 1 < len(text) and text[character + 1] == ' ') or character == len(text) - 1):
            output += 'ς'
        else:
            output += text[character]

    return output





def correct_language(text):
    if not text:
        return ''

    result = greek_eng(text)
    if result == 'Mismatch':
        return 'Mismatch'

    first_char = result[0]
    if first_char in gre_to_eng:
        return apply_correct_s(result)
    elif first_char in eng_to_gre:
        return result
    else:
        # Unexpected character
        return result


# === Hotkey listener ===

stop_event = threading.Event()
keyboard_controller = Controller()
current_keys = set()

def on_press(key):
    try:
        if key.char:
            current_keys.add(key.char.lower())
    except AttributeError:
        current_keys.add(str(key))

    # Hotkey: ctrl + shift + t
    if {'t', 'Key.ctrl', 'Key.shift'} <= current_keys:
        threading.Thread(target=on_hotkey).start()  # run hotkey logic in a thread

def on_release(key):
    try:
        if key.char:
            current_keys.discard(key.char.lower())
    except AttributeError:
        current_keys.discard(str(key))

    # Optional: allow pressing ESC to quit (if debugging)
    if key == Key.esc:
        stop_event.set()
        return False

def on_hotkey():
    time.sleep(0.1)  # wait for Cmd+C to complete
    text = pyperclip.paste()
    fixed = correct_language(text)

    if fixed != 'Mismatch':
        pyperclip.copy(fixed)
        with keyboard_controller.pressed(Key.cmd):
            keyboard_controller.press('v')
            keyboard_controller.release('v')
    else:
        pass

# Start keyboard listener in the background
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Block main thread cleanly until stop_event is set
stop_event.wait()

# Cleanup
listener.stop()
listener.join()