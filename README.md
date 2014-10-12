# Django IRC Bot

Django irc bot is based on willie but uses django models for database actions. 



## TODO
 
### Django frontend

- [ ] User registration through django web ui link and email
- [ ] Token generation for IRC "login"
- [ ] Edit user profile page for non admin users
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
