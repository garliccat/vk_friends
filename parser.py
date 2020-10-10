import requests
import csv
from options import token


def write_csv(data):
    with open('vk_friends.csv', 'a', newline='', encoding='utf-8') as f:
        #newline - to avoid blank rows after each record
        #encoding utf-16 - we are in russia, thats all
        writer = csv.writer(f, delimiter=';')
        writer.writerow(data)

def uid_name(uid):
    '''
    returns first name of user with provided VK uid
    '''
    ret = requests.get(r'https://api.vk.com/method/users.get?user_id={}&access_token={}&v=5.124'.format(uid, token)).json()
    return str(ret['response'][0]['first_name'])

def uid_frnds(uid):
    '''
    returns a list of names of friends of provided VK uid
    '''
    ret = requests.get(r'https://api.vk.com/method/friends.get?user_id={}&access_token={}&v=5.124'.format(uid, token)).json()
    if ret['response']['count'] > 0:
        return [uid_name(i) for i in ret['response']['items']]

def uid_frndscnt(uid):
    '''
    returns friends count from UID
    '''
    ret = requests.get(r'https://api.vk.com/method/friends.get?user_id={}&access_token={}&v=5.124'.format(uid, token)).json()
    return ret['response']['count']


with open('vk_friends.csv', 'r', encoding='utf-8') as f:
	l = 1
	for i in f:
		l += 1
		pass
	last_uid = int(i.split(';')[0])
	print('UID in last line: %d' % last_uid)
	print('Number of lines: %d' % l)

# last_uid = 441000000

stop = last_uid + 100000

for uid in range(last_uid + 1, stop):
    try:
        name = uid_name(uid)
        frnds_cnt = uid_frndscnt(uid)

        if frnds_cnt > 100 or frnds_cnt == 0:
            continue

        frnds_lst = uid_frnds(uid)
        
        l += 1
        print('Line number: ', l)
        print('UID: ', uid, ' of ', stop, ' ({:.1f} %)'.format((uid - last_uid) / (stop - last_uid) * 100))
        print('Name: ', name)
        print('Friends count: ', frnds_cnt)
        print('Friends: ', frnds_lst)
        print()

        write_csv([uid, 
            name, 
            frnds_cnt, 
            '|'.join(frnds_lst)])

    except:
       pass