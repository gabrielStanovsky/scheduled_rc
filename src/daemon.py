""" Usage:
    <file-name> --usrs=USERS_FILE --msgs=MESSAGES_FILE --sleep=NUM_OF_MINUTES --uname=UNAME --pwd=PWD [--out=OUTPUT_FILE] [--debug]

Options:
  --help                           Show this message and exit
  -i INPUT_FILE --in=INPUT_FILE    Input file
                                   [default: infile.tmp]
  -o INPUT_FILE --out=OUTPUT_FILE  Input file
                                   [default: outfile.tmp]
  --debug                          Whether to debug
"""
# External imports
import logging
import pdb
from pprint import pprint
from pprint import pformat
from docopt import docopt
from pathlib import Path
from tqdm import tqdm
import json
from datetime import datetime
import time
from rocketchat.api import RocketChatAPI

# Local imports


#----

def get_messages_to_send(msgs_fn):
    """
    Get messages that need to be sent in this iteration, based on their time.
    Also updates the file to show that they were sent.
    TODO: update only on success.
    """
    msgs = [json.loads(line) for line in open(msgs_fn, encoding = "utf8")]
    updated_msgs = []
    msgs_to_send = []
    for msg in msgs:
        if msg.get("sent") is None:
            msg_time = datetime.strptime(msg["time"], "%d-%b-%Y %H:%M")
            now = datetime.now()
            if msg_time < now:
                # this message is due
                msgs_to_send.append(msg)
                msg["sent"] = True
        updated_msgs.append(msg)

    # write updated msgs to file in place only if something changed:
    if msgs_to_send:
        json_str = "\n".join([json.dumps(msg) for msg in updated_msgs])
        with open(msgs_fn, "w", encoding = "utf8") as fout:
            fout.write(json_str)
    
    return msgs_to_send

DOMAIN = 'https://rocketchat.cs.huji.ac.il/'
    
if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    usrs_fn = Path(args["--usrs"])
    msgs_fn = Path(args["--msgs"])
    sleep_in_mins = int(args["--sleep"])
    uname = args["--uname"]
    pwd = args["--pwd"] # <- this sucks

    # Determine logging level
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    logging.info(f"Users: {usrs_fn}, Messages file: {msgs_fn}.")

    # Start computation
    
    # log in to RC and do some dummy operation to make sure it's working
    api = RocketChatAPI(settings = {'username': uname,
                                    'password': pwd,
                                    'domain': DOMAIN})
    
    
    assert(api.get_public_rooms())
    
    users_dict = json.loads(open(usrs_fn, encoding = "utf8").read())
    sleep_duration = sleep_in_mins * 60
    logging.info("Listening...")
    while True:
        msgs_to_send = get_messages_to_send(msgs_fn)
        if msgs_to_send:
            logging.info(f"Sending: {msgs_to_send}")
            for msg in msgs_to_send:
                name = msg["name"] 
                uid = users_dict[name]
                msg_txt = msg["message"]
                logging.info(f"Attempting to send {msg_txt} to {name}")
                status = api.send_message(msg_txt, uid)
                if status["success"]:
                    logging.info("Sucess!")
                else:
                    logging.info("Failure!")
                
        time.sleep(sleep_duration)
    
    # End
    logging.info("DONE")
