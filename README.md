# Telegram Bot for capture grafana dashboard

## Disclaimer

Tujuan utama project ini adalah untuk memenuhi tugas kuliah saya, maka dari itu project ini masih sangat jauh dari kata sempurna.

## How to use

### Pre-requisites

1. Install Grafana & Prometheus stack, you can follow this article for install Grafana & Prometheus [LINK](https://medium.com/devops-dudes/install-prometheus-on-ubuntu-18-04-a51602c6256b). Then create dashboard, and panel for monitoring

2. Install grafana image render plugin via grafana cli on grafana server
   ```
   grafana-cli plugins install grafana-image-renderer
   ```
3. Install chrome & dependency

   ```
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo dpkg -i google-chrome-stable_current_amd64.deb

   # If you get error missing dependency
   sudo apt --fix-missing update
   sudo apt update
   sudo apt install -f

   # Then install chrome again
   sudo dpkg -i google-chrome-stable_current_amd64.deb
   ```
4. Create telegram bot, invite to a group, save token-bot and chat id. You can follow this article to create [telegram bot](https://www.alphr.com/telegram-create-bot/) and [get chat id](https://stackoverflow.com/a/38388851).

5. Pull this repository

   ```
   git pull https://github.com/fauzan-rafi/grafana-bot-telegram.git
   ```

6. Create Folder for save capture

   ```
   cd grafana-bot-telegram
   mkdir rendered
   ```

7. Configure for downloading image folder

   ```
   FILE_PATH = r"rendered/image.png"
   ```

8. Cofigure you grafana url, grafana api, dashboard id, bot token on main.py

9. Setup env python

10. Install requirements

11. Start bot
