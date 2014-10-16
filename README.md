# Django IRC Bot

Django irc bot is based on willie but uses django models for database actions. 

## Install 

### Prerequisistes
```bash 
    git clone git@github.com:fliphess/django-ircbot.git
    cd django-ircbot 
    pip install -r requirements.txt
    ./manage.py syncdb  
```

edit control/settings.py

### Running the webinterface: 
   ./manage.py runserver 
   
### Running the irc bot 
  ./start-ircbot 


## Registration Flow
1. Create user account on site, or be notified the register page using .meet <name>
2. Get email, visit link
3. Subscribed
4. Edit profile, set nick, hostname and other irc data 
5. Generate registration token 
6. msg bot /msg <botnick> register <token>
7. you are registered!

## Login Flow
1. Login to django web ui
2. Generate new registration token
3. msg bot /msg <botnick> login <token>
4. you are now logged in!


## TODO
 
### Django frontend

- [X] User registration through django web ui link and email
- [X] adjust user registration to notify token through private message OR email
- [X] Token generation for IRC "login"
- [X] Create user edit profile page for non admin users
- [ ] control bot page (connect to socket)
- [ ] live log 
- [ ] send to channel/priv functionality (also msg oneself to change settings)
- [ ] proper edit profile page with more then just a form
- [ ] easy page 
- [ ] api view to send data to channel using registration token or user/pass
- [ ] socket listener buttons in profile

### Bot
- [X] .meet <user> module to start the registration process
- [ ] trigger module that updates seen data
- [ ] .seen <user> module that gets the last seen data from database
- [X] about information module
- [ ] quotes module 
- [ ] auto ban on join
- [ ] superuser task to keep the bot running
- [ ] socket listener to start/stop/reload the bot
- [ ] auto load module 
- [X] auto reload (all) module(s) functionality
- [ ] listener module that auto logout all parted/quitted/left
- [ ] auto channel to +i mode

### ORM
- [X] adjust willie modules to use django orm and add to modules + initial_data.json
- [X] Quotes Model
- [ ] Last seen field in user model
- [ ] edit django settings module or store all non-django settings in database
