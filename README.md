http://cs234.stanford.edu/

## Set up instructions
cd assignment1 <br/>
sudo pip install virtualenv      # This may already be installed <br/>
virtualenv .env                  # Create a virtual environment <br/>
source .env/bin/activate         # Activate the virtual environment <br/>
pip install -r requirements.txt  # Install dependencies <br/>
### Install Gym
git clone https://github.com/openai/gym
cd gym
pip install -e . # minimal install
### Work on the assignment for a while ...
deactivate                       # Exit the virtual environment
