from core.errors import ClientError

# ----------------------------- Setting Input Types

TEXT = "text"
NUMBER = "number"
TEXTAREA = "textarea"
# ------------------------------- key types
class Setting:
    def __init__(self, label, value, tp, desc, hint) -> None:
        self._value = value
        self._label = label
        self._tp = tp

        self._desc = desc
        self._hint = hint

    def get_value(self):
        if self._tp == NUMBER:
            return int(self._value)
        return self._value
    
    def set_value(self, value):
        self._value = value

    def get_setting(self):
        return {
            "label": self._label,
            "value": self._value,
            "tp": self._tp,
            "desc": self._desc,
            "hint": self._hint
        }

def create_setting(label, value, tp = TEXT, desc = "", hint = ""):
    return Setting(label, value, tp, desc, hint)
# ------------------------------------------
BASIC = {
    # starting new room limit
    "new_room_limit": create_setting("Room limit", 2, NUMBER, "New public rooms limit", hint="Maybe 2 is fine 😁"),
    # groups limit
    "rooms_limit": create_setting("Rooms Create Limit", 100, NUMBER, "Specify how many rooms can be created", hint="Rooms That can run in this server"),
    # Allow new users
    "allow_new_rooms": create_setting("Allow New Rooms", "Yes", TEXT, desc="Users can create new rooms", hint="Yes | No"),
    # blocked usernames
    "blocked_names": create_setting("Blocked Names", "", TEXTAREA, desc="Blocked usernames", hint="use commas seperated ex: A B"),
}
# ------------------------------------------ TODO impl catch later
def get_setting(key):
    setting = BASIC.get(key)
    if setting: return BASIC[key].get_value()

    raise ClientError("Something Went wrong with settings")