from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import RegistrationForm
from .models import Account
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from carts.views import _cart_id
from carts.models import Cart, CartItem

import requests


# Create your views here.
def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            mail = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            
            username = mail.split('@')[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                mail=mail,
                phone = phone,
                password=password
            )
            user.phone = phone
            user.save()
           
            current_site = get_current_site(request)
            mail_subject = 'Por favor activa tu cuenta'
            body =  render_to_string('accounts/account_verification_email.html', {
               'user': user,
               'domain': current_site,
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': default_token_generator.make_token(user),
            })
           
            to_mail = mail
            send_email = EmailMessage(mail_subject, body, to=[to_mail])
            send_email.send()
           
           
           
           
           
           
           
           
           
            messages.success(request, '¡Registro exitoso!')
            return redirect('register')
        
        
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        mail = request.POST['mail']
        password = request.POST['password']
        
        user = auth.authenticate(mail=mail, password=password)
        
        if user is not None:
            try: 
                cart =  Cart.objects.filter(cart_id=_cart_id(request)).first()
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)
                    
                    product_variation = []

                    for item in cart_items:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user = user
                                item.save()
            except:
                pass
            
            
            
            
            auth.login(request, user)
            messages.success(request, '¡Has iniciado sesión!')
            
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))

                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
           
            
        else:
            messages.error(request, 'Credenciales inválidas')
            return redirect('login')
    
    
    return render(request, 'accounts/login.html')








@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, '¡Has cerrado sesión correctamente!')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, '¡Gracias por activar tu cuenta! Ahora puedes iniciar sesión.')
        return redirect('login')
    else:
        messages.error(request, 'El enlace de activación es inválido o ha expirado.')
        return redirect('register')
    
@login_required(login_url='login')
def dashboard(request):
    
    return render(request, 'accounts/dashboard.html')

def forgotpassword(request):
    if request.method == 'POST':
        mail = request.POST['mail']
        
        if Account.objects.filter(mail=mail).exists():
            user = Account.objects.get(mail__exact=mail)
            
            current_site = get_current_site(request)
            mail_subject = 'Restablecer tu contraseña'
            body =  render_to_string('accounts/reset_password_email.html', {
               'user': user,
               'domain': current_site,
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': default_token_generator.make_token(user),
            })
           
            to_mail = mail
            send_email = EmailMessage(mail_subject, body, to=[to_mail])
            send_email.send()
            
            messages.success(request, 'Se ha enviado un correo electrónico para restablecer su contraseña.')
            return redirect('login')
        else:
            messages.error(request, 'La cuenta de correo no existe.')
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotpassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Por favor restablece tu contraseña')
        return redirect('resetpassword')
    else:
        messages.error(request, 'El enlace de restablecimiento de contraseña es inválido o ha expirado.')
        return redirect('login')
    
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Contraseña restablecida con éxito.')
            return redirect('login')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('resetpassword')
    return render(request, 'accounts/resetpassword.html')

