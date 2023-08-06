import os
import json

from .verbose import VERBOSE
from .utils import check_password, gen_password
guest_properties_required = [
    "firstname",
    "familyname",
    "email",
    "description",
    "date_of_birth",
    "host_organization",
    "host_npid",
    "mail_technical_contact",
    "admin_group",
    "valid_from",
    "valid_until",
    "notification",
]
guest_properties_optional = [
    "title",
]


class Person():
    def __init__(self, conn, data=None, **keyvals):
        """create or update a new (guest) identity in IAM.
        Following properties are required:
        - firstname
        - familyname
        - email
        - description
        - date_of_birth
        - host_organization
        - host_npid
        - mail_technical_contact
        - admin_group
        - valid_from
        - valid_until
        - notification
        
        The following properties are optional:
        - title

        """
        self.conn = conn
        self.data = data
        self.npid = None
        self.firstname = None
        self.familyname = None
        self.email = None
        self.description = None
        self.date_of_birth = None
        self.host_organization = None
        self.host_npid = None
        self.mail_technical_contact = None
        self.admin_group = None
        self.valid_from = None
        self.valid_until = None
        self.title = None

        if data:
            self.is_new = False
            for key in data:
                setattr(self, key, data[key])
        else:
            self.is_new = True
            for key in guest_properties_required:
                if key in keyvals:
                    setattr(self, key, keyvals[key])
                else:
                    raise ValueError(f"the {key} property is required.")
        
    def save(self):
        body = { key: getattr(self, key, None) for key in guest_properties_required + guest_properties_optional}
        if self.is_new:
            endpoint = '/usermgr/person/'
            resp = self.conn._post_request(endpoint, body)
            action = 'created'
        else:
            endpoint = f'/usermgr/person/{self.npid}'
            resp = self.conn._put_request(endpoint, body)
            action = 'updated'

        if resp.ok:
            # TODO: get the new npid from post request?
            if VERBOSE:
                print(f"Person {self.firstname} {self.familyname} was successfully {action}")
        elif resp.status_code == 401:
            raise ValueError('the provided admin-username/password is incorrect or you are not allowed to create/update this person')
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(f"unable to create/update this person: {data['message']}")
        
    def __getitem__(self, key):
        return getattr(self, key, self.data.get(key))
            
    def new_user(self, username, password=None, firstname=None, familyname=None, mail=None, description=None):
        if len(username) < 6:
            raise ValueError('Usernames must be 6 chars or longer')
        if password is None:
            password = gen_password()
        elif not check_password(password):
            raise ValueError('the initial password must contain at least Lowercase, uppercase characters and a digit')
        if description is None:
            description = username
        endpoint = '/usermgr/person/{}'.format(self.npid)
        body = {
            "username": username,
            "init_passwd": password,
            "memo": description,
        }
        resp = self.conn._post_request(endpoint, body)
        if resp.ok:
            user = self.conn.get_user(username)
            user.init_password = password
            if VERBOSE:
                print("new user {} was successfully created".format(username))
            return user
        elif resp.status_code == 401:
            raise ValueError('Provided admin-username/password is incorrect or you are not allowed to do this operation')
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])
