from tkinter import Tk, Canvas
from websocket import WebSocket
import threading,time,requests,ast
def move_window(event):
        window.geometry(f'+{event.x_root}+{event.y_root}')


window = Tk()
window.geometry("298x95")
window.configure(bg = "#8ABAD5")
window.overrideredirect(True)
window.bind("<B1-Motion>", move_window)
window.attributes("-topmost", True)


#variables
word = "Waiting..."
room_code = "ROOM_CODe"
"Status options 🔴/"
said_word_status = '🔮'
connection_status = "🔴"
auth_token = 'AUTH_TOKEN'
player_amount = 0
words_bank = open('wordlist.txt', 'r').read().split('\n')

#end of variables

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
    try:
        r = requests.post('https://jklm.fun/api/joinRoom',headers=headers,json=data)
        rjson = r.json()
        server_link = str(rjson['url'])
        server_link = server_link.split('.')[0]
        server_link = server_link.split('https://')
        return server_link[1]
    except:
        print("Invalid room!")
        exit()
def heartbeat(websock):
    print("heartbeat started")
    while True:
        recv = websock.recv()
        print(recv)
        time.sleep(25000/1000)
        websock.send('3')
def find_word(sylabol):
    for word in words_bank:
        if sylabol in word:
            words_bank.remove(word)
            return word
        else:
            pass
    return "Not Found 😭"
def connect(ws_link, auth_token):
    try:
        print(ws_link)
        global connection_status,word,said_word_status,player_amount
        connection_status = '🚀'
        control_socket = WebSocket()
        data_socket = WebSocket()
        data_socket.connect(ws_link,
                http_proxy_host="192.241.125.217",
                http_proxy_port="8261",
                http_proxy_auth=('gatoproxies','gatolover999'),
                proxy_type="http")
        recieved = data_socket.recv()
        
        data_socket.send('40')
        sesh_response = data_socket.recv()

        data_socket.send('420["joinRoom",{"roomCode":"%s","userToken":"%s","nickname":"🤖","language":"en-US"}]' % (room_code, auth_token))
        find_join = data_socket.recv()


        control_socket.connect(ws_link,
                http_proxy_host="192.186.176.45",
                http_proxy_port="8095",
                http_proxy_auth=('gatoproxies','gatolover999'),
                proxy_type="http")
        recieved = control_socket.recv()

        control_socket.send('40')
        sesh_response = control_socket.recv()

        control_socket.send('42["joinGame","bombparty","%s","%s"]' % (room_code,auth_token))
        thing_response = control_socket.recv()
        print(thing_response)
        threading.Thread(target=heartbeat, args=(control_socket,)).start()
        threading.Thread(target=heartbeat, args=(data_socket,)).start()
        connection_status="✅"
        while True:
            data = control_socket.recv()
            if 'nextTurn' in data:
                data = data.strip('42')
                next_person_list = ast.literal_eval(data)
                sylabol = next_person_list[2]
                input_word = find_word(sylabol)
                word = input_word
                print(f"{word} | {sylabol}")
            elif 'failWord' in data:
                said_word_status = '❌'
            elif 'correctWord' in data:
                said_word_status = '✅'
            else:
                print(data)

    except:
        print("I deadass dont know whats wrong lmao")

def update_word():
    global word,connection_status,player_amount
    canvas.itemconfig(word_enter, text=word)
    canvas.itemconfig(connection_status_text, text=f"Room Code: {room_code}     Game Connection Status : {connection_status}")
    canvas.itemconfig(player_amount,text=f"V1.0.5 Lobby {player_amount}/16")
    canvas.itemconfig(word_status, text=f"{said_word_status}")

    window.after(100, update_word)  
window.after(500,update_word)
balancer = get_room_link(room_code)
ws_link = f'wss://{balancer}.jklm.fun/socket.io/?EIO=4&transport=websocket'
threading.Thread(target=connect,args=(ws_link,auth_token),).start()

canvas = Canvas(
    window,
    bg = "#8ABAD5",
    height = 95,
    width = 298,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
text_rectangle = canvas.create_rectangle(
    6.0,
    31.0,
    289.0,
    89.0,
    fill="#74AECE",
    outline="#4380a1")


word_enter = canvas.create_text(
    150.0,
    60.0,
    text=word,
    fill="#d0f4de",
    font=("Helvetica", 30)
    ,anchor="center",
    justify="center",
    width=280.0
)
#make it so o can highlight word_enter

canvas.create_text(
    9.0,
    0.0,
    anchor="nw",
    text="JKLM.FUN Bombparty Assist",
    fill="#000000",
    font=("Inter", 12 * -1)
)

canvas.create_rectangle(
    255.0,
    3.0,
    281.0,
    29.0,
    fill="#77B7DA",
    outline="")

word_status = canvas.create_text(
    260.0,
    7.0,
    anchor="nw",
    text=said_word_status,
    fill="#000000",
    font=("Inter", 15 * -1)
)

connection_status_text = canvas.create_text(
    11.0,
    17.0,
    anchor="nw",
    text=f"Room Code: {room_code}     Game Connection Status : {connection_status}",
    fill="#000000",
    font=("Inter", 8 * -1)
)

playercount = canvas.create_text(
    174.0,
    4.0,
    anchor="nw",
    text=f"V1.0.5 Lobby {player_amount}/16",
    fill="#000000",
    font=("Inter", 8 * -1)
)
window.resizable(False, False)
window.mainloop()
