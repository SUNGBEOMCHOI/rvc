import os
import sys
ai_project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
uvr_project_path = os.path.join(ai_project_path, 'python-audio-separator')
sys.path.append(uvr_project_path)

import configparser

from audio_separator.separator import Separator

class VoiceSeparationModule:
    def __init__(self, config_path=os.path.join(ai_project_path, 'voice_separation_config.ini')):
        config = self.load_config(config_path)
        self.separator = self.create_separator(config)

    def voice_separation(self, music_path, save_root_vocal, save_root_ins, callback=None):
        vocal_path, ins_path = self.separator.separate(music_path, save_root_vocal, save_root_ins)
        if callback:
            callback(vocal_path, ins_path)
        return vocal_path, ins_path
    
    def create_separator(self, config):
        mdx_params = {
            "hop_length": config.getint('mdx', 'hop_length'),
            "segment_size": config.getint('mdx', 'segment_size'),
            "overlap": config.getfloat('mdx', 'overlap'),
            "batch_size": config.getint('mdx', 'batch_size'),
            "enable_denoise": config.getboolean('mdx', 'enable_denoise'),
        }

        separator = Separator(
            model_file_dir=config.get('general', 'model_file_dir'),
            output_format=config.get('general', 'output_format'),
            sample_rate=config.getint('general', 'sample_rate'),
            mdx_params=mdx_params,
        )

        separator.load_model(model_filename=config.get('general', 'model_name'))

        return separator

    def load_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        return config
    
if __name__ == '__main__':
    voice_separation_module = VoiceSeparationModule()
    
    # Test voice separation
    music_path = '/home/choi/desktop/rvc/ai/data/user2/input/music/origin_music.mp3'
    save_root_vocal = '/home/choi/desktop/rvc/ai/data/user2/output/music'
    save_root_ins = '/home/choi/desktop/rvc/ai/data/user2/output/music'
    voice_separation_module.voice_separation(music_path, save_root_vocal, save_root_ins)