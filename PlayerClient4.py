import os
import json
from dotenv import load_dotenv

import paho.mqtt.client as paho
from paho import mqtt
import time


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    """
        Prints the result of the connection with a reasoncode to stdout ( used as callback for connect )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param flags: these are response flags sent by the broker
        :param rc: stands for reasonCode, which is a code for the connection result
        :param properties: can be used in MQTTv5, but is optional
    """
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    """
        Prints mid to stdout to reassure a successful publish ( used as callback for publish )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param properties: can be used in MQTTv5, but is optional
    """
    print("mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    """
        Prints a reassurance for successfully subscribing
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param granted_qos: this is the qos that you declare when subscribing, use the same one for publishing
        :param properties: can be used in MQTTv5, but is optional
    """
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

game_over = False
# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    """
        Prints a mqtt message to stdout ( used as callback for subscribe )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param msg: the message with topic and payload
    """
    global current_position, walls

    print("message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

     # Check if the message indicates the game is over
    if msg.payload.decode() == "Game Over: Game has been stopped":
        game_over = True  # Set the flag to True to end the game loop
    elif 'game_state' in msg.topic:
        # Extracting current position and walls from the payload
        current_position = json.loads(msg.payload.decode()).get('currentPosition', [])
        walls = json.loads(msg.payload.decode()).get('walls', [])
        print(f"Current Position: {current_position}, Walls: {walls}")


#def next_move(current_pos, walls):
    # if [current_pos[0], current_pos[1] + 1] not in walls and (current_pos[1] + 1)>0 and (current_pos[1] + 1)<10:
    #     return "RIGHT"
    # elif [current_pos[0] - 1, current_pos[1]] not in walls and (current_pos[0] - 1)>0 and (current_pos[0] - 1)<10:
    #     return "UP"
    # elif [current_pos[0] + 1, current_pos[1]] not in walls and (current_pos[0] + 1)>0 and (current_pos[0] + 1)<10:
    #     return "DOWN"
    # elif [current_pos[0], current_pos[1] - 1] not in walls and (current_pos[1] - 1)>0 and (current_pos[1] - 1)<10:
    #     return "LEFT"
    # return "ERROR!"

# def next_move(current_pos, walls):
#     # Calculate potential moves based on the current position
#     moves = {
#         "RIGHT": [current_pos[0], current_pos[1] + 1],
#         "DOWN": [current_pos[0] + 1, current_pos[1]],
#         "LEFT": [current_pos[0], current_pos[1] - 1],
#         "UP": [current_pos[0] - 1, current_pos[1]]
#     }

#     # Order of preference for moves
#     preference = ["RIGHT", "DOWN", "LEFT", "UP"]

#     for direction in preference:
#         next_pos = moves[direction]
        
#         # Check if next position is not a wall and within bounds (assuming grid size 10x10 for simplicity)
#         if next_pos not in walls and 0 <= next_pos[0] < 10 and 0 <= next_pos[1] < 10:
#             return direction

#     # If no direction is valid (which shouldn't happen in most cases), return an error or a default action
#     return "ERROR!"

visited = set()  

def next_move(current_pos, walls):
    global visited

    moves = {
        "RIGHT": [current_pos[0], current_pos[1] + 1],
        "DOWN": [current_pos[0] + 1, current_pos[1]],
        "LEFT": [current_pos[0], current_pos[1] - 1],
        "UP": [current_pos[0] - 1, current_pos[1]]
    }

    visited.add(tuple(current_pos))

    unvisited_moves = {direction: pos for direction, pos in moves.items() if tuple(pos) not in visited and pos not in walls}
    visited_moves = {direction: pos for direction, pos in moves.items() if tuple(pos) in visited and pos not in walls}

    for direction, pos in unvisited_moves.items():
        if 0 <= pos[0] < 10 and 0 <= pos[1] < 10:
            return direction

    for direction, pos in visited_moves.items():
        if 0 <= pos[0] < 10 and 0 <= pos[1] < 10:
            return direction
        
    return "ERROR!"



if __name__ == '__main__':
    load_dotenv(dotenv_path='./credentials.env')
    
    broker_address = os.environ.get('BROKER_ADDRESS')
    broker_port = int(os.environ.get('BROKER_PORT'))
    username = os.environ.get('USER_NAME')
    password = os.environ.get('PASSWORD')

    client = paho.Client(callback_api_version=paho.CallbackAPIVersion.VERSION1, client_id="Player4_aut", userdata=None, protocol=paho.MQTTv5)
    
    # enable TLS for secure connection
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    client.username_pw_set(username, password)
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    client.connect(broker_address, broker_port)

    # setting callbacks, use separate functions like above for better visibility
    client.on_subscribe = on_subscribe # Can comment out to not print when subscribing to new topics
    client.on_message = on_message
    client.on_publish = on_publish # Can comment out to not print when publishing to topics

    lobby_name = "TestLobby"
    player_4 = "Player4"

    client.subscribe(f"games/{lobby_name}/lobby")
    client.subscribe(f'games/{lobby_name}/+/game_state')
    client.subscribe(f'games/{lobby_name}/scores')
    client.loop_start()

    client.publish("new_game", json.dumps({'lobby_name':lobby_name,
                                            'team_name':'BTeam',
                                            'player_name' : player_4}))

    time.sleep(1) # Wait a second to resolve game start
    client.publish(f"games/{lobby_name}/start", "START")
    time.sleep(20)

    while not game_over:
        print(current_position)
        print(walls)
        next_m = next_move(current_position,walls)
        client.publish(f"games/{lobby_name}/{player_4}/move", next_m)
        time.sleep(1)

    print("Game has ended!")
    client.publish(f"games/{lobby_name}/start", "STOP")
