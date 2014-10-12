# Django IRC Bot

Django irc bot is based on willie but uses django models for database actions. 


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
- [ ] adjust user registration to notify token through private message OR email
- [ ] Token generation for IRC "login"
- [ ] Create user edit profile page for non admin users
- [ ] control bot page (connect to socket)
- [ ] live log 
- [ ] send to channel/priv functionality (also msg oneself to change settings)


### Bot
- [ ] .meet <user> module to start the registration process
- [ ] trigger module that updates seen data
- [ ] .seen <user> module that gets the last seen data from database
- [ ] about information module
- [ ] quotes module 
- [ ] auto ban on join
- [ ] superuser task to keep the bot running
- [ ] udp socket listener module to send data from other programmes
- [ ] socket listener to start/stop/reload the bot
- [ ] auto load module and auto reload (all) module(s) functionality

### ORM
- [ ] adjust willie modules to use django orm and add to modules + initial_data.json
- [ ] Quotes Model
- [ ] Last seen field in user model
- [ ] edit django settings module or store all non-django settings in database
