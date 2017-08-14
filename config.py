# simulation
# caution: this might fuck with physics if too fast
FAST_FORWARD_SCALE = 100

# generations
TIME_PER_GENERATION = 5
TOP_PROPORTION_TO_TAKE = 0.2
GENERATION_SIZE = 10

# mutating
MUTATE_NORMAL_MEAN = 0  # middle value
MUTATE_NORMAL_SD = 0.2  # variation
MUTATE_WEIGHT_CHANCE = 0.25

# entity
# 2 inputs (temp, time)
# 3 outputs (speed, direction, colour)
NET_LAYERS = [2, 3, 3]
ENTITY_DEFAULT_COLOUR = (0.9, 0.9, 0.9)
ENTITY_RADIUS = 8
ENTITY_MAX_FORCE = 60
SENSOR_LENGTH_LIMITS = (8, 16)

# world
WORLD_SIZE = (600, 600)
WORLD_TEMP_NOISE_SCALE = 200

# food
FOOD_RATE = 0.2  # seconds
INITIAL_FOOD_SIMULATION = 5  # seconds; count = this/FOOD_RATE
KEEP_SPAWNING_FOOD = True  # if false, only spawn initial food

# renderer
# beware, currently very slow
RENDER_TEMPERATURE = False
WINDOW_SIZE = WORLD_SIZE
