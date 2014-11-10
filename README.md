# Forky

Forky is a irc bot based on willie but uses django models for database actions. 

This bot is not fully compatible anymore with all willie modules, but it does not take much refactoring. 

While still heavily under development, both the bootstrap web interface, as the user interaction through the irc bot 
are both kinda sorta functional 

This bot does not send passwords in plain text to the irc bot, but uses a token based system, where after each action, 
your token is automagically refreshed, this way avoiding you to use the password of you registered user account to be send over irc. 

At the moment most of the modules don't require a token to use the module, but check for a is_login flag, which is atm only 
set at login, but never unchecked when parting/disconnecting/in time/etc so still lots to do :) 

Feel free to join me in this irc project! i love pull requests so please do :)


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

## Work in Progress:
- [ ] Quotes
- [ ] Add created by field in model 
- [ ] fix carousel 
- [ ] allow creation for quotes not the user itself, but everyone

- [ ] add quote module 
- [ ] complain  quote function 
- [ ] complain module that taggs users 
- [ ] if complain N times => take user rights to set quotes etc 
- [ ] 


### Django frontend

- [X] User registration through django web ui link and email
- [X] adjust user registration to notify token through private message OR email
- [X] Token generation for IRC "login"
- [X] Create user edit profile page for non admin users
- [X] Write socket client package
- [X] control bot page (connect to socket)
- [X] send to channel/priv functionality (also msg oneself to change settings)
- [X] api view to send data to channel using registration token or user/pass
- [X] socket listener buttons in profile
- [ ] live log for superusers (all events logged to db)
- [ ] proper edit profile page with more then just a basic django form
- [ ] http://bixly.com/blog/awesome-forms-django-crispy-forms/
- [ ] items apps to view ones quotes/infoitems/etc
- [ ] -Fully- implement register/login through email AND bot 
- [ ] http://cssdeck.com/labs/twitter-bootstrap-tabbed-login-and-signup-register-forms-interface

### Bot
- [X] .meet <user> module to start the registration process
- [X] about information module
- [X] auto reload (all) module(s) functionality
- [X] restrict modules to the corresponding user status
- [X] login/register module
- [X] socket listener to send raw irc to server
- [X] check if user is login or reply in restriction 
- [X] rewrite decrypt / socket server thing to log incoming data for each user
- [ ] trigger module that updates seen data
- [ ] .seen <user> module that gets the last seen data from database
- [ ] quotes module 
- [ ] auto ban on join
- [ ] hard exit on disconnection
- [ ] supervisor task to keep the bot running
- [ ] auto load module 
- [ ] listener module that auto logout all parted/quitted/left
- [ ] auto channel to +i mode
- [ ] superuser module to request all data of a user, send in privmsg
- [ ] fix endless reload loop in multiple threads while func.thread(False)
- [ ] socket listener control protocol + options to start/stop/reload the bot
- [ ] remove any other user restriction but the ones in the user model
- [ ] get settings from django models instead of a huge django.conf.settings 


### ORM
- [X] adjust willie modules to use django orm and add to modules + initial_data.json
- [X] Quotes Model
- [X] Separate models into apps
- [ ] Last seen field in user model
- [ ] edit django settings module or store all non-django settings in database
- [ ] channel modes in channel model
- [ ] event/socket_logging/channel_logging model for stats etc, with rotation 
- [ ] settings table for all irc/socket/application settings that are NOT Django
