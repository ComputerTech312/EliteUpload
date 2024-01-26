import hexchat
import re, random, string

__module_name__ = "Moderator Tools"
__module_version__ = "1.0"
__module_description__ = "A set of tools for channel moderators"

def kick_user(word, word_eol, userdata):
    if len(word) < 2:
        print("Usage: /KICK <nick>")
    else:
        hexchat.command("KICK {} :Kicked by moderator".format(word[1]))

def ban_user(word, word_eol, userdata):
    if len(word) < 2:
        print("Usage: /BAN <nick>")
    else:
        hexchat.command("MODE +b {}".format(word[1]))

def unban_user(word, word_eol, userdata):
    if len(word) < 2:
        print("Usage: /UNBAN <nick>")
    else:
        hexchat.command("MODE -b {}".format(word[1]))

def check_ban(word, word_eol, userdata):
    if len(word) < 2:
        print("Usage: /CHECKBAN <hostmask>")
    else:
        try:
            hostmask = word[1].replace('.', '\.').replace('*', '.*').replace('?', '.')
            pattern = re.compile(hostmask, re.IGNORECASE)
            users = hexchat.get_list("users")
            matching_users = [user for user in users if pattern.search(user.nick + "!" + user.host)]
            percentage = len(matching_users) / len(users) * 100
            print("Ban of {} would affect {} users ({:.2f}% of channel)".format(word[1], len(matching_users), percentage))
        except re.error:
            print("Invalid hostmask")

def quiet_user(word, word_eol, userdata):
    if len(word) < 2:
        print("Usage: /QUIET <nick>")
    else:
        modes = "vhoaq"
        for mode in modes:
            hexchat.command("MODE -{} {}".format(mode, word[1]))
        hexchat.command("MODE +b {}".format(word[1]))

def unquiet_user(word, word_eol, userdata):
    if len(word) < 2:
        print("Usage: /UNQUIET <nick>")
    else:
        hexchat.command("MODE -b {}".format(word[1]))

hexchat.hook_command("QUIET", quiet_user)
hexchat.hook_command("UNQUIET", unquiet_user)
'''
# Store the pending actions
pending_actions = {}

def mass_action(word, word_eol, userdata):
    global pending_actions

    if len(word) < 3:
        print("Usage: /MASSACTION <action> <hostmask>")
        print("Action can be KICK, BAN, or KICKBAN")
    elif word[1].upper() == "CONFIRM":
        if word[2] not in pending_actions:
            print("No action to confirm or confirmation string does not match")
        else:
            # Perform the action
            action, hostmask, matching_users = pending_actions[word[2]]
            for user in matching_users:
                if action == "KICK":
                    print(f"Executing command: KICK {user.nick}")
                    hexchat.command(f"KICK {user.nick}")
                elif action == "BAN":
                    print(f"Executing command: MODE +b {user.nick}")
                    hexchat.command(f"MODE +b {user.nick}")
                elif action == "KICKBAN":
                    print(f"Executing command: KICKBAN {user.nick}")
                    hexchat.command(f"KICKBAN {user.nick}")
            print(f"Performed {action} on {len(matching_users)} users matching {hostmask}")
            # Delete the confirmed action
            del pending_actions[word[2]]
            print(f"Deleted confirmation string {word[2]} from pending actions")
    else:
        try:
            action = word[1].upper()
            hostmask = word[2].replace('.', '\.').replace('*', '.*').replace('?', '.')
            pattern = re.compile(hostmask, re.IGNORECASE)
            users = hexchat.get_list("users")
            matching_users = [user for user in users if pattern.search(f"{user.nick}!{user.host}")]
            # Generate a random confirmation string
            confirmation_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            # Store the action details
            pending_actions[confirmation_string] = (action, hostmask, matching_users)
            print(f"To confirm, type: /MASSACTION CONFIRM {confirmation_string}")
        except re.error:
            print("Invalid hostmask")

hexchat.hook_command("MASSACTION", mass_action)
'''

def print(text):
    hexchat.prnt(text)

hexchat.hook_command("KICK", kick_user)
hexchat.hook_command("BAN", ban_user)
hexchat.hook_command("UNBAN", unban_user)
hexchat.hook_command("CHECKBAN", check_ban)

print("Moderator Tools loaded")