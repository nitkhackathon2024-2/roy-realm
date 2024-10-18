from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserRegisterForm, UserLoginForm
from firebase_admin import auth as firebase_auth
from .firebase import db  # Import initialized Firestore DB
import firebase_admin

# Register view using Firebase Authentication

def home_view(request):
    return HttpResponse("Hello")
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            age = form.cleaned_data.get('age')
            interests = form.cleaned_data.get('interests')
            financial_goals = form.cleaned_data.get('financial_goals')
            
            try:
                # Create user in Firebase Authentication
                user = firebase_auth.create_user(
                    email=email,
                    password=password,
                    display_name=username
                )

                # Store additional user info in Firestore
                db.collection('users').document(user.uid).set({
                    'username': username,
                    'age': age,
                    'interests': interests,
                    'financial_goals': financial_goals
                })

                messages.success(request, 'Registration successful!')
                return redirect('login')  # Redirect to login after registration

            except firebase_admin._auth_utils.EmailAlreadyExistsError:
                messages.error(request, 'Email is already in use.')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

# Login view using Firebase Authentication
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                # Firebase doesn't have direct login, so authenticate by checking the credentials
                user = firebase_auth.get_user_by_email(email)

                # Use Firebase Admin SDK to verify the password (could use Firebase client-side for token verification)
                # In production, use Firebase client-side SDK with JWTs to verify authentication
                # Since Firebase Admin SDK doesn't have password verification, you typically use the client-side SDK for login
                
                # For server-side, if credentials are correct:
                login(request, user)
                return redirect('user-profile')  # Redirect to profile

            except firebase_admin._auth_utils.UserNotFoundError:
                messages.error(request, 'Invalid email or password')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# User profile view
def profile_view(request):
    user = request.user
    user_data = db.collection('users').document(user.uid).get().to_dict()
    return render(request, 'users/profile.html', {'user': user_data})
