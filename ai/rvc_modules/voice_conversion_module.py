import os
import sys
ai_project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rvc_project_path = os.path.join(ai_project_path, 'Retrieval-based-Voice-Conversion-WebUI')
print(rvc_project_path)
sys.path.append(rvc_project_path)

import configparser
import ffmpeg

from modules.voice_mr_separation.voice_separation import uvr, initialize_voice_separation_model

def load_config():
    config = configparser.ConfigParser()
    config.read('/home/choi/desktop/rvc/ai/rvc_modules/config.ini')
    return config



class VoiceConversionModule:
    def __init__(self, ):
        config = load_config()
        print(config)
        
        
        # Setting up voice separation model
        self.voice_separation_config = config['VOICE_SEPARATION']
        model_name = self.voice_separation_config.get('model_name')
        agg = self.voice_separation_config.getint('agg')
        device = self.voice_separation_config.get('device')
        is_half = self.voice_separation_config.getboolean('is_half')
        self.voice_separation_model = initialize_voice_separation_model(model_name, agg, device, is_half)

    def voice_separation(self, music_path, save_root_vocal, save_root_ins):
        agg = self.voice_separation_config.get('agg')
        format0 = self.voice_separation_config.get('format')
        
        uvr(self.voice_separation_model, music_path, save_root_vocal, save_root_ins, agg, format0)


if __name__ == "__main__":

    # Test voice separation
    music_path = '/home/choi/desktop/rvc/ai/data/user2/input/music/origin_music.mp3'
    save_root_vocal = '/home/choi/desktop/rvc/ai/data/user2/output/music'
    save_root_ins = '/home/choi/desktop/rvc/ai/data/user2/output/music'

    voice_conversion_module = VoiceConversionModule()
    voice_conversion_module.voice_separation(music_path, save_root_vocal, save_root_ins)