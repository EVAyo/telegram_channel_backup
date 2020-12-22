# telegram_channel_backup

Backup your telegram channel to md file. Backup every two hour, [change](https://github.com/gaoyunzhi/telegram_channel_backup/blob/master/channel_backup.py#L49). 

# Install
- Fork the repository and pull to your machine
- `pip3 install --user cached_url telegram_util bs4 --upgrade'`

# Customize
- In https://github.com/gaoyunzhi/telegram_channel_backup/blob/master/channel_backup.py, change line 11 to customize. 
- Format example: `channel_username: 1` 
- If you want to only backup message starting with message id x, do `channel_username: x`

# Run
- go to your local repository
- `nohup python3 setup.py &`
