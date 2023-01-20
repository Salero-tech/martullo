# martullo discrod bot
Martullo is a simple discord bot which responds to certain triggers (messages/words).

## Commands
Use your specified prefix before the command. I use ?.

### help
Gives a short overview over the available commands.
```
list triggers: ?triggers
add trigger: ?add [ trigger1 trigger2 ] response
Special key for response: !zeit! => time !name! => name
remove trigger: ?remove trigger name
```

### triggers
Gives a list of all the registerd triggers.$

### add
Allows to register new triggers.

!name! allows you to embed the senders name in the response.
!zeit! allow you to embed the current time in the response.

```
?add [ trigger1 trigger2 ... ] response

example:
?add [ time ] it is !zeit!
```

### remove
Allows to remove a trigger. 
Just specify one of the triggers.
```
?remove trigger

example:
?remove time
```

## install
1. Install docker & docker-compose.
2. Download the proviede docker-compse file.
3. Fill in your discord tocken, prefix & activity in the compose file.
4. Modify the location of your data folder for saving the triggers.
5. Run ```docker-compse up -d```