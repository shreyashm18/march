from rest_framework.authtoken.models import Token
from account.forms import InputDataForm

def token(request):
    if request.user.is_authenticated:
        token = Token.objects.get(user=request.user)
        print(f'token === {token.key}')
        return {"token": token.key}
    else:
        return {"token": None}

def formData(request):
    form = InputDataForm()
    return {'form':form}