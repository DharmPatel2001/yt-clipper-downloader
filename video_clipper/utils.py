import yt_dlp
import os
import ffmpeg

def get_video_quality(youtube_url):
    """ Get available video formats from YouTube using yt-dlp """
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        formats = info_dict.get('formats', [])
        available_qualities = [f['height'] for f in formats if 'height' in f and f['ext'] == 'mp4']
        return available_qualities

def delete_mp3_and_webm_files(directory=".", video_filename=None, video_not_download=False):
    """Delete all MP3 and WebM files in the specified directory."""
    files_in_directory = os.listdir(directory)
    deleted_files = []
    for file_name in files_in_directory:
        if video_not_download:
            if file_name.replace("｜", "|").startswith(video_filename):
                file_path = os.path.join(directory, file_name)
                try:
                    os.remove(file_path)  # Delete the file
                    deleted_files.append(file_name)
                except Exception as e:
                    print(f"Error deleting file {file_name}: {e}")
        elif file_name.replace("｜", "|").startswith(video_filename):
            if file_name.endswith('.m4a') or file_name.endswith('.webm') or 'f396' in file_name:
                file_path = os.path.join(directory, file_name)
                try:
                    os.remove(file_path)  # Delete the file
                    deleted_files.append(file_name)
                except Exception as e:
                    print(f"Error deleting file {file_name}: {e}")
    if deleted_files:
        print(f"Deleted files: {', '.join(deleted_files)}")
    else:
        print("No MP3 or WebM files found to delete.")

def clip_video(input_file, output_file, output_directory, start_time, end_time, video_download):
    """ Clip the video from start_time to end_time using ffmpeg. """
    print("-------output_file-------",input_file)
    if os.path.exists(input_file):
        if os.path.exists(output_file):
            return {"message":"This Clip Already Exist your system"}
        output_file = os.path.join(output_directory, output_file) 
        ffmpeg.input(input_file, ss=start_time, to=end_time).output(output_file).run()
        return {"message":"Trimmed Video Downloaded Successfully..."}
    else:
        print(f"Error: File {input_file} not found.")


def find_song_data(youtube_url, file_path, start_time, end_time, video_download, quality="720p"):
    available_qualities = get_video_quality(youtube_url)
    print("Available video qualities:", available_qualities)
    requested_quality = int(quality.replace("p", ""))
    if requested_quality not in available_qualities:
        print(f"Error: Requested quality {quality} is not available. Available qualities are: {available_qualities}")
        return None

    video_format = f'bestvideo[height<={requested_quality}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
    
    ydl_opts = {
        'format': video_format,
        'outtmpl': os.path.join(file_path, '%(title)s.%(ext)s'),
        'embedthumbnail': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'noplaylist': True,
        'keepvideo': True,
        # Fixes for 403 Forbidden
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.youtube.com/',
        },
        'cookiefile': 'cookies.txt',  # Ensure cookies.txt exists if login is required
        'force_generic_extractor': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        video_filename = ydl.prepare_filename(info_dict)
    
    print(f"Video downloaded to: {video_filename}")
    
    if not start_time and not end_time:
        delete_mp3_and_webm_files(directory=file_path, video_filename=info_dict["title"])

    if start_time is not None and end_time is not None:
        title = info_dict["title"]
        clipped_video_filename = f"clip_{title}_{start_time}_{end_time}_{requested_quality}p.mp4"
        clip = clip_video(video_filename, clipped_video_filename, file_path, start_time, end_time, video_download)
        print(f"Clipped video saved to: {clipped_video_filename}")
        
        if video_download:
            delete_mp3_and_webm_files(directory=file_path, video_filename=info_dict["title"])
        else:
            delete_mp3_and_webm_files(directory=file_path, video_filename=info_dict["title"], video_not_download=True)

    return video_filename


# def convert_to_seconds(time_str):
#     minutes, seconds = map(int, time_str.split(":"))
#     total_seconds = minutes * 60 + seconds
#     return total_seconds