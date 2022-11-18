echo "Cloning Repository"
git clone https://github.com/BikashTG/TECH_RENAME_BOT /TECH_RENAME_BOT
cd /TECH_RENAME_BOT 
echo "installing requirements"
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
