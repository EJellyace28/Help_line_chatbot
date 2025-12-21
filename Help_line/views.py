from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import os
from dotenv import load_dotenv
from groq import Groq
from .models import Chat, Message

# Load environment variables and configure Groq
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
print(f"Groq API Key loaded: {'Yes' if api_key else 'NO'}")
client = Groq(api_key=api_key)

# System prompt for the AI assistant
SYSTEM_PROMPT = """You are Calm Companion, a warm, empathetic, and supportive AI assistant focused on mental wellness and emotional support. 

Your personality:
- Compassionate and understanding
- A good listener who validates feelings
- Provides helpful suggestions without being preachy
- Uses calming, reassuring language
- Encourages self-care and positive coping strategies

Guidelines:
- Keep responses concise but meaningful (2-4 sentences typically)
- Ask follow-up questions to understand the user better
- Never give medical advice - suggest professional help when appropriate
- Be supportive without being dismissive of real concerns
- Use a warm, friendly tone"""

def landing_view(request):
    """Landing page view"""
    return render(request, 'pages/landing.html')

def login_view(request):
    """Login page view"""
    if request.method == 'POST':
        email = request.POST.get('loginEmail')
        password = request.POST.get('loginPassword')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            print(f"User {user.username} logged in successfully")
            return redirect('chat')
        else:
            messages.error(request, 'Invalid email or password')
            print("Authentication failed")
    
    return render(request, 'pages/login.html')

def register_view(request):
    """Registration page view"""
    if request.method == 'POST':
        name = request.POST.get('registerName')
        email = request.POST.get('registerEmail')
        password = request.POST.get('registerPassword')
        confirm_password = request.POST.get('registerConfirmPassword')
        
        print(f"Registration attempt: {name}, {email}")
        
        if not all([name, email, password, confirm_password]):
            messages.error(request, 'All fields are required')
            return render(request, 'pages/register.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'pages/register.html')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            return render(request, 'pages/register.html')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'pages/register.html')
        
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
            user.save()
            
            print(f"User {email} created successfully")
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
            
        except Exception as e:
            print(f"Error creating user: {e}")
            messages.error(request, 'Error creating account. Please try again.')
            return render(request, 'pages/register.html')
    
    return render(request, 'pages/register.html')

@login_required(login_url='login')
def chat_view(request, chat_id=None):
    """Chat interface view - shows all chats and current conversation"""
    user_chats = Chat.objects.filter(user=request.user)
    current_chat = None
    messages_list = []
    
    if chat_id:
        current_chat = get_object_or_404(Chat, id=chat_id, user=request.user)
        messages_list = current_chat.messages.all()
    
    return render(request, 'pages/chat.html', {
        'user_name': request.user.first_name or request.user.username,
        'chats': user_chats,
        'current_chat': current_chat,
        'messages': messages_list,
    })

@login_required(login_url='login')
@require_http_methods(["POST"])
def create_chat(request):
    """Create a new chat"""
    try:
        chat = Chat.objects.create(
            user=request.user,
            title="New Conversation"
        )
        return JsonResponse({
            'success': True,
            'chat_id': chat.id,
            'redirect_url': f'/chat/{chat.id}/'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required(login_url='login')
@require_http_methods(["POST"])
def send_message(request, chat_id):
    """Send a message in a chat"""
    try:
        chat = get_object_or_404(Chat, id=chat_id, user=request.user)
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({'success': False, 'error': 'Message cannot be empty'}, status=400)
        
        # Create user message
        user_message = Message.objects.create(
            chat=chat,
            sender='user',
            content=content
        )
        
        # Update chat title from first message
        if chat.messages.count() == 1:
            chat.title = content[:50] + "..." if len(content) > 50 else content
            chat.save()
        
        # Build conversation history for context
        chat_history = []
        previous_messages = chat.messages.exclude(id=user_message.id).order_by('created_at')
        for msg in previous_messages:
            role = 'user' if msg.sender == 'user' else 'model'
            chat_history.append({'role': role, 'parts': [msg.content]})
        
        # Add current user message
        chat_history.append({'role': 'user', 'parts': [content]})
        
        # Generate AI response using Groq (FREE Llama model)
        try:
            # Build conversation history for Groq
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            
            previous_messages = chat.messages.exclude(id=user_message.id).order_by('created_at')[:10]
            for msg in previous_messages:
                role = "user" if msg.sender == 'user' else "assistant"
                messages.append({"role": role, "content": msg.content})
            
            # Add current user message
            messages.append({"role": "user", "content": content})
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            bot_response_content = response.choices[0].message.content.strip()
            print(f"Groq API SUCCESS: {bot_response_content[:100]}...")
            
        except Exception as ai_error:
            import traceback
            print(f"Groq API ERROR: {type(ai_error).__name__}: {ai_error}")
            traceback.print_exc()
            bot_response_content = "I'm sorry, I'm experiencing some issues right now. Please try again in a moment. I'm here for you."
        
        bot_message = Message.objects.create(
            chat=chat,
            sender='bot',
            content=bot_response_content
        )
        
        return JsonResponse({
            'success': True,
            'user_message': {
                'id': user_message.id,
                'content': user_message.content,
                'sender': user_message.sender,
                'created_at': user_message.created_at.isoformat()
            },
            'bot_message': {
                'id': bot_message.id,
                'content': bot_message.content,
                'sender': bot_message.sender,
                'created_at': bot_message.created_at.isoformat()
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required(login_url='login')
@require_http_methods(["DELETE"])
def delete_chat(request, chat_id):
    """Delete a chat"""
    try:
        chat = get_object_or_404(Chat, id=chat_id, user=request.user)
        chat.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required(login_url='login')
@require_http_methods(["POST"])
def rename_chat(request, chat_id):
    """Rename a chat"""
    try:
        chat = get_object_or_404(Chat, id=chat_id, user=request.user)
        data = json.loads(request.body)
        new_title = data.get('title', '').strip()
        
        if not new_title:
            return JsonResponse({'success': False, 'error': 'Title cannot be empty'}, status=400)
        
        chat.title = new_title
        chat.save()
        
        return JsonResponse({'success': True, 'title': chat.title})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect('landing')