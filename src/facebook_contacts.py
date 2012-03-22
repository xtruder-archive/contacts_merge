from time import sleep
from urlparse import urlparse

import gdata.contacts.client
from selenium import webdriver
from facebook import GraphAPI
from functools_plus.functools_plus import struct_fields, struct, enum

school_type=enum("highs_school", "college")
            
@struct_fields(title=None, company=None)
class job(struct): 
    def __init__(self, *args): struct.__init__(self, args)
    
@struct_fields(name=None, type=None, year=None)
class education(struct):
    def __init__(self, *args): struct.__init__(self, args)
    
@struct_fields(email=None)
class email(struct):
    def __init__(self, *args): struct.__init__(self, args)

class Contact(object):
    _name=None
    _phonetic_name=None
    _nickname=None
    _job=[]
    _education=[]
    _email=[]
    _phone=[]
    _address=None
    _birthday=None
    _url=None
    _notes=None
    _picture=None
    
    @property
    def name(self): return self._name
    @name.setter
    def name(self, value): self._name= value
    
    @property
    def phonetic_name(self): return self._phonetic_name
    @phonetic_name.setter
    def phonetic_name(self, value, b): 
        self._phonetic_name= value
    
    @property
    def nickname(self): return self._nickname
    @nickname.setter
    def nickname(self, value): self._nickname= value
    
    @property
    def job(self): return self._job
    @job.setter
    def job(self, value): self._job= value
    
    @property
    def education(self): return self._education
    @education.setter
    def education(self, value): self._education= value
    
    @property
    def email(self): return self._email
    @email.setter
    def email(self, value): self._email= value
    
    @property
    def phone(self): return self._phone
    @phone.setter
    def phone(self, value): self._phone= value  

    @property
    def address(self): return self._address
    @address.setter
    def address(self, value): self._address= value  
    
    @property
    def birthday(self): return self._birthday
    @birthday.setter
    def birthday(self, value): self._birthday= value  
    
    @property
    def url(self): return self._url
    @url.setter
    def url(self, value): self._url= value  
    
    @property
    def notes(self): return self._notes
    @notes.setter
    def notes(self, value): self._notes= value  
    
    @property
    def picture(self): return self._picture
    @picture.setter
    def picture(self, value): self._picture= value  
    
    def update(self):
        pass

class FacebookContact(Contact):
    info=""
    picture=""
    
    @property
    def name(self):  
        if self._name:
            return self._name
        info= self.info       
        if(info.has_key("name")):
            return info["name"]
        else:
            name=""
            if(info.has_key("first_name")):
                name=info["first_name"]
            if(info.has_key("last_name")):
                name+=" "+info["first_name"]
                
            return name
        return None
    @name.setter
    def name(self, value): self._name= value
    
    @property
    def nickname(self):
        if self._nickname:
            return self._nickname
        info= self.info
        if(info.has_key("username")):
            return info["username"]
        return None
    @nickname.setter
    def nickname(self, value): self._nickname= value
    
    @property
    def job(self):
        if self._job:
            return self._job
        
        info= self.info
        jobs=[]
        if(info.has_key("work")):
            last_name=""
            for work in info["work"]: 
                if(work.has_key("employer")):
                    if(work["employer"]["name"]==last_name):
                        continue
                    last_name=work["employer"]["name"] 
                    if(work.has_key("position")):
                        jobs.append(job(work["position"]["name"] ,last_name))
                    else:
                        jobs.append(job("" ,last_name))
            return jobs
        return None
    @job.setter
    def job(self, value): self._job= value
    
    @property
    def education(self):
        if self._education:
            return self._education
        
        info= self.info
        if(info.has_key("education")):
            educations=[]
            for school in info["education"]:
                name=""
                type=""
                year=""
                
                if(school.has_key("school")):
                    name= school["school"]["name"]
                    if(school.has_key("year")):
                        year= school["year"]["name"]
                    if(school.has_key("type")):
                        type= school["type"]
                    
                    educations.append(education(name, type, year))
            return educations
        return None
    @education.setter
    def education(self, value): self._education= value
    
    @property
    def email(self): return self._email
    @email.setter
    def email(self, value): self._email= value
    
    @property
    def phone(self): return self._phone
    @phone.setter
    def phone(self, value): self._phone= value  

    @property
    def address(self):
        if self._address:
            return self._address
        
        info=self.info
        if(info.has_key("hometown") and info["hometown"]["name"] !="None"):
            return info["hometown"]["name"]
        return None
    @address.setter
    def address(self, value): self._address= value  
    
    @property
    def birthday(self):
        if self._birthday:
            return self._birthday
        
        info= self.info 
        if(info.has_key("birthday"))  :
            return info["birthday"]  
        return None 
    @birthday.setter
    def birthday(self, value): self._birthday= value  
    
    @property
    def url(self):
        if self._url:
            return self._url
        
        info= self.info
        if(info.has_key("website")):
            return info["website"]
        elif(info.has_key("link")):
            return info["link"]
        return None
    @url.setter
    def url(self, value): self._url= value  
    
    @property
    def notes(self):
        if self._notes:
            return self._notes
        
        info= self.info
        if(info.has_key("bio")):
            return info["bio"]
        return None
    @notes.setter
    def notes(self, value): self._notes= value   
    
    def __init__(self, info, picture):
        self.info= info
        self.picture= picture
        
