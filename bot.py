import threading,time,requests,random,ast
from websocket import WebSocket
def get_room_link(room):
    headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://jklm.fun",
    "referer": f"https://jklm.fun/{room}",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
    data = {"roomCode": room}
    r = requests.post('https://jklm.fun/api/joinRoom',headers=headers,json=data)
    rjson = r.json()
    server_link = str(rjson['url'])
    server_link = server_link.split('.')[0]
    server_link = server_link.split('https://')
    return server_link[1]
def heartbeat(websock):
    print("heartbeat started")
    while True:
        time.sleep(25000/1000)
        websock.send('3')
def join_game(websock):
    websock.send('42["joinRound"]')
def send_word(websock,input_word):
    websock.send('42["setWord","%s",true]' % input_word)
def send_chat(websock,chat_mesage):
    websock.send('42["chat","%s"]' % chat_mesage)
def find_word(sylbol):
    for word in words_bank:
        if sylbol in word:
            words_bank.remove(word)
            return word
        else:
            pass
    return "not found"


words_bank = open('wordlist.txt', 'r').read().split('\n')
accs = open('acs.txt', 'r').read().splitlines()
proxies = open('proxies.txt', 'r').read().splitlines()
rm_code = "ROOMCODE"
balancer = get_room_link(rm_code)
ws_link = f'wss://{balancer}.jklm.fun/socket.io/?EIO=4&transport=websocket'
account_number = 0


def connect(user_auth,proxy,account_nu,room_code):
    print(f'using {proxy}')
    proxy_ip = proxy.split(':')[0]
    proxy_port = proxy.split(':')[1]
    control_socket = WebSocket()
    data_socket = WebSocket()
    data_socket.connect(ws_link,http_proxy_host=proxy_ip,http_proxy_port=proxy_port,proxy_type="http")
    recieved = data_socket.recv()

    data_socket.send('40')
    sesh_response = data_socket.recv()

    data_socket.send('420["joinRoom",{"roomCode":"%s","userToken":"%s","nickname":"🍆🥵","language":"en-US"}]' % (room_code, user_auth))
    find_join = data_socket.recv()


    control_socket = WebSocket()
    control_socket.connect(ws_link,http_proxy_host=proxy_ip,http_proxy_port=proxy_port,proxy_type="http")
    recieved = control_socket.recv()

    control_socket.send('40')
    sesh_response = control_socket.recv()

    control_socket.send('42["joinGame","bombparty","%s","%s"]' % (room_code,user_auth))
    find_response = control_socket.recv()
    find_response = find_response.strip('42')
    send_chat(data_socket,f"🌭Bot {account_nu} Ready For Action!🌭")
    #try to turn find_response into lst
    game_user_id = int(find_response.split('selfPeerId')[-1].split(',')[0].strip('":'))
    join_game(control_socket)
    threading.Thread(target=heartbeat, args=(control_socket,)).start()
    threading.Thread(target=heartbeat, args=(data_socket,)).start()

    """
    ["setMilestone",{"name":"round","startTime":1669261930102,"currentPlayerPeerId":0,"dictionaryManifest":{"name":"English","bonusAlphabet":"abcdefghijklmnopqrstuvwy","promptDifficulties":{"beginner":500,"medium":300,"hard":100}},"syllable":"bar","promptAge":0,"usedWordCount":0,"playerStatesByPeerId":{"0":{"lives":2,"word":"","wasWordValidated":false,"bonusLetters":[]},"8":{"lives":2,"word":"","wasWordValidated":false,"bonusLetters":[]}}},1669261930120]"""
    #auto fill thingy majigure
    while True:
        data = control_socket.recv()
        if 'nextTurn' in data:
            data = data.strip('42')
            next_person_list = ast.literal_eval(data)
            if next_person_list[1] == game_user_id:
                sylabol = next_person_list[2]
                input_word = find_word(sylabol)
                send_word(control_socket,input_word)
                if 'fail' in data:
                    print(data)
                    exit()
                else:
                    print(data)
            else:
                sylabol = next_person_list[2]
                input_word = find_word(sylabol)
                print(input_word)
        elif 'currentPlayerPeerId' in data:
            data = data.strip('42')
            starting_player = int(data.split('"currentPlayerPeerId":')[1].split(',')[0])
            if starting_player == game_user_id:
                sylabol = data.split('"syllable":"')[1].split('"')[0]
                input_word = find_word(sylabol)
                send_word(control_socket,input_word)
            else:
                sylabol = data.split('"syllable":"')[1].split('"')[0]
                word = find_word(sylabol)
                print("you were not first")
        else:
            pass
for acc in accs:
    account_number = account_number + 1
    proxy = random.choice(proxies)
    proxies.remove(proxy)
    threading.Thread(target=connect, args=(acc,proxy,account_number,rm_code)).start()