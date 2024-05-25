from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import BookingForm, CommentForm
from .models import Menu, UserComments


# Create your views here.


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'book.html', context)


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', main_data)


def display_menu_items(request, pk=None):
    if pk:
        try:
            menu_item = Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            raise Http404("Menu item does not exist")
    else:
        menu_item = ''
    return render(request, 'menu_item.html', {'menu_item': menu_item})

# Comments View


def form_view(request):
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            uc = UserComments(
                first_name=cd['first_name'],
                last_name=cd['last_name'],
                comment=cd['comment'],
            )
            uc.save()
            return JsonResponse({'message': 'success'})
    return render(request, 'blog.html', {'form': form})