class GoogleContact(Contact):
    gentry= None
    gclient= None
    
    @property
    def name(self):
        if self.gentry.name:
            self._name= self.gentry.name.full_name.text
            return self._name
        return None
    @name.setter
    def name(self, value): 
        self._name= value
        self.gentry.name.full_name= gdata.data.FullName(text=value)
    
    @property
    def nickname(self): 
        if self.gentry.nickname:
            self._nickname= self.gentry.nickname.text
            return self._nickname
        return None
    @nickname.setter
    def nickname(self, value):
        self._nickname= value
        self.gentry.nickname= gdata.contacts.Nickname(value)
    
    @property
    def job(self):
        if self.gentry.organization:
            self._job.append(job(self.gentry.organization.title.text, self.gentry.organization.name.text))
            return self._job
        return None
    @job.setter
    def job(self, value): 
        self._job= value
        self.gentry.organization= gdata.data.Organization(title=gdata.data.OrgTitle(text=value[0].title), name=gdata.data.OrgName(text=value[0].name))
    
    @property
    def education(self): return self._education
    @education.setter
    def education(self, value): self._education= value
    
    @property
    def email(self):
        for lemail in self.gentry.email:
            self._email.append(email(lemail.address))
        return self._email
    @email.setter
    def email(self, value): self._email= value
    
    @property
    def phone(self): return self._phone
    @phone.setter
    def phone(self, value): self._phone= value  

    @property
    def address(self): return self._address
    @address.setter
    def address(self, value): self._address= value  
    
    @property
    def birthday(self): return self._birthday
    @birthday.setter
    def birthday(self, value): self._birthday= value  
    
    @property
    def url(self): return self._url
    @url.setter
    def url(self, value): self._url= value  
    
    @property
    def notes(self): return self._notes
    @notes.setter
    def notes(self, value): self._notes= value  
    
    @property
    def picture(self):
        return self.gclient.GetPhoto(self.gentry)
    @picture.setter
    def picture(self, value):
        self.gclient.ChangePhoto(value, self.gentry, content_type='image/jpeg')
    
    def update(self):
        self.gclient.Update(self.gentry)
    
    def __init__(self, gentry, gclient):
        self.gentry= gentry
        self.gclient= gclient
        
class contacts_access:
    contacts=[]
    
    def GetFriends(self): 
        pass   
    
class google_contacts_access(contacts_access):
    username= "jakahudoklin@gmail.com"
    password= "2134567"
    client= None
    feed= None
    
    def GetContactsFeed(self):
        self.client= gdata.contacts.client.ContactsClient(source='xtruder-merge_contacts-v1')
        try:
            self.client.ClientLogin(self.username, self.password, self.client.source);
        except:
            return False
        
        query = gdata.contacts.client.ContactsQuery()
        query.max_results= 400
        try:
            self.feed = self.client.GetContacts(q=query)
        except:
            return False
        
        return True  
    
    def GetFriends(self): 
        if not self.feed:
            if not self.GetContactsFeed():
                return False
            
        for entry in self.feed.entry:
            name=""
            if entry.name:
                name= entry.name.full_name.text
            print "Adding new contact %s" %(name)
            
            self.contacts.append(GoogleContact(entry, self.client))
        
