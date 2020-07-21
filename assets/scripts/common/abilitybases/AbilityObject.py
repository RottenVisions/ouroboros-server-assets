# -*- coding: utf-8 -*-
import Ouroboros
from OURODebug import *
import GlobalConst

class AbilityObject:
	def __init__(self):
		self._id = 0
		self._name = ''
		self._level = 0
		self._icon = ''
		self._apCost = -1
		self._school = ''
		self._speed = 0
		self._costType = 0
		self._castingTime = 0.0
		self._rangeMin = 0.0
		self._rangeMax = 0.0
		self._isRotate = False
		self._cooldown = 0.0
		self._maxReceiverCount = 999
		self._selfCasting = False

		self._cost = 0

		self._onCooldown = False
		self._cooldownFinishedTime = -1
		self._casting = False
		self._castingFinishedTime = -1
		self._traveling = False
		self._travelingFinishedTime = -1

		self._active = False
		self._contacted = False

	def loadFromDict(self, dictDatas):
		"""
		virtual method.
		Create this object from the dictionary
		"""
		self._id = dictDatas.get('id', 0)
		self._name = dictDatas.get('name', '')
		self._level = dictDatas.get('level', 0)
		self._icon = dictDatas.get('icon', '')
		self._apCost = dictDatas.get('apCost', -1)
		self._school = dictDatas.get('school', '')
		self._costType = dictDatas.get('costType', 0)
		self._cost = dictDatas.get('cost', 0)
		self._selfCasting = dictDatas.get('selfCasting', False)

		# Ability speed
		self._speed = dictDatas.get('speed', 0)

		# Casting time
		self._castingTime = dictDatas.get("castingTime", 0.0)

		# Minimum and maximum range of application
		self._rangeMin = dictDatas.get('rangeMin', 0)
		self._rangeMax = dictDatas.get('rangeMax', 2)

		# Casting turn
		self._isRotate	= dictDatas.get("isRotate", True)

		# Maximum number of operations
		self._maxReceiverCount = dictDatas.get("maxReceiverCount", 999)

		# Cooldown
		self._cooldown = dictDatas.get("cooldown", 0)
		#self.springCDs = dictDatas.get("springCDs", [])

	def getIsInPhase(self):
		return self.getCasting() or self.getTraveling() or self.getOnCooldown()

	def setActive(self, value):
		self._active = value

	def getActive(self):
		return self._active

	def getContacted(self):
		return self._contacted

	def setContacted(self, value):
		self._contacted = value

	def getID(self):
		return self._id

	def getName(self):
		return self._name

	def getLevel(self):
		return self._level

	def getIcon(self):
		return self._icon

	def getAPCost(self):
		return self._apCost

	def hasCastTime(self):
		return self._castingTime > 0.0

	def hasCost(self):
		return self._cost > 0.0

	def getCastTime(self):
		return self._castingTime

	def getCasting(self):
		return self._casting

	def setCasting(self, value):
		self._casting = value

	def setCastingFinishedTime(self, value):
		self._castingFinishedTime = value

	def getCastingFinishedTime(self):
		return self._castingFinishedTime

	def getSelfCasting(self):
		return self._selfCasting

	def getTravelTime(self):
		return self._travelTime

	def setTravelTime(self, value):
		self._travelTime = value

	def hasTravelTime(self):
		return self._travelTime >= GlobalConst.GC_ABILITY_ARRIVED_THRESHOLD

	def getTraveling(self):
		return self._traveling

	def setTraveling(self, value):
		self._traveling = value

	def setTravelingFinishedTime(self, value):
		self._travelingFinishedTime = value

	def getTravelingFinishedTime(self):
		return self._travelingFinishedTime

	def getCostType(self):
		return self._costType

	def getCost(self):
		return self._cost

	def getCooldown(self):
		return self._cooldown

	def hasCooldown(self):
		return self._cooldown > 0.0

	def getOnCooldown(self):
		return self._onCooldown

	def setOnCooldown(self, value):
		self._onCooldown = value

	def setCooldownFinishedTime(self, value):
		self._cooldownFinishedTime = value

	def getCooldownFinishedTime(self):
		return self._cooldownFinishedTime

	def getSchool(self):
		return self._school

	def getRangeMin(self):
		return self._rangeMin

	def getRangeMax(self):
		return self._rangeMax

	def getSpeed(self):
		return self._speed

	def isRotate(self):
		return self._isRotate

	def getMaxReceiverCount(self):
		return self._maxReceiverCount