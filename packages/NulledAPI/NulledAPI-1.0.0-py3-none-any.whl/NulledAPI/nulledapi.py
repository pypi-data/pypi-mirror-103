import requests
from hashlib import md5

class Nulled:
    '''
    Un-Official Nulled.to API developed by M3GZ \n
    Visit my profile page -> https://www.nulled.to/user/4103370-m3gz
    '''
    group_list = {
        92: 'nova',
        91: 'aqua',
        100: 'disinfector',
        7: 'vip',
        10: 'contributor',
        12: 'royal',
        38: 'legendary',
        102: 'coder',
        99: 'godly',
        8: 'reverser',
        73: 'retired',
        6: 'mod',
        109: 'admin',
    }

    def get_user_info(self, user_name_or_id, secure_hash='', session_id=''):
        '''
        Get nulled user info from username or user ID
        '''
        try:
            user_name_or_id = int(user_name_or_id)
        except ValueError:
            if secure_hash == '':
                return {'user_found':False,'error':(True,'NULL_SECURE_HASH')}
            if session_id == '':
                return {'user_found':False,'error':(True,'NULL_SESSION_ID')}
            try:
                a = self.search_user(user_name_or_id,secure_hash,session_id)
            except ValueError:
                return {'user_found':False,'error':(True,'BAD_SESSION_ID_OR_CF_ERROR')}
            user_name_or_id = [x for x in a if a[x]['name'].lower() == user_name_or_id][0]
        try:
            r = requests.get('https://chat-ssl2.nulled.to/api/user/'+str(user_name_or_id)).json()['data']['user']
        except ValueError:
            return {'user_found':False,'error':(True,'BANNED_USER_OR_UNDOCUMENTED_CUSTOM_UG_KAPPA')}
        info = {'user_found':True}|dict((k,r[k]) for k in ['username','id','group','shouts','discord'])|{'error':(False,'NO_ERROR_USER_FOUND')}
        info['group'] = self.group_list[info['group']]
        return info

    def auth(self, auth_code:str):
        '''
        ----------
        Returns dictionary in the format below
        Example usage `print(nulled.auth('NULLED-5E72C-60984-4D332-5B526-X'))`
        ```json
        {
            'authenticated': True,
            'user_found': True,
            'username': 'M3GZ',
            'id': 4103370,
            'group': 'aqua',
            'shouts': 348,
            'discord': '_megz#1304',
            'error': (False, 'NO_ERROR_USER_FOUND')
        }
        ```
        Now you can limit parts of your programs for different usergroups Kappa
        
        Paramters
            auth_code : str
                Description: Nulled auth code (https://www.nulled.to/auth.php)
        '''

        r = requests.get('https://www.nulled.to/misc.php?action=validateKey&authKey='+md5(str.encode(auth_code)).hexdigest()).json()
        try:
            if r['auth']:
                return {'authenticated':True}|self.get_user_info(r['uid'])
            else:
                return {'authenticated':False}
        except KeyError:
            return {'authenticated':False}
    
    def search_user(self, username:str, secure_hash:str, session_id:str):
        headers = {'cookie':'nulledsession_id='+session_id+';'}
        try:
            a = requests.get('https://www.nulled.to/index.php?app=core&module=ajax&section=findnames&do=get-member-names&secure_key='+secure_hash+'&name='+username,headers=headers).json()
        except ValueError:
            return {'user_found':False,'error':(True,'BAD_SESSION_ID_OR_CF_ERROR')}
        return dict((k,{'name':a[k]['name'],'group':a[k]['showas'][a[k]['showas'][:a[k]['showas'].rfind('>')].rfind('>')+1:a[k]['showas'].find('<',a[k]['showas'][:a[k]['showas'].rfind('>')].rfind('>')+1)],'profile_pic':a[k]['img']}) for k in a)