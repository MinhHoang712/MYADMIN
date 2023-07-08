from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests, os
import time

from my_admin.settings import BASE_DIR
audio_id = 1

def home(request):
    audio_path = request.GET.get('audio_path')
    if audio_path:
        print("Get OK : ", audio_path)
    else :
        print("Fail to get:", audio_path)
    context = {
        'audio_path': audio_path
    }
    return render(request, 'myapp/index.html', context)

def make_audio(request):
    url = 'https://api.fpt.ai/hmi/tts/v5'
    if request.method == 'GET':
        return JsonResponse({'error' : "Sai phương thức"})
    if request.method == 'POST':
        payload = request.POST.get('message')

        headers = {
            'api-key': 'QZjlL4U8P8HMRNpj6Q7ZB6XUTFTbxhGV',
            'speed': '',
            'voice': 'banmai'
        }

        response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)

        if response.json()["error"] != 0:
            print(response.json()["message"])
            raise ValueError()
        
        time.sleep(2)

        audio_url = response.json()["async"]

        global audio_id 
        audio_id += 1
        audio_path = os.path.join(os.path.join(BASE_DIR, "myapp", 'static'), f'audio{audio_id}.mp3')

        with open(audio_path, 'wb') as audio_file:
            audio_file.write(requests.get(audio_url).content)
        return redirect(f'/audio?audio_id={audio_id}')
    return JsonResponse({'error': 'Invalid request'})
