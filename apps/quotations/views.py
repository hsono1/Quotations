from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote


def index(request):
    return render(request, 'quotations/index.html')

def register(request):
    user = User.objects.val_Reg(request.POST)
    if 'errors' in user:
        errors = user['errors']
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    if 'register' in user:
        request.session['user_id'] = user['register'].id
        return redirect('/success')

def login(request):
    user = User.objects.val_Login(request.POST)
    if 'register' in user:
        request.session['user_id'] = user['register'].id
        return redirect("/success")
    else:
        if 'errors' in user:
            errors=user['errors']
            for error in errors:
                messages.error(request, error)
            return redirect('/')

def content(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login first")
        return redirect('/')
    else:
        user = request.session['user_id']
        user_obj = User.objects.get(id= user)
        u_favorites = user_obj.quote_set.all()
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'quotes': Quote.objects.all(), 'favorites' : u_favorites
        }
        return render(request, 'quotations/content.html', context)


def addQuote(request):
    author1 = request.POST['author']
    message1 = request.POST['message']
    creator1 = User.objects.get(id = request.POST['creator'])
    quote = Quote.objects.create(author= author1, message= message1, creator= creator1)
    return redirect("/success")


def userQuotes(request, id):
    user = User.objects.get(id = id)
    quote = user.u_creator.all()
    count = user.u_creator.count()
    context = {  'user': user  , 'count': count, 'quotes': quote   }
    return render(request, "quotations/user.html", context)


def userFavorite(request):
    message_id = request.POST['message_obj']
    message_obj = Quote.objects.get(id=message_id)
    user = request.POST['user']
    user1 = User.objects.get(id= user) 
    message_obj.favorites.add(user1)
    message_obj.creator = None
    return redirect("/success")



def remove(request):
    message_id = request.POST['message_obj']
    message_obj = Quote.objects.get(id=message_id)
    user = request.POST['user']
    user1 = User.objects.get(id= user) 
    message_obj.creator =  user1
    user1.quote_set.remove(message_obj)
    return redirect("/success")

def logout(request):
    del request.session['user_id']
    return redirect("/")

