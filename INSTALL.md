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
# find the newest stable version of chromdriver for testing and run:
wget https://storage.googleapis.com/chrome-for-testing-public/VERSION/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
#add chromedriver to path
sudo mv chromedriver-linux64 /usr/bin
```