#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@title: youtube.py
@author: Yiğit GÜMÜŞ
@date: 2025-03-16 18:57:57
@description: Bu dosya YouTube'dan video indirme işlemlerini ve ek özellikleri gerçekleştirir.
"""

from pytubefix import (
  YouTube,
  Search,
  Channel,
  Playlist
)
from pytubefix.cli import on_progress
import ffmpeg

from pathlib import Path
import os
import tempfile

class YouTubeAPI:
  def __init__(self, folder_name: str = 'videos'):
    self.default_folder_name = folder_name


  def download_video(self, video_url: str) -> None:
    """
    YouTube'dan video indirir

    Args:
      video_url: İndirilecek video URL'si
      folder_path: İndirilen video dosyasının kaydedileceği yol
    """
    try:

      # Youtube Client
      yt = YouTube(video_url, on_progress_callback=on_progress)

      # Dosya adını belirleme
      filename = yt.title

      Path(filename+'.mp4').touch()

      # Video ve Ses Streamlerini al
      video_stream = yt.streams.get_highest_resolution()
      audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

      # Video ve sesi indir.
      temp_dir = tempfile.gettempdir()

      video_file_name = filename+'_video.mp4'
      audio_file_name = filename+'_audio.mp4'

      file_paths = [
        filename+'.mp4',
        os.path.join(temp_dir, video_file_name),
        os.path.join(temp_dir, audio_file_name)
      ]
      for fp in file_paths:
        if os.path.exists(fp):
            os.remove(fp)

      video_path = video_stream.download(output_path=temp_dir, filename=video_file_name)
      audio_path = audio_stream.download(output_path=temp_dir, filename=audio_file_name)

      # Video ve sesi birleştir
      video_input = ffmpeg.input(video_path)
      audio_input = ffmpeg.input(audio_path)


      merge_output = ffmpeg.output(video_input, audio_input, filename+'.mp4', format='mp4', vcodec="copy", acodec="aac")

      merge_output.run(overwrite_output=True)

      # Dosyaları sil
      os.remove(video_path)
      os.remove(audio_path)
    except Exception as e:
      print(f'Error: {e}')
      print('Video download failed!')

  def download_playlist(self, playlist_url: str, folder_name: str | None) -> None:
    """
    YouTube'dan playlist indirir

    Args:
      playlist_url: İndirilecek playlist URL'si
      folder_name: İndirilen videoların kaydedileceği klasör adı
    """
    if folder_name in [None, '']:
      folder_name = self.default_folder_name

    Path(folder_name).mkdir(parents=True, exist_ok=True)
    for video in Playlist(playlist_url).videos:
      ys = video.streams.get_highest_resolution()
      print(f'Downloading: {video.title}')
      ys.download(folder_name)
      print('Downloaded:', video.title)


  def search_videos(self, query: str, max_results: int = 10):
    '''
    Video araması yapar ve sonuçları ekrana yazdırır

    Args:
      query: Aranacak video adı
      max_results: Arama sonuçlarının maksimum sayısı
    '''
    for video, _ in zip(Search(query).videos, range(max_results)):
        print('----------------------------------')
        print(f'Title: {video.title}')
        print(f'URL: {video.watch_url}')
        print(f'Duration: {video.length} sec')
        print(f'Views: {video.views}')

  def detailed_search_videos(self, query: str, max_results: int = 10) -> None:
    '''
    Detaylı video araması yapar ve sonuçları ekrana yazdırır

    Args:
      query: Aranacak video adı
      max_results: Arama sonuçlarının maksimum sayısı
    '''

    for video, _ in zip(Search(query).videos, range(max_results)):
        print('--------------------------------------------------------------')
        print(f'Title: {video.title}')
        print(f'URL: {video.watch_url}')
        print(f'Duration: {video.length} sec')
        print(f'Views: {video.views}')
        print(f'Channel ID: {video.channel_id}')
        print(f'Channel URL: {video.channel_url}')
        print(f'Channel Name: {Channel(video.channel_url).channel_name}')
        print(f'Published: {video.publish_date}')
        print('------------------------------------------')
        print(f'Description:\n{video.description}')
        print('--------------------------------------------------------------', end=5*'\n')


if __name__ == '__main__':
  yt = YouTubeAPI()
  yt.download_video('https://www.youtube.com/watch?v=9bZkp7q19f0')
