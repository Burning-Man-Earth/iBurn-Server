import requests
import time
import hmac
import hashlib

#Sending Comment To Server


def get_security_hash(object_pk,content_type,timestamp,secret):
    '''
    Copying the security hash mechanism thats in 
    from django.utils.crypto import salted_hmac
    '''
    key_salt = "django.contrib.forms.CommentSecurityForm"
    key = hashlib.sha1(key_salt + secret).digest()
    info = (content_type, object_pk, str(timestamp))
    value = "-".join(info)
    security_hash = hmac.new(key, 
                    msg=value, 
                    digestmod=hashlib.sha1).hexdigest()
    return security_hash

def send_message(name,email,message,token,object_pk):
    '''
    Returns:
    201: Comment created.
    202: Comment in moderation.
    204: Comment confirmation has been sent by mail.
    403: Comment rejected, as in Disallow black listed domains.
    '''
       
    secret = 'Not a secret'
    content_type = 'blog.post'
    timestamp = int(time.time())
    headers = {}
    headers['comment']=message
    headers['name']=name
    headers['email']=email
    headers['timestamp']=timestamp
    headers['content_type']=content_type
    headers['object_pk']=str(object_pk)
    headers['honeypot']=''
    headers['security_hash']=get_security_hash(str(object_pk),
                                            content_type,
                                            timestamp,
                                            secret)
    r = requests.post('http://localhost:8000/comments/api/comment/',data=headers,
                     headers={'Authorization': 'Token {}'.format(token)})
    return r.status_code

def main():

    
    iburn_server_username = 'burner@iburn.com'
    iburn_server_password = 'burningman'
    server_address = 'http://localhost:8000'
    event_id = 20858



    '''
    Instructions for initial load
    python manage.py flush
    python manage.py loaddata fixtures/*
    python manage.py createsuperuser
    python manage.py runserver
    '''


    #Get Auth Token
    headers = {'username':iburn_server_username,'password':iburn_server_password}
    r = requests.post(server_address+'/api-token-auth/',data=headers)
    r.status_code
    token = r.json()['token']



    #Send Comment
    message = 'Comment from API!'
    name = 'Stephen'
    email = 'stephen.suffian@gmail.com'

    status = send_message(name,email,message,token,event_id)
    print(status)

    #Get Comments for Event
    headers = {'Authorization': 'Token {}'.format(token)}
    r = requests.get(server_address+'/comments/api/blog-post/{}/'.format(event_id),
                    headers=headers)
    print(r.json())

if __name__ == '__main__':
    main()

