from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pynput', 'pyperclip', 'setuptools'],
    'includes': ['pkg_resources', 'jaraco.text'],
    'plist': {
        'CFBundleName': 'Keyboard Translator',
        'CFBundleIdentifier': 'com.yourname.keyboardtranslator',
        'CFBundleVersion': '0.1.0',
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)