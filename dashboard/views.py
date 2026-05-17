import requests, json
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST   
from .models import ChatConversation, ChatMessage

OLLAMA_API_URL = "http://localhost:11434/api/chat"

@login_required
def dashboard_home(request):
    user_chats = request.user.chats.all().order_by('-created_at')

    if request.method == "POST":
        prompt = request.POST.get('prompt', '').strip()
        selected_model = request.POST.get('model_name', 'qwen2.5:3b')
        temperature = request.POST.get('temperature', '0.7')
        rag_context = request.POST.get('rag_context', 'all')
        top_k = request.POST.get('top_k', '4')
        
        if prompt:
            chat = ChatConversation.objects.create(user=request.user, title=prompt[:30] + "...")
            
            ChatMessage.objects.create(conversation=chat, role='user', content=prompt)

            base_url = reverse('chat_detail', args=[chat.id])
            query_params = (
                f"?first_msg=true"
                f"&model_name={selected_model}"
                f"&temperature={temperature}"
                f"&rag_context={rag_context}"
                f"&top_k={top_k}"
            )
            return redirect(f"{base_url}{query_params}")

    return render(request, 'dashboard/index.html', {'user_chats': user_chats})

@login_required
def chat_detail(request, chat_id):
    user_chats = request.user.chats.all().order_by('-created_at')
    chat = get_object_or_404(ChatConversation, id=chat_id, user=request.user)
    messages = chat.messages.all().order_by('created_at')

    last_assistant_msg = messages.filter(role='assistant').last()
    current_model = last_assistant_msg.model_used if last_assistant_msg else 'llama3'

    return render(request, 'dashboard/chat_room.html', {
        'chat': chat,
        'messages': messages,
        'user_chats': user_chats,
        'current_model': current_model
    })
    
@login_required
@require_POST
def rename_chat(request, chat_id):
    chat = get_object_or_404(ChatConversation, id=chat_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        new_title = data.get('title', '').strip()
        
        if new_title:
            chat.title = new_title
            chat.save()
            return JsonResponse({'success': True, 'new_title': chat.title})
        
        return JsonResponse({'success': False, 'error': 'Invalid name'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid payload'}, status=400)


@login_required
@require_POST
def delete_chat(request, chat_id):
    chat = get_object_or_404(ChatConversation, id=chat_id, user=request.user)
    chat.delete()
    
    redirect_url = reverse('dashboard_home') 
    
    return JsonResponse({'success': True, 'redirect_url': redirect_url})

@login_required
@require_POST
def chat_stream(request, chat_id):
    chat = get_object_or_404(ChatConversation, id=chat_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt')
        temperature = float(data.get('temperature', 0.7))
        selected_model = data.get('model_name', 'qwen2.5:3b')
        is_first_msg = data.get('is_first_msg', False)

        if not prompt:
            return JsonResponse({'error': 'Prompt vazio'}, status=400)

        if not is_first_msg:
            ChatMessage.objects.create(conversation=chat, role='user', content=prompt)

        messages = chat.messages.all().order_by('created_at')
        history = []
        for msg in messages:
            history.append({"role": msg.role, "content": msg.content})

        payload = {
            "model": selected_model,
            "messages": history,
            "options": {"temperature": temperature},
            "stream": True
        }

        def stream_generator():
            full_ai_response = ""
            try:
                response = requests.post(OLLAMA_API_URL, json=payload, stream=True, timeout=60)
                
                if response.status_code != 200:
                    try:
                        error_json = response.json()
                        error_msg = f"[Ollama error]: {error_json.get('error')}"
                    except:
                        error_msg = f"[Ollama error]: The server returned a {response.status_code} status."
                    
                    yield error_msg
                    ChatMessage.objects.create(conversation=chat, role='assistant', content=error_msg, model_used=selected_model)
                    return
                
                for line in response.iter_lines():
                    if line:                        
                        chunk_data = json.loads(line.decode('utf-8'))
                        text_chunk = chunk_data.get('message', {}).get('content', '')
                        
                        if text_chunk:
                            full_ai_response += text_chunk
                            yield text_chunk

                ChatMessage.objects.create(
                    conversation=chat, 
                    role='assistant', 
                    content=full_ai_response, 
                    model_used=selected_model
                )

            except Exception as e:
                error_msg = "\n[Ollama connection error]"
                yield error_msg
                ChatMessage.objects.create(conversation=chat, role='assistant', content=error_msg, model_used=selected_model)

        return StreamingHttpResponse(stream_generator(), content_type='text/plain')

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)