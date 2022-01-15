import os, requests, time, random, stdiomask
from random import randint
from uuid import uuid4
from user_agent import generate_user_agent


posts = []
uid = str(uuid4())
banner = """
                                                                      
 _____ _____ _____ _____    ____  _____ __    _____ _____ _____ _____ 
|  _  |     |   __|_   _|  |    \|   __|  |  |   __|_   _|   __| __  |
|   __|  |  |__   | | |    |  |  |   __|  |__|   __| | | |   __|    -|
|__|  |_____|_____| |_|    |____/|_____|_____|_____| |_| |_____|__|__|
                        
                    ~~Free Tool by joshua~~                                                           
                                                                             
"""




def GetSelfID():
    global selfID, graph
    try:
        graph = r.get(f'https://instagram.com/{username}/?__a=1').json()
        selfID = str(graph['logging_page_id'].split('_')[1])
        return True
    except:
        return False

def Collect(number):
    done = 0
    added = 0
    if  graph['graphql']['user']["edge_owner_to_timeline_media"]['count'] == 0:
        print('[ERROR] No posts found.')
        time.sleep(5)
        return
    get_posts = r.get(f'https://instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables=%7B%22id%22%3A%22{selfID}%22%2C%22first%22%3A500%7D').json()
    while True:
        try:
            x = str(get_posts['data']['user']["edge_owner_to_timeline_media"]['edges'][done]['node']['id'])
            if x not in posts:
                posts.append(x)
                added+=1
                if len(posts) == number:
                    break
            done+=1
        except:
            if get_posts['data']['user']["edge_owner_to_timeline_media"]['page_info']['has_next_page']:
                end_cursor = get_posts['data']['user']["edge_owner_to_timeline_media"]['page_info']['end_cursor']
                os.system('cls' if os.name == 'nt' else 'clear')
                print(banner)
                print(f'[SEARCHING] Collected {added}/{number} posts')
                time.sleep(8)
                get_posts = r.get(f'https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables=%7B%22id%22%3A%22{selfID}%22%2C%22first%22%3A500%2C%22after%22%3A%22{end_cursor}%3D%3D%22%7D').json()
                done= 0
                
            else:
                break
    if added > 0:
        print(f'\n[SUCCESS] {added}x posts collected!')
        time.sleep(4)
        return True
    else:
        print(f'\n[ERROR] Failed to collect posts!')
        time.sleep(4)
        return False



def delete():
    deleted = 0
    error = 0
    number = len(posts)
    while len(posts) > 0:
        item = random.choice(posts)
        like_url = f'https://www.instagram.com/create/{item}/delete/'
        head = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f'sessionid={id};',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com',
        'user-agent': generate_user_agent(),
        'x-csrftoken': '8tzzZmtfRqaQjKk9GmdnqPmRrvTGBRY9',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': 'hmac.AR1oDoUbdtXZGVrS6LpI7YEC6n8qFXeg3o6S7sOmOyJ0hb6m',
        'x-instagram-ajax': '181fef01fd26',
        'x-requested-with': 'XMLHttpRequest'
        }
        
        
        delete_it = r.post(like_url,headers=head)
        if 'ok' in delete_it.text:
            deleted+=1
            os.system('cls' if os.name == 'nt' else 'clear')
            print(banner)
            print(f'[-] Done: {deleted}\n[-] Error: {error}\n[-] Account: {username}')
            if deleted == number:
                posts.remove(item)
                print(f'\n[!] {number}x posts have been successfully deleted!')
                time.sleep(9)
                return
            else:
                time.sleep(speed)
                posts.remove(item)
        else:
            error+=1
            print('[!] Error in delete! Sleeping 5 minutes.')
            time.sleep(301)
    else:
        print('[ERROR] No posts found to delete. Collect them first!')
        time.sleep(6)
        return





def login():
    global username, r, id
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        url = 'https://b.i.instagram.com/api/v1/accounts/login/'
        headers = {'User-Agent': 'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)'}
        username = input('[+] Username: ')
        password = stdiomask.getpass('[+] Password: ')
        data = {'uuid':uid,  'password':password, 'username':username, 'device_id':uid, 'from_reg':'false', '_csrftoken':'missing', 'login_attempt_countn':'0'}
        r = requests.session()
        req = r.post(url, headers=headers, data=data)
        try:
            id = req.cookies['sessionid']
            print('\n[SUCCESS] Logged in!')
            time.sleep(3)
            break
        except:
            if "The password you entered is incorrect."in req.text:
                print('\n[ERROR] Password Incorrect')
                time.sleep(5)
            elif "The username you entered doesn't appear to belong to an account." in req.text:
                print('\n[ERROR] User does not exist')
                time.sleep(5)
                
            elif "Invalid Parameters" in req.text:
                print('\n[ERROR] Invalid Inputs')
                time.sleep(5)
            else:
                print(f'[ERROR] Check Your Account For a Checkpoint')
                time.sleep(5)
    panel()



def panel():
    global speed
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        choice = input(f"""[1] Collect Posts
[2] Delete Collected Posts
[-] Current number of collected posts: {len(posts)}\n\n[+] Choose One: """)
        
        if choice == '1':
            number = int(input('[-] Number of posts to collect: '))
            print('\n[COLLECTING] Collecting {} posts to delete...'.format(number))
            if GetSelfID():
                Collect(number)
            else:
                print('[ERROR] Unable to gather posts.')
        elif choice == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(banner)
            speed = input("""[-] Determine your delete speed:\n\n[1] Fast 2-4 sec delay
[2] Medium 10-15 sec delay
[3] Slow 30-60 sec delay\n\n[+] Choose One: """)
            if speed == '1':
                speed = randint(1,4)
                delete()
            elif speed == '2':
                speed = randint(10,15)
                delete()
            elif speed == '3':
                speed = randint(30,60)
                delete()
            else:
                pass
        

if __name__ == "__main__":
    login()