# Instructions to run on Mac OS X

# If pip is not installed in system, then install using instructions here https://pip.pypa.io/en/latest/installing.html

# Install virtualenv
pip install virtualenv

# Create environment
virtualenv crawler_env

# Activate environment
cd crawler_env
source bin/activate

# Copy files (app.py, crawler.py and requirements.txt) into crawler_env directory

# Install dependecies
pip install -r requirements.txt

# Now run server
python app.py



# To run, just curl the localhost api endpoint like this
curl http://localhost:5000/api/v1.0/crawl?url=http%3A%2F%2Fwww.workshopsf.org%2F%3Fpage_id%3D140%26id%3D1328

# Need to percent-escape the url param
# http://www.sfmoma.org/exhib_events/exhibitions/513 -> http%3A%2F%2Fwww.sfmoma.org%2Fexhib_events%2Fexhibitions%2F513
# http://www.workshopsf.org/?page_id=140&id=1328 -> http%3A%2F%2Fwww.workshopsf.org%2F%3Fpage_id%3D140%26id%3D1328
# http://events.stanford.edu/events/353/35309/ -> http%3A%2F%2Fevents.stanford.edu%2Fevents%2F353%2F35309%2F
# To do this in python, just bring up a python shell
python
# Then run the following in shell
from urllib import urlencode
urlencode({'url': 'http://www.sfmoma.org/exhib_events/exhibitions/513'})

