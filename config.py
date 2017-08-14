# simulation
SPEED_SCALE = 1 # TODO move to simulator
FAST_FORWARD_TICK_PER_SECOND = 10

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
NET_LAYERS = [2, 20, 10, 10, 3]
ENTITY_DEFAULT_COLOUR = (0.9, 0.9, 0.9)

# world
WORLD_SIZE = (600, 600)
WORLD_TEMP_NOISE_SCALE = 80

# renderer
# beware, currently very slow
RENDER_TEMPERATURE = False
