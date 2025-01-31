# video_clipper/views.py
from django.shortcuts import render
from .utils import find_song_data
import os

def video_clipper_view(request):
    if request.method == "POST":
        youtube_url = request.POST.get('youtube_url')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        quality = request.POST.get('quality', '720p')
        file_path = request.POST.get('file_path')
        video_download = request.POST.get('video_download')

        # if start_time and end_time:
        #     start_time = convert_to_seconds(start_time)
        #     end_time = convert_to_seconds(end_time)

        if not file_path:
            if os.name == 'nt':
                file_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
            else:
                file_path = os.path.join(os.environ['HOME'], 'Downloads')

        download_completed = find_song_data(youtube_url, file_path, start_time, end_time, video_download, quality)
        if download_completed:
            if start_time:
                return render(request, 'index.html', {"message":"Trimmed Video Downloaded Successfully..."})
            if start_time and video_download:
                return render(request, 'index.html', {"message":"Trimmed And Original Video Downloaded Successfully..."})
            return render(request, 'index.html', {"message":"Video Downloaded Successfully..."})
        else:
            return render(request, 'index.html', {"message": "Failed to process video..."})
    return render(request, 'index.html')





