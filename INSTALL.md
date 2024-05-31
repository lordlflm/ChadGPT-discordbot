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
```