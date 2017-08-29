# class SmaAccount():
#     account_type = ''
#     realname = ''
#     username = ''
#     location = ''
#     gender = ''
#     age = ''
#     job = ''
#     job_place = ''
#     status = ''

#     @classmethod
#     def __init__(cls, account_dict):
#         cls.account_type = account_dict['account_type']
#         cls.realname = account_dict['realname']
#         cls.username = account_dict['username']
#         cls.location = account_dict['location']
#         cls.gender = account_dict['gender']
#         cls.age = account_dict['age']
#         cls.job = account_dict['job']
#         cls.job_place = account_dict['job_place']
#         cls.status = account_dict['status']

#     @classmethod
#     def to_dict(cls):
#         return {'account_type' : cls.account_type,
#                 'realname' : cls.realname,
#                 'username' : cls.username,
#                 'location' : cls.location,
#                 'gender' : cls.gender,
#                 'age' : cls.age,
#                 'job' : cls.job,
#                 'job_place' : cls.job_place,
#                 'status' : cls.status
#                }

#     @classmethod
#     def from_dict(cls, account_dict):
#         cls.account_type = account_dict['account_type']
#         cls.realname = account_dict['realname']
#         cls.username = account_dict['username']
#         cls.location = account_dict['location']
#         cls.gender = account_dict['gender']
#         cls.age = account_dict['age']
#         cls.job = account_dict['job']
#         cls.job_place = account_dict['job_place']
#         cls.status = account_dict['status']

#     @classmethod
#     def copy(cls, account_class):
#         return SmaAccount({'account_type' : account_class.account_type,
#                            'realname' : account_class.realname,
#                            'username' : account_class.username,
#                            'location' : account_class.location,
#                            'gender' : account_class.gender,
#                            'age' : account_class.age,
#                            'job' : account_class.job,
#                            'job_place' : account_class.job_place,
#                            'status' : account_class.status
#                          })