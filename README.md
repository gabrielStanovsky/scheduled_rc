# scheduled_rc

A crappy message scheduler for Rocket.Chat.

## Setup

1. Install packages:
`pip install -r requirements.txt`

2. Setup a users file, see example [here](data/example_users.json). This maps from a user nickname of your choice to their RC id (I couldn't figure out how to do this reliably through the API).

## Usage
1. Put your messages along with intended send time in a message file. See example [here](data/example_messages.json).

2. Run the deamon:
`python daemon.py --usrs=PATH/TO/USERS --msgs=PATH/TO/MESSAGES --sleep=SLEEP-TIME-IN-MINUTES --uname=YOUR-USERNAME --pwd=YOUR-PASSWORD --domain=YOUR-RC-DOMAIN`

3. You can update the messages file without restarting the deamon.
