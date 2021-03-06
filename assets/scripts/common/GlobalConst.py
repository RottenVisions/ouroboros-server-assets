"""
"""
GC_OK								= 0x000
GC_ERROR							= 666

# Ability related
GC_ABILITY_INSUFFICIENT_EG			= 0x001		# Insufficient eg
GC_ABILITY_ENTITY_DEAD				= 0x002		# Entity is dead
GC_ABILITY_AP_CAP					= 200		# Max threshold for ability points
GC_ABILITY_ARRIVED_THRESHOLD		= 0.01
GC_ABILITY_OUT_OF_MAX_RANGE			= 0x003
GC_ABILITY_OUT_OF_MIN_RANGE			= 0x004
GC_ABILITY_COST_INSUFFICIENT_HP		= 0x005
GC_ABILITY_COST_INSUFFICIENT_EG		= 0x006
GC_ABILITY_ON_COOLDOWN				= 0x007
GC_ABILITY_SELF_CAST_FORBIDDEN		= 0x008
GC_ABILITY_CAST_NON_SOURCE_ENTITY	= 0x009
GC_ABILITY_IS_CASTING				= 0x010
GC_ABILITY_INVALID_TARGET_ENTITY	= 0x011
GC_ABILITY_GLOBAL_COOLDOWN_ACTIVE	= 0x012
GC_ABILITY_NOT_CASTABLE_WHILE_MOVING= 0x013
GC_ABILITY_NOT_IN_FOV				= 0x014

GC_AURA_SELF_CAST_ONLY				= 1

GC_INVALID_TARGET					= 301
GC_INVALID_ID 						= 302
GC_ALREADY_CASTING_ABILITY 			= 303
GC_INVALID_SOURCE					= 304

GC_ACCOUNT_AVATAR_LIMIT				= 3
GC_CURRENCY_CAP 					= 5000000
GC_EXPERIENCE_CAP 					= 10000000

GC_AUTO_ATTACK_INTERVAL				= 2.0
GC_GLOBAL_ABILITY_COOLDOWN			= 1.0

GC_AUTO_ATTACK_MELEE_DISTANCE		= 4.0

#Inventory
EMPTY_SLOT = -1  # Empty inventory  value
INVENTORY_OPERATION_ERROR = -1	 # Invalid inventory operation value
INVENTORY_OPERATION_FULL = -2
INVENTORY_OPERATION_EMPTY_SOURCE = -3 # Invalid source input
INVENTORY_OPERATION_EMPTY_DESTINATION = -7 # Invalid destination input
INVENTORY_OPERATION_ITEM_NONEXISTENT = -4
INVENTORY_OPERATION_INVALID_INDEX = -5	 # Invalid inventory operation value
INVENTORY_OPERATION_INVALID_COUNT = -6
INVENTORY_OPERATION_OVERFLOWED = -7
INVENTORY_OPERATION_COMPLETELY_FULL = -8
INVENTORY_OPERATION_OK = 99
INVENTORY_BASE_SIZE = 12
INVENTORY_EQUIPMENT_BASE_SIZE = 10
INVENTORY_SIZE_MAX = 100

INVENTORY_ITEM_CAN_NOT_USE = 101
INVENTORY_ITEM_CAN_NOT_EQUIP = 102

INVENTORY_TYPE_INVENTORY = 0
INVENTORY_TYPE_EQUIPMENT = 1

#Guild Rankings

LEADER = 0
CO_LEADER = 1
MEMBER = 2

#Guild Parameters
GUILD_NAME_LIMIT = 32
GUILD_CAPACITY = 50
GUILD_NOTICE_MAX_LENGTH = 128
GUILD_CREATION_PRICE = 2000

#Party & Raid
PARTY_CAPACITY = 5
MICRO_RAID_CAPACITY = 10
MINI_RAID_CAPACITY = 15
RAID_CAPACITY = 40

#Chat
CHAT_CHANNEL_GLOBAL_CAPACITY = 5

#Maps for different zones
idmo_maps = {
	b'Zone_1' : 6,
	b'Zone_2' : 3,
	b'Zone_3' : 2,
	b'' : 1,
}