## Testing
```bash
# setup discord api
echo 'DISCORD_TOKEN=YOUR_DISCORD_TOKEN' > .env

# setup virtualenv
python3 -m venv .venv
. .venv/bin/activate

# install deps
pip3 install discord
pip3 install bs4
pip3 install seleniumbase
pip3 install python-dotenv

# setup selenium
# install chrome from https://www.google.com/chrome/
sudo dpkg -i PATH/TO/google-chrome-stable_current_amd64.deb
# seleniumbase installs chromedriver for you
```

## Deploying
```bash
docker build -t chadgpt .  
docker run -t chadgpt
```
