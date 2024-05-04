import os
import sys
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(project_path)

from ai.rvc_modules.voice_conversion_module import VoiceConversionModule

class VoiceConversionManager:
    _instance = None
    _voice_conversion_module = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VoiceConversionManager, cls).__new__(cls)
            cls._voice_conversion_module = VoiceConversionModule()
        return cls._instance
    
    def get_voice_conversion_module(self):
        return self._voice_conversion_module