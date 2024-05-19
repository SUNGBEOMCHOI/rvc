import os
import sys
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(project_path)

import time
from queue import Queue
from threading import Thread

from ai.rvc_modules.voice_conversion_module import VoiceConversionModule
from ai.rvc_modules.voice_separation_module import VoiceSeparationModule

class VoiceConversionManager:
    _instance = None
    _voice_conversion_module = None
    _voice_separation_module = None
    _request_queue = Queue()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VoiceConversionManager, cls).__new__(cls)
            cls._voice_conversion_module = VoiceConversionModule()
            cls._voice_separation_module = VoiceSeparationModule()
            cls._start_request_handler()
        return cls._instance

    @classmethod
    def _start_request_handler(cls):
        def handle_requests():
            while True:
                if not cls._request_queue.empty():
                    request = cls._request_queue.get()
                    if request is None:  # Stop signal received
                        break
                    cls._process_request(request)
                    cls._request_queue.task_done()
                time.sleep(1)  # Check the queue every 1 second
                print('VoiceConversionManager: handle_requests, request_queue size:', cls._request_queue.qsize())

        thread = Thread(target=handle_requests)
        thread.daemon = True
        thread.start()

    @classmethod
    def _process_request(cls, request):
        method_name, args, kwargs = request
        if method_name == 'voice_separation':
            method = getattr(cls._voice_separation_module, method_name)
        else:
            method = getattr(cls._voice_conversion_module, method_name)
        print('VoiceConversionManager: _process_request, method:', method_name, 'args:', args, 'kwargs:', kwargs)
        method(*args, **kwargs)

    def get_voice_conversion_module(self):
        return self._voice_conversion_module

    def voice_separation(self, music_path, save_root_vocal, save_root_ins, callback=None):
        self._request_queue.put(('voice_separation', (music_path, save_root_vocal, save_root_ins, callback), {}))

    def inference(self, voice_model_path, input_voice_path, input_instrument_path, output_voice_path, output_mix_path, index_path, callback=None):
        self._request_queue.put(('inference', (voice_model_path, input_voice_path, input_instrument_path, output_voice_path, output_mix_path, index_path, callback), {}))

    def train(self, voice_dir, output_dir, callback):
        self._request_queue.put(('train', (voice_dir, output_dir, callback), {}))

    def stop_request_handler(self):
        self._request_queue.put(None)
        self._request_queue.join()  # Wait for the queue to be empty

def get_voice_conversion_manager():
    return VoiceConversionManager()