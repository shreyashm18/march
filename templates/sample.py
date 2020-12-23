def passToken(request, time_period = 15):
    print(f'request = {request.user}')
    token = Token.objects.get(user=request.user)
    print(f'token = {token.key}')
    print(f'token type = {type(token.key)}')
    # token = token.key
    if token.key:
        endpoint = 'http://127.0.0.1:8000/covid/report/'
        tkn = 'Token '+token.key
        print(f'tookeenn = {tkn}')
        dict = requests.get(url=endpoint, headers = {'Authorization': tkn})
        dict = dict.json()
        print(f'dict = {dict} dict type = {type(dict)}')
    return render(request,'covid.html',dict)



    return Response(dict)