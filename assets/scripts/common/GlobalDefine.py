"""
"""

# ------------------------------------------------------------------------------
# Entity State
# ------------------------------------------------------------------------------
ENTITY_STATE_UNKNOWN									= -1
ENTITY_STATE_FREE										= 0
ENTITY_STATE_DEAD										= 1
ENTITY_STATE_REST										= 2
ENTITY_STATE_FIGHT										= 3
ENTITY_STATE_MAX    									= 4
ENTITY_STATE_STUNNED   									= 5

# Sub State
ENTITY_SUB_STATE_NORMAL									= 0
ENTITY_SUB_STATE_RANDOM_STROLL							= 1
ENTITY_SUB_STATE_GO_BACK								= 2
ENTITY_SUB_STATE_CHASE_TARGET							= 3
ENTITY_SUB_STATE_FLEE									= 4

# Some behavioral prohibition signs
FORBID_NO												= 0x00000000
FORBID_MOTION											= 0x00000001
FORBID_CHAT												= 0x00000002
FORBID_SPELL											= 0x00000004
FORBID_TRADE											= 0x00000008
FORBID_EQUIP											= 0x00000010
FORBID_INTONATE											= 0x00000020
FORBID_ATTACK_PHY_NEAR									= 0x00000040
FORBID_ATTACK_PHY_FAR									= 0x00000080
FORBID_ATTACK_MAGIC										= 0x00000080
FORBID_YAW												= 0x00008000

FORBID_ATTACK_PHY = FORBID_ATTACK_PHY_NEAR | FORBID_ATTACK_PHY_FAR
FORBID_ATTACK_MAG = FORBID_ATTACK_MAGIC
FORBID_ATTACK = FORBID_ATTACK_PHY | FORBID_ATTACK_MAG
FORBID_MOTION_YAW = FORBID_MOTION | FORBID_YAW

FORBID_ALL = [
	FORBID_MOTION,
	FORBID_YAW,
	FORBID_CHAT,
	FORBID_ATTACK,
	FORBID_SPELL,
	FORBID_TRADE,
	FORBID_EQUIP,
	FORBID_INTONATE,
	FORBID_ATTACK_PHY_NEAR,
	FORBID_ATTACK_PHY_FAR,
	FORBID_ATTACK_MAGIC,
]

FORBID_ACTIONS = {
	ENTITY_STATE_UNKNOWN  : 0,
	ENTITY_STATE_FREE    : FORBID_NO,
	ENTITY_STATE_DEAD    : FORBID_MOTION_YAW | FORBID_TRADE | FORBID_ATTACK | FORBID_SPELL | FORBID_EQUIP,
	ENTITY_STATE_REST    : FORBID_MOTION_YAW | FORBID_TRADE | FORBID_ATTACK | FORBID_SPELL | FORBID_EQUIP,
	ENTITY_STATE_FIGHT   : FORBID_EQUIP | FORBID_TRADE,
	}

for f in FORBID_ALL: FORBID_ACTIONS[ENTITY_STATE_UNKNOWN] |= f

TYPE_NONE = 999

# ------------------------------------------------------------------------------
# Types - Source
# ------------------------------------------------------------------------------

SOURCE_TYPE_AURA = 0
SOURCE_TYPE_ABILITY = 1
SOURCE_TYPE_OTHER = 2

# ------------------------------------------------------------------------------
# Schools
# ------------------------------------------------------------------------------

SCHOOL_EVERYTHING 	= -2
SCHOOL_UNKNOWN 		= -1
SCHOOL_NONE 		= 0
SCHOOL_PHYSICAL		= 1
SCHOOL_FIRE 		= 2
SCHOOL_FROST 		= 3
SCHOOL_SHADOW 		= 4
SCHOOL_HOLY 		= 5
SCHOOL_DARK 		= 6
SCHOOL_LIGHT		= 7
SCHOOL_NATURE 		= 8
SCHOOL_MIRROR 		= 9
SCHOOL_MUD			= 10
SCHOOL_SPATIAL 		= 11
SCHOOL_DEMON 		= 12
SCHOOL_METAL 		= 13
SCHOOL_BLOOD 		= 14
SCHOOL_SONG 		= 15
SCHOOL_SUMMONING	= 16
SCHOOL_NUTRITION 	= 17

# ------------------------------------------------------------------------------
# Effects
# ------------------------------------------------------------------------------

EFFECT_DAMAGE_OVER_TIME 	= 0
EFFECT_HEAL_OVER_TIME 		= 1
EFFECT_FEAR 				= 2
EFFECT_CONFUSION			= 3
EFFECT_ROOT 				= 4
EFFECT_IMMUNITY 			= 5
EFFECT_SPECIAL 				= 6
EFFECT_INCREASE 			= 7
EFFECT_DECREASE				= 8
EFFECT_SLOW 				= 9
EFFECT_SUMMON 				= 10
EFFECT_BLIND				= 11

# ------------------------------------------------------------------------------
# Ability Effects Proc
# ------------------------------------------------------------------------------

EFFECT_APPLY_ORDER_START				= 0
EFFECT_APPLY_ORDER_TIME					= 1
EFFECT_APPLY_ORDER_FINISH				= 2

# ------------------------------------------------------------------------------
# Ability Effects Proc
# ------------------------------------------------------------------------------

EFFECT_PROC_NONE							= 0
EFFECT_PROC_ANY_HIT							= 1
EFFECT_PROC_ON_ENEMY_HIT					= 2
EFFECT_PROC_ON_EXP_GAIN						= 3
EFFECT_PROC_ON_CRIT_HIT_VICTIM				= 4
EFFECT_PROC_ON_CAST_ABILITY					= 5
EFFECT_PROC_ON_PHYSICAL_ATTACK_VICTIM		= 6
EFFECT_PROC_ON_RANGED_ATTACK				= 7
EFFECT_PROC_ON_RANGED_CRIT_ATTACK			= 8
EFFECT_PROC_ON_PHYSICAL_ATTACK				= 9
EFFECT_PROC_ON_MELEE_ATTACK_VICTIM			= 10
EFFECT_PROC_ON_ABILITY_HIT					= 11
EFFECT_PROC_ON_RANGED_CRIT_ATTACK_VICTIM	= 12
EFFECT_PROC_ON_CRIT_ATTACK					= 13
EFFECT_PROC_ON_RANGED_ATTACK_VICTIM			= 14
EFFECT_PROC_ON_PRE_DISPEL_AURA_VICTIM		= 15
EFFECT_PROC_ON_ABILITY_LAND_VICTIM			= 16

# ------------------------------------------------------------------------------
# Attributes
# ------------------------------------------------------------------------------

ATTRIBUTE_HEALTH 			= 0
ATTRIBUTE_ENERGY 			= 1
ATTRIBUTE_WILL				= 2
ATTRIBUTE_STRENGTH 			= 3
ATTRIBUTE_ENDURANCE 		= 4
ATTRIBUTE_ATTACK_POWER		= 5
ATTRIBUTE_DEFENSE_POWER		= 6
ATTRIBUTE_DODGE 			= 7
ATTRIBUTE_BLOCK				= 8
ATTRIBUTE_PARRY 			= 9
ATTRIBUTE_CRITICAL 			= 10
ATTRIBUTE_HIT				= 11
ATTRIBUTE_STEALTH			= 12

# ------------------------------------------------------------------------------
# Define conversation related
# ------------------------------------------------------------------------------
DIALOG_TYPE_NORMAL			= 0 # Ordinary conversation
DIALOG_TYPE_QUEST			= 1 # Task dialogue

# ------------------------------------------------------------------------------
# Ability related
# ------------------------------------------------------------------------------
# Ability object category
ABILITY_OBJECT_TYPE_UNKNOWN		= 0
ABILITY_OBJECT_TYPE_ENTITY		= 1
ABILITY_OBJECT_TYPE_POSITION	= 2

ABILITY_COST_TYPE_HP			= 0
ABILITY_COST_TYPE_EG			= 1
ABILITY_COST_TYPE_BOTH			= 2

ABILITY_TARGET_TYPE_SELF					= 0
ABILITY_TARGET_TYPE_SINGLE					= 1
ABILITY_TARGET_TYPE_MULTIPLE				= 2
ABILITY_TARGET_TYPE_AREA_OF_EFFECT			= 3

ABILITY_TYPE_INCREASE					= 0
ABILITY_TYPE_DECREASE					= 1
ABILITY_TYPE_REMOVE						= 2
ABILITY_TYPE_INTERRUPT					= 3

ABILITY_CALCULATION_POSITION_SOURCE					= 0
ABILITY_CALCULATION_POSITION_DESTINATION			= 1

# ------------------------------------------------------------------------------
# Aura related
# ------------------------------------------------------------------------------
# Aura object category
AURA_OBJECT_TYPE_UNKNOWN	= 0
AURA_OBJECT_TYPE_ENTITY		= 1

AURA_UPDATE_ADDED			= 0
AURA_UPDATE_REMOVED			= 1
AURA_UPDATE_REFRESHED		= 2
AURA_UPDATE_FINISHED		= 3
AURA_UPDATE_STACKED			= 4

# ------------------------------------------------------------------------------
# Aura Target Type
# ------------------------------------------------------------------------------

AURA_TARGET_TYPE_SELF					= 0
AURA_TARGET_TYPE_SINGLE					= 1
AURA_TARGET_TYPE_MULTIPLE				= 2
AURA_TARGET_TYPE_AREA_OF_EFFECT			= 3

# ------------------------------------------------------------------------------
# Attribute
# ------------------------------------------------------------------------------

ATTRIBUTE_BURNING				= 0
ATTRIBUTE_FREEZING				= 1
ATTRIBUTE_SLOWED				= 2
ATTRIBUTE_CONFUSED				= 3
ATTRIBUTE_FEARED				= 4
ATTRIBUTE_CURSED				= 5
ATTRIBUTE_ROOTED				= 6
ATTRIBUTE_IMMUNE				= 7
ATTRIBUTE_STUNNED				= 8
ATTRIBUTE_BLEEDING				= 9
ATTRIBUTE_MALE					= 10
ATTRIBUTE_FEMALE				= 11
ATTRIBUTE_FRIENDLY				= 12
ATTRIBUTE_ENEMY					= 13

# ------------------------------------------------------------------------------
# Entity Motion State
# ------------------------------------------------------------------------------

ENTITY_MOTION_STATE_STATIONARY					= 0
ENTITY_MOTION_STATE_WALK						= 1
ENTITY_MOTION_STATE_RUN							= 2

# ------------------------------------------------------------------------------
# Entity Animation State
# ------------------------------------------------------------------------------

ENTITY_ANIMATION_STATE_IDLE						= 0
ENTITY_ANIMATION_STATE_WALK						= 1
ENTITY_ANIMATION_STATE_RUN						= 2
ENTITY_ANIMATION_STATE_ATTACK_1					= 3
ENTITY_ANIMATION_STATE_ATTACK_2					= 4
ENTITY_ANIMATION_STATE_ATTACK_3					= 5
ENTITY_ANIMATION_STATE_SPELL_READY_OMNI			= 6
ENTITY_ANIMATION_STATE_SPELL_CAST_OMNI			= 7
ENTITY_ANIMATION_STATE_SPELL_READY_DIRECTED		= 8
ENTITY_ANIMATION_STATE_SPELL_CAST_DIRECTED		= 9
ENTITY_ANIMATION_STATE_DEATH					= 10

# ------------------------------------------------------------------------------
# Entity Animation State
# ------------------------------------------------------------------------------

ENTITY_ABILITY_STATE_CASTING					= 0
ENTITY_ABILITY_STATE_LAUNCH_PROJECTILE			= 1
ENTITY_ABILITY_STATE_IMPACT						= 2
ENTITY_ABILITY_STATE_COOLDOWN_START				= 3
ENTITY_ABILITY_STATE_COOLDOWN_END				= 4
ENTITY_ABILITY_STATE_CAST_CANCELED				= 5
ENTITY_ABILITY_STATE_CHANNELING					= 6