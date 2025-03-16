#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@title: drive.py
@author: Yiğit GÜMÜŞ
@date: 2025-03-16 20:33:59
@description: Bu dosya Google Drive ile ilgili işlemleri gerçekleştirir.
"""
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

import os

from settings import PROJECT_NAME

def upload_to_drive(file_path, file_name=None, target_folder_id=None):
  """
  pydrive2 kullanarak yerel dosyayı Google Drive'a yükler

  Args:
    file_path: Yüklenecek dosyanın tam yolu
    file_name: Drive'a yüklenecek dosyanın adı (belirtilmezse orijinal dosya adı kullanılır)

  Returns:
    Yüklenen dosyanın Drive'daki ID'si
  """
  # Eğer dosya adı belirtilmemişse, orijinal dosya adını kullan
  if not file_name:
    file_name = os.path.basename(file_path)

  # Google Drive kimlik doğrulama
  gauth = GoogleAuth()

  # Otomatik kimlik doğrulama veya mevcut credentials.json dosyasını kullan
  # Eğer kimlik doğrulama bilgileri yoksa yeni bir tarayıcı açılacak
  gauth.LocalWebserverAuth()

  # Google Drive'a bağlan
  drive = GoogleDrive(gauth)

  # Yüklenecek dosyayı oluştur
  file_drive = drive.CreateFile({'title': file_name})

  # Dosya içeriğini ayarla
  file_drive.SetContentFile(file_path)

  # Dosyayı yükle
  file_drive.Upload()

  print(f"Dosya başarıyla yüklendi. Dosya ID: {file_drive['id']}")
  return file_drive['id']

def create_folder_at_drive(folder_name: str, folder_path: str | None = None) -> str:
  """
  pydrive2 kullanarak Google Drive'da yeni bir klasör oluşturur

  Args:
    folder_name: Oluşturulacak klasörün adı

  Returns:
    Oluşturulan klasörün ID'si
  """
  # Google Drive kimlik doğrulama
  gauth = GoogleAuth()

  # Otomatik kimlik doğrulama veya mevcut credentials.json dosyasını kullan
  # Eğer kimlik doğrulama bilgileri yoksa yeni bir tarayıcı açılacak
  gauth.LocalWebserverAuth()

  # Google Drive'a bağlan
  drive = GoogleDrive(gauth)

  # Oluşturulacak klasörü oluştur
  folder_drive = drive.CreateFile({
    'title': folder_name,
    'mimeType': 'application/vnd.google-apps.folder'}
  )

  # Klasörü oluştur
  folder_drive.Upload()

  print(f"Klasör başarıyla oluşturuldu. Klasör ID: {folder_drive['id']}")
  return folder_drive['id']

def upload_files_to_drive(files: list[str], folder_id: str | None = None):
  """
  Google Drive'a birden fazla dosya yükler

  Args:
    files: Yüklenecek dosyaların yolları
    folder_id: Dosyaların yükleneceği klasörün ID'si
  """
  # Google Drive kimlik doğrulama
  gauth = GoogleAuth()

  # Otomatik kimlik doğrulama veya mevcut credentials.json dosyasını kullan
  # Eğer kimlik doğrulama bilgileri yoksa yeni bir tarayıcı açılacak
  gauth.LocalWebserverAuth()

  # Google Drive'a bağlan
  drive = GoogleDrive(gauth)

  if folder_id is None:
    # Eğer klasör ID'si belirtilmemişse, yeni bir klasör oluştur
    folder_id = create_folder_at_drive(PROJECT_NAME)

  # Dosyaları yükle
  for file_path in files:
    file_name = os.path.basename(file_path)
    file_drive = drive.CreateFile({
      'title': file_name,
      'parents': [{"kind": "drive#fileLink", 'id': folder_id}]
    })
    file_drive.SetContentFile(file_path)
    file_drive.Upload()

    print(f"{file_name} başarıyla yüklendi. Dosya ID: {file_drive['id']}")

if __name__ == '__main__':
  # Dosyanın yolu
  file_path = 'test.txt'

  # Dosyayı Google Drive'a yükle
  upload_to_drive(file_path)
