import re
import time
import requests

class SmaCon:
    perconnection_delay = 5
    session = requests.Session()

    @classmethod
    def __init__(cls, perconnection_delay=5):
        cls.perconnection_delay = perconnection_delay

    @classmethod
    def login(cls, username, password):
        print('Logging in')
        response = cls.session.post('http://www.smaboy.com/member/loginpost',
                                    {
                                        'username' : username,
                                        'password' : password
                                    })
        time.sleep(cls.perconnection_delay)
        return re.search(username, response.text, re.IGNORECASE)

    @classmethod
    def get_username_from_browse(cls, index=1):
        print('Getting usernames from browse page: %d' % index)
        response = cls.session.post('http://www.smaboy.com/browse/index', {
            'age_from' : '',
            'age_to': '',
            'location': '',
            'gender': '',
            'var1': '',
            'var2': '',
            'var3': '',
            'var4': '',
            'var5': '',
            'var6': '',
            'var7': '',
            'page': index
        })
        time.sleep(cls.perconnection_delay)
        if re.search('Sorry, no results', response.text):
            # No result
            return None

        return re.findall('top:-20px;margin-left:-20px;"><a href="http://www.smaboy.com/u/(.*?)">',
                          response.text)

    @classmethod
    def get_account(cls, username):
        if re.search('/timeline', username):
            return cls.get_timeline_account(username)
        if re.search('/twitter', username):
            return cls.get_twitter_account(username)

        return cls.get_normal_account(username)

    @classmethod
    def get_normal_account(cls, username):
        print('Getting normal account from username: %s' % username)
        response = cls.session.get('http://www.smaboy.com/u/%s' % username)
        time.sleep(cls.perconnection_delay)

        #userid
        find = re.search(r'/add/(\d+)', response.text, re.DOTALL)
        userid = find.group(1) if find else ''

        #realname
        find = re.search('<span style="font-size:24px;font-weight:bold;padding-bottom:5px;">'
                         '(.*?)</span>',
                         response.text, re.DOTALL)
        realname = find.group(1) if find else ''

        #province
        find = re.search('From <span class="cblue"><a>(.*?)</a>', response.text, re.DOTALL)
        province = find.group(1) if find else ''

        #city
        find = re.search('City <a>(.*?)</a>', response.text, re.DOTALL)
        city = find.group(1) if find else ''

        #gender
        find = re.search('Gender <span class="cblue"><a>(.*?)</a>', response.text, re.DOTALL)
        gender = find.group(1) if find else ''

        #age
        find = re.search('Age <span class="cblue"><a>(.*?)</a>', response.text, re.DOTALL)
        age = find.group(1) if find else ''
        age = 'hidden' if age == '<i>Tersembunyi</i>' else age
        #job
        find = re.search('<span><i class="mrs imgt info_job sp_bg2">'
                         '</i><span class="cblue">.*?<a>(.*?)</a>',
                         response.text, re.DOTALL)
        job = find.group(1) if find else ''

        #job_place
        find = re.search('di <a>(.*?)</a>', response.text, re.DOTALL)
        job_place = find.group(1) if find else ''

        #status
        find = re.search('Status <span class="cblue"><a>(.*?)</a>', response.text, re.DOTALL)
        status = find.group(1) if find else ''

        #follow and friend status
        find = re.findall('<span class="uiButtonText">(.*?)</span>', response.text, re.DOTALL)
        total_button = len(find)
        follow_status = ''
        friend_status = ''
        if total_button == 3:
            #Followed
            follow_status = 'followed'
            if 'Tambahkan sebagai teman' in find[0]:
                friend_status = 'Unfriend'
            elif 'Waiting Confirmation' in find[0]:
                friend_status = 'waiting confirmation'
            else:
                print('Unknown friend status value: %s' % find[0])
        elif total_button == 4:
            follow_status = 'unfollowed'
            if 'Tambahkan sebagai teman' in find[1]:
                friend_status = 'Unfriend'
            elif 'Waiting Confirmation' in find[1]:
                friend_status = 'waiting confirmation'
            else:
                print('Unknown normal friend status value: %s' % find[1])

        else: print('Website has change the button layout, update code')

        return {'account_type' : 'normal',
                'username' : username,
                'userid' : userid,
                'realname' : realname,
                'location' : '%s, %s' % (city, province),
                'gender' : gender,
                'age' : age,
                'job' : job,
                'job_place' : job_place,
                'status' : status,
                'friend_status' : friend_status,
                'follow_status' : follow_status
               }

    @classmethod
    def get_twitter_account(cls, username):
        print('Getting twitter account from username: %s' % username)
        response = cls.session.get('http://www.smaboy.com/u/%s' % username)
        time.sleep(cls.perconnection_delay)

        #userid
        find = re.search(r'/add/(\d+)', response.text, re.DOTALL)
        userid = find.group(1) if find else ''

        #realname
        find = re.search('<div style="font-size:24px;font-weight:bold;padding-bottom:5px;">'
                         '(.*?)</div>', response.text, re.DOTALL)
        realname = find.group(1) if find else ''

        #twitter_name
        find = re.search('<div style="font-size:18px;font-weight: normal;'
                         'line-height: 24px;color: #777;">(.*?)</div>',
                         response.text, re.DOTALL)
        twitter_name = find.group(1) if find else ''

        #location
        find = re.search('<div style="font-size:12px;font-weight: normal;'
                         'line-height: 24px;color: #777;">(.*?)</div>',
                         response.text, re.DOTALL)

        location = find.group(1) if find else ''

        #follow and friend status
        find = re.findall('<span class="uiButtonText">(.*?)</span>', response.text, re.DOTALL)
        total_button = len(find)
        follow_status = ''
        friend_status = ''
        if total_button == 1:
            #Followed
            follow_status = 'followed'
            if 'Tambah Teman' in find[0]:
                friend_status = 'Unfriend'
            elif 'Waiting' in find[0]:
                friend_status = 'waiting confirmation'
            else:
                print('Unknown friend status value: %s' % find[0])
        elif total_button == 2:
            follow_status = 'unfollowed'
            if 'Tambah Teman' in find[1]:
                friend_status = 'Unfriend'
            elif 'Waiting' in find[1]:
                friend_status = 'waiting confirmation'
            else:
                print('Unknown twitter friend status value: %s' % find[1])

        else: print('Website has change the button layout, update code')

        return {'account_type' : 'twitter',
                'username' : username,
                'userid' : userid,
                'realname' : realname,
                'twitter_name' : twitter_name,
                'location' : location,
                'friend_status' : friend_status,
                'follow_status' : follow_status
               }

    @classmethod
    def get_timeline_account(cls, username):
        print('Getting timeline account from username: %s' % username)
        response = cls.session.get('http://www.smaboy.com/u/%s' % username)
        time.sleep(cls.perconnection_delay)

        #userid
        find = re.search(r'/add/(\d+)', response.text, re.DOTALL)
        userid = find.group(1) if find else ''

        #realname
        find = re.search('<span style="font-size:24px;font-weight:bold;'
                         'padding-bottom:5px;">(.*?)</span>', response.text, re.DOTALL)
        realname = find.group(1) if find else ''

        #province
        find = re.search('</i>Tinggal di <span class="cblue"><a>(.*?)</a>',
                         response.text, re.DOTALL)
        province = find.group(1) if find else ''

        #city
        find = re.search('kota <a>(.*?)</a>',
                         response.text, re.DOTALL)

        city = find.group(1) if find else ''

        #follow and friend status
        find = re.findall('<span class="uiButtonText">(.*?)</span>', response.text, re.DOTALL)
        total_button = len(find)
        friend_status = ''
        if total_button == 2:
            if 'Tambahkan sebagai teman' in find[0]:
                friend_status = 'Unfriend'
            elif 'Waiting Confirmation' in find[0]:
                friend_status = 'waiting confirmation'
            else:
                print('Unknown friend status value: %s' % find[0])

        else: print('Website has change the button layout, update code')

        return {'account_type' : 'twitter',
                'username' : username,
                'userid' : userid,
                'realname' : realname,
                'location' : '%s, %s' % (city, province),
                'friend_status' : friend_status
               }

    @classmethod
    def add_friend(cls, account, message=''):
        print(account['userid'])
        userid = account['userid']
        print('adding %s as friend' % account['realname'])
        response = cls.session.post('http://www.smaboy.com/friends/addpost',
                                    files={'msg': (None, message), 'uid': (None, userid)})
        time.sleep(cls.perconnection_delay)
        if re.search(userid, response.text, re.IGNORECASE):
            print('%s added as friend' % account['realname'])
        else:
            print('%s failed to add as friend' % account['realname'])
