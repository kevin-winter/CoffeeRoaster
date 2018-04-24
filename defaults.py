# Sensor Data
samplefreq = 5 #Hz
max_recorded = int(10*60*samplefreq)

# Main Page
refresh_rate = 1 #Hz

# Roasting
profile = 4
profiles = {
    0: ("Cinnomon", 196),
    1: ("New England", 205),
    2: ("American", 210),
    3: ("City", 219),
    4: ("Full City", 225),
    5: ("Vienna", 230),
    6: ("French", 240),
    7: ("Italien", 245),
    8: ("Custom",)}


nr_profiles = len(profiles)

roasttime = 4*60
min_roasttime = 30
max_roasttime = 30*60

roasttemp = 230
min_roasttemp = 180
max_roasttemp = 300

preheat = "PH"

HEATING = 0
FAN = 1
BEAN_ENTRANCE = 2
BEAN_EXIT = 3

TESTLED = 100