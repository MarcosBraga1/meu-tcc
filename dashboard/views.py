import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatConversation, ChatMessage

OLLAMA_API_URL = "http://localhost:11434/api/chat"

@login_required
def dashboard_home(request):
    user_chats = request.user.chats.all().order_by('-created_at')

    if request.method == "POST":
        prompt = request.POST.get('prompt')
        temperature = float(request.POST.get('temperature', 0.7))
        selected_model = request.POST.get('model_name', 'llama3')

        if prompt:
            chat = ChatConversation.objects.create(user=request.user, title=prompt[:30] + "...")
            
            ChatMessage.objects.create(conversation=chat, role='user', content=prompt)

            payload = {
                "model": selected_model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "options": {
                    "temperature": temperature
                },
                "stream": False
            }

            try:
                response = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
                if response.status_code == 200:
                    response_data = response.json()
                    ai_response = response_data['message']['content']
                    
                    ChatMessage.objects.create(conversation=chat, role='assistant', content=ai_response, model_used=selected_model)
            except requests.exceptions.RequestException:
                ChatMessage.objects.create(
                    conversation=chat, 
                    role='assistant', 
                    content="Error: Could not connect to the local Ollama server. Please ensure the service is running (`ollama serve`).",
                    model_used=selected_model
                )

            return redirect('chat_detail', chat_id=chat.id)

    return render(request, 'dashboard/index.html', {'user_chats': user_chats})

@login_required
def chat_detail(request, chat_id):
    user_chats = request.user.chats.all().order_by('-created_at')
    chat = get_object_or_404(ChatConversation, id=chat_id, user=request.user)
    messages = chat.messages.all().order_by('created_at')

    if request.method == "POST":
        prompt = request.POST.get('prompt')
        temperature = float(request.POST.get('temperature', 0.7))
        selected_model = request.POST.get('model_name', 'llama3')

        if prompt:
            ChatMessage.objects.create(conversation=chat, role='user', content=prompt)

            history = []
            for msg in messages:
                history.append({"role": msg.role, "content": msg.content})
            history.append({"role": "user", "content": prompt})

            payload = {
                "model": selected_model,
                "messages": history,
                "options": {"temperature": temperature},
                "stream": False
            }

            try:
                response = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
                if response.status_code == 200:
                    ai_response = response.json()['message']['content']
                    ChatMessage.objects.create(conversation=chat, role='assistant', content=ai_response, model_used=selected_model)
            except requests.exceptions.RequestException:
                ChatMessage.objects.create(conversation=chat, role='assistant', content="Connection error with Ollama.", model_used=selected_model)

            return redirect('chat_detail', chat_id=chat.id)

    last_assistant_msg = messages.filter(role='assistant').last()
    current_model = last_assistant_msg.model_used if last_assistant_msg else 'llama3'

    return render(request, 'dashboard/chat_room.html', {
        'chat': chat,
        'messages': messages,
        'user_chats': user_chats,
        'current_model': current_model
    })