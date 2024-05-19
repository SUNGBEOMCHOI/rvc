import os
import sys
ai_project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rvc_project_path = os.path.join(ai_project_path, 'Retrieval-based-Voice-Conversion-WebUI')
print(rvc_project_path)
sys.path.append(rvc_project_path)

import configparser
import ffmpeg

from infer.modules.vc.modules import VC
from configs.config import Config as RVCConfig
# from modules.voice_mr_separation.voice_separation import uvr, initialize_voice_separation_model
from modules.infer.inference import rvc_inference
from modules.infer.mix_voice_instrument import mix_voice_and_instrument
from modules.train.preprocess import preprocess_dataset
from modules.train.extract_feature import extract_f0_feature
from modules.train.train import click_train
from modules.train.train_index import train_index

class VoiceConversionModule:
    def __init__(self, config_path=os.path.join(ai_project_path, 'config.ini')):
        rvc_config = RVCConfig()
        config = self.load_config(config_path)
        
        self.voice_separation_args = self.setting_config(config, 'VOICE_SEPARATION')
        self.inference_config = self.setting_config(config, 'VOICE_INFERENCE')
        self.train_args = self.setting_config(config, 'VOICE_TRAIN')
        self.train_args['pretrained_g'] = os.path.join(rvc_project_path, self.train_args.get('pretrained_g'))
        self.train_args['pretrained_d'] = os.path.join(rvc_project_path, self.train_args.get('pretrained_d'))
        
        self.voice_model = VC(rvc_config)        
        # self.voice_separation_model = initialize_voice_separation_model(self.voice_separation_args)

    def voice_separation(self, music_path, save_root_vocal, save_root_ins, format='wav', callback=None):  
        # voice_path, instrument_path = uvr(self.voice_separation_model, music_path, save_root_vocal, save_root_ins, format)
        # if callback:
        #     callback(voice_path, instrument_path)
        # return voice_path, instrument_path
        raise NotImplementedError

    def inference(self, voice_model_path, input_voice_path, input_instrument_path, output_voice_path, output_mix_path, index_path, callback=None):
        output_voice_path = rvc_inference(self.voice_model, voice_model_path, input_voice_path, output_voice_path, index_path, self.inference_config)
        output_mix_path = mix_voice_and_instrument(output_voice_path, input_instrument_path, output_mix_path)
        if callback:
            callback(output_voice_path, output_mix_path)
        return output_voice_path, output_mix_path

    def train(self, voice_dir, output_dir, callback=None):
        preprocess_dataset(voice_dir, output_dir, self.train_args)
        extract_f0_feature(output_dir, self.train_args)
        trained_voice_path = click_train(output_dir, self.train_args)
        trained_index_path = train_index(output_dir, self.train_args)
        if callback:
            callback(trained_voice_path, trained_index_path)
        return trained_voice_path, trained_index_path

    def setting_config(self, config, config_name):
        return {k: self.cast_config_value(v) for k, v in config[config_name].items()}
    
    def cast_config_value(self, value):
        # Check for boolean strings specifically
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False

        # Attempt to convert the config values to int or float if applicable
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value  # Return as string if neither int nor float

    def load_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        return config

if __name__ == "__main__":
    voice_conversion_module = VoiceConversionModule()

    # Test voice separation
    # music_path = '/home/choi/desktop/rvc/ai/data/user2/input/music/origin_music.mp3'
    # save_root_vocal = '/home/choi/desktop/rvc/ai/data/user2/output/music'
    # save_root_ins = '/home/choi/desktop/rvc/ai/data/user2/output/music'
    # voice_conversion_module.voice_separatiopretrained_G14n(music_path, save_root_vocal, save_root_ins)

    # Test training
    # voice_dir = '/home/choi/desktop/rvc/ai/data/user2/input/speaker'
    # output_dir = '/home/choi/desktop/rvc/ai/data/user2/output/trained_model'
    # trained_voice_path, trained_index_path = voice_conversion_module.train(voice_dir, output_dir)
    # print(trained_voice_path, trained_index_path)

    # Test voice conversion
    # voice_model_path = '/home/choi/desktop/rvc/ai/data/user2/output/trained_model/trained_voice.pth'
    # input_voice_path = '/home/choi/desktop/rvc/ai/data/user2/output/music/vocal_origin_music.mp3.wav'
    # input_instrument_path = '/home/choi/desktop/rvc/ai/data/user2/output/music/instrument_origin_music.mp3.wav'
    # output_voice_path = '/home/choi/desktop/rvc/ai/data/user2/output/cover/output.wav'
    # output_mix_path = '/home/choi/desktop/rvc/ai/data/user2/output/cover/output_final.wav'
    # index_path = '/home/choi/desktop/rvc/ai/data/user2/output/trained_model/trained_index.index'
    # voice_conversion_module.inference(voice_model_path, input_voice_path, input_instrument_path, output_voice_path, output_mix_path, index_path)
