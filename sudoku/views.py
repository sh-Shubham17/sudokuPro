from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    """ this method is used to render home page
    parameter : 
        request object
    Returns : 
    render method with home.html file location 
    
    Note: files must be in templates because django looks for files in templates folder
    """
    return render(request, 'home.html' )

def registerPage(request):
    """> This method will render register.html page
        > This will also checks and saves the data entered by user to register on the web app
    parameter : 
        request object
    returns : 
    reder() method  """
    if request.user.is_authenticated:
        return redirect('home') #to redirect user back to home page who are already logged in and trying to access register page

    else :
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'account was created for ' + user)

                print('details saved')
                return redirect('login')

        response = {'form': form}
        #print( ' in register page in view')
        return render(request, 'accounts/register.html', response)


def loginPage(request):     #name is loginPage not login because we already have login function imported from django.conttrib.auth
    """
    checks and authenticates user whether user is valid & register user or not

    parameters :
        request object
    returns :
        render() method
    """
    if request.user.is_authenticated:
        return redirect('home')

    else :
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)
            print('user',user)
            if user is not None :
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'username or password is incorrect')

        response = {}
        return render(request, 'accounts/login.html', response ) 

def logoutUser(request):
    """ to logout current user from web app
    parameter : 
        request object
    returns:
        redirect method to direct user to login page to log back in 
        """
    logout(request)
    return redirect('login')
