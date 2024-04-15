import argparse
import yt_dlp as youtube_dl

def download_audio(video_url, output_path):
    # Extract the file extension and validate it
    file_name, file_extension = ".".join(output_path.split('.')[:-1]), output_path.split('.')[-1]
    if file_extension not in ['mp3', 'wav']:
        raise ValueError("Unsupported format. Please choose 'mp3' or 'wav'.")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': file_extension,
            'preferredquality': '192',
        }],
        'outtmpl': file_name,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def arg_parse():
    parser = argparse.ArgumentParser(description='Download audio from YouTube video')
    parser.add_argument('--video_url', type=str, help='YouTube video URL', default='https://www.youtube.com/watch?v=FTA-19ZMdCk')
    parser.add_argument('--output_path', type=str, help='Output path for the audio file, including format', default='downloaded_audio.mp3')
    return parser.parse_args()

def main():
    args = arg_parse()
    download_audio(args.video_url, args.output_path)

if __name__ == '__main__':
    main()