class facebook_contacts_access(contacts_access):
    APP_ID= 215453061808947
    #APP_PERMISSONS="user_about_me,friends_about_me,\
    #user_birthday,friends_birthday,user_education_history,friends_education_history,\
    #user_hometown,friends_hometown,user_photos,friends_photos,user_website,friends_website,\
    #user_work_history,friends_work_history,read_friendlists,email"
    APP_PERMISSONS="read_stream,manage_mailbox,manage_friendlists,read_mailbox,publish_checkins \
    ,status_update,photo_upload,video_upload,sms,create_event,rsvp_event,offline_access,email,xmpp_login \
    ,create_note,share_item,export_stream,publish_stream,publish_likes,ads_management,contact_email,access_private_data \
    ,read_insights,read_requests,manage_notifications,read_friendlists,manage_pages,physical_login,manage_groups,publish_actions \
    ,read_deals,app_notifications,whitelisted_offline_access,user_birthday,friends_birthday,user_religion_politics,friends_religion_politics \
    ,user_relationships,friends_relationships,user_relationship_details,friends_relationship_details,user_hometown,friends_hometown,user_location \
    ,friends_location,user_likes,friends_likes,user_activities,friends_activities,user_interests,friends_interests,user_education_history, \
    friends_education_history,user_work_history,friends_work_history,user_online_presence,friends_online_presence,user_website,friends_website \
    ,user_groups,friends_groups,user_events,friends_events,user_photos,friends_photos,user_videos,friends_videos,user_photo_video_tags,friends_photo_video_tags \
    ,user_notes,friends_notes,user_location_posts,friends_location_posts,user_checkins,friends_checkins,user_questions,friends_questions,user_friends, \
    friends_friends,user_about_me,friends_about_me,user_status,friends_status,user_address,friends_address,user_mobile_phone,friends_mobile_phone \
    ,user_games_activity,friends_games_activity,user_subscriptions,friends_subscriptions"
    
    APP_AUTHORIZE_URI='https://www.facebook.com/dialog/oauth?client_id=%d&redirect_uri=%s&scope=%s,&response_type=token'
    REDIRECT_URI= "https://www.facebook.com/connect/login_success.html"
    PHOTO_URI= "http://graph.facebook.com/%s/picture"
    
    access_token=None
    expire_time=None
    
    def __init__(self):
        pass
    
    def WaitForUrl(self, driver, uri):
        while not driver.current_url.count(self.REDIRECT_URI):
            sleep(0.5)
        return
    
    def ParseUrl(self,url):
        params = dict([part.split('=') for part in url.split('&')])
        return params
        
    def GetToken(self):
        driver= webdriver.Firefox()
        driver.get(self.APP_AUTHORIZE_URI %(self.APP_ID, self.REDIRECT_URI, self.APP_PERMISSONS))
        self.WaitForUrl(driver, self.REDIRECT_URI)
            
        url= self.ParseUrl(urlparse(driver.current_url).fragment)
        self.access_token=""
        if url.has_key("access_token"):
            self.access_token= url["access_token"]
        else:
            driver.close()
            return False
            
        self.expire_time= int(url["expires_in"])
        driver.close()
        return True
        
    def GetFriends(self):
        if not self.access_token:
            if not self.GetToken():
                return False
            
        self.contacts= []
            
        print self.access_token
        graph= GraphAPI(self.access_token)
        friends = graph.get_connections("me", "friends")
        for friend in friends["data"]:
            print "Adding", friend["name"]
            
            info= graph.get_object("%s" %(friend["id"]))
            print info
            picture= self.PHOTO_URI %(friend["id"])
            self.contacts.append(FacebookContact(info, picture))
            
        return True

if __name__ == "__main__":
    fb= google_contacts_access()
    fb.GetFriends()
    print "Result count: %d" %(len(fb.contacts))
    for contact in fb.contacts:
        print contact.name
        for email in contact.email:
            print email.email

