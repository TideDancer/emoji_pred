sudo apt-get update
sudo apt-get install -y python2-dev python-pip
sudo apt-get install -y wget unzip

wget --no-verbose "https://github.com/bfelbo/DeepMoji/archive/master.zip" && unzip master.zip
mv DeepMoji-master deepmoji
rm master.zip
cd deepmoji

pip2 install . 
pip2 install tensorflow==1.5.0 numpy==1.13.1 pandas flask

yes | python2 scripts/download_weights.py && mkdir -p api

cd api && echo "" > __init__.py
cd ../
cp ../server.py api/ 
cp ../emoji-lookup.csv . 

