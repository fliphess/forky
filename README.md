# Forky

Forky is a irc bot based on willie but uses django models for database actions. 

This bot is not fully compatible anymore with all willie modules, but it does not take much refactoring. 

While still heavily under development, both the bootstrap web interface, as the user interaction through the irc bot 
are both kinda sorta functional 

This bot does not send passwords in plain text to the irc bot, but uses a one time password or "token" based mechanism 
for irc authenthication and registration, where after each action, your token is automagically refreshed, 
this way avoiding you to use the password of your registered user account to be send over irc. 

At the moment most of the modules don't require a token to use the module, but check for a is_login flag, which is atm only 
set at login, but never unchecked when parting/disconnecting/in time/etc so still lots to do :) 

As much as possible i'm trying to make this bot multiple channel supporting, but it does not make much separation. 
Operator, voice, banned etc are user based, so operator means operator on all channels the bot is in.

Feel free to join me in this irc project! i love pull requests so please do. I'm making a lot of changes at the moment, 
 so any contact would be appreciated :)


## Install 

### Prerequisistes
```bash
 
    git clone git@github.com:fliphess/django-ircbot.git
    cd django-ircbot 
    pip install -r requirements.txt
    ./manage.py syncdb  
    ./manage.py collectstatic
```

edit control/settings.py

### Running the webinterface: 
```
   ./manage.py runserver 0.0.0.0:8080 
```
   
### Running the irc bot 
```
  ./start-ircbot
```

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


## User restrictions
{
    0: 'user'
    1: 'registered and logged in'
    2: 'voice'
    3: 'operator'
    4: 'staff'
    5: 'superuser'
}

## Cool - TODO
- [ ] http://cssdeck.com/labs/twitter-bootstrap-tabbed-login-and-signup-register-forms-interface
- [ ] http://bixly.com/blog/awesome-forms-django-crispy-forms/


## Work in Progress:
`sys / first`
- [ ] "replace" origin with django model 
- [ ] - log events from socket server right after decryption and auth
- [ ] - Update last seen field in bot class where user_object is set

`orm`
- [ ] Create socket event model 
- [ ] Create irc event model 
- [ ] Create channel message model

`mods`
- [ ] Create log event module
- [ ] Create auto ban function on JOIN event module
- [ ] Create log message module
- [ ] listener module that auto logout all parted/quitted/left module
- [ ] .seen <user> module that gets the last seen data from database


### Django frontend
- [X] Quotes
- [X] items apps to view ones quotes/infoitems/etc
- [X] User registration through django web ui link and email
- [X] adjust user registration to notify token through private message OR email
- [X] Token generation for IRC "login"
- [X] Create user edit profile page for non admin users
- [X] Write socket client package
- [X] control bot page (connect to socket)
- [X] send to channel/priv functionality (also msg oneself to change settings)
- [X] api view to send data to channel using registration token or user/pass
- [X] socket listener buttons in profile
- [X] fix carousel 

- [ ] live log for superusers (all events logged to db)
- [ ] proper edit profile page with more then just a basic django form
- [ ] -Fully- implement register/login through email AND bot 

### Bot
- [X] .meet <user> module to start the registration process
- [X] about information module
- [X] restrict modules to the corresponding user status
- [X] login/register module
- [X] socket listener to send raw irc to server
- [X] check if user is login or reply in restriction 
- [X] rewrite decrypt / socket server thing to log incoming data for each user
- [X] add quote module 

- [ ] auto load module 
- [ ] auto channel to +i mode module
- [ ] superuser module to request all data of a user, send in privmsg
- [ ] auto reload (all) module(s) functionality
- [ ] fix endless reload loop in multiple threads while func.thread(False) in reload module
- [ ] remove any other user restriction but the ones in the user model
- [ ] create proper user restriction function or use the groups from django

### ORM
- [X] adjust willie modules to use django orm and add to modules + initial_data.json
- [X] Quotes Model
- [X] Separate models into apps
- [ ] edit django settings module or store all non-django settings in database
- [ ] channel modes in channel model
- [ ] event/socket_logging/channel_logging model for stats etc, with rotation 
- [ ] settings table for all irc/socket/application settings that are NOT Django

### System
- [ ] get settings from django models instead of a huge django.conf.settings 
- [ ] supervisor task to keep the bot running
- [ ] hard exit on disconnection or auto reconnect
- [ ] socket listener control protocol + options to start/stop/reload the bot
- [ ] request removal for info items quotes etc

