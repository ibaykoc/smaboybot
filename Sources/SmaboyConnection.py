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
        if re.search('/timeline', username) or re.search('/twitter', username):
            # Cannot get account detail from this account type yet
            return None
        print('Getting account from username: %s' % username)
        response = cls.session.get('http://www.smaboy.com/u/%s' % username)
        time.sleep(cls.perconnection_delay)
        # realname = ''
        # province = ''
        # city = ''
        # gender = ''
        # age = ''
        # job = ''
        # job_place = ''
        # status = ''

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

        return {'account_type' : 'normal',
                'realname' : realname,
                'username' : username,
                'location' : '%s, %s' % (city, province),
                'gender' : gender,
                'age' : age,
                'job' : job,
                'job_place' : job_place,
                'status' : status
               }
            