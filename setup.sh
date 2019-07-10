

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y python3 
sudo apt-get install -y python3-dev
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-tk


pip3 install flask gunicorn pymongo Flask-Cors

cd flask_app
EXPOSE 8000
gunicorn -b 0.0.0.0:8000 app
