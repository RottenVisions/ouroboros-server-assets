# -*- coding: utf-8 -*-
import Ouroboros
import random
import GlobalConst
import GlobalDefine
import ServerConstantsDefine
from OURODebug import *
from abilitybases.AbilityObject import AbilityObject
from abilitybases.AbilityCastObject import AbilityCastObject

class ActiveAbility(AbilityObject):
	def __init__(self):
		AbilityObject.__init__(self)
		self.castingAbilityTimer = -1
		self.castingAbilityDelay = -1
		self.scObject = None
		self.castingCaster = None

	def loadFromDict(self, dictDatas):
		"""
		virtual method.
		Create this object from the dictionary
		"""
		AbilityObject.loadFromDict(self, dictDatas)

		# Ability speed
		self.speed = dictDatas.get('speed', 0)

		# Casting time
		self.castingTime = dictDatas.get("castingTime", 0.0)

		# Minimum and maximum range of application
		self.rangeMin = dictDatas.get('rangeMin', 0)
		self.rangeMax = dictDatas.get('rangeMax', 2)
		self.__castMaxRange = dictDatas.get("rangeMaxAdd", 10.0)

		# Casting turn
		self.__isRotate	= dictDatas.get("isRotate", True)

		# Maximum number of operations
		self.maxReceiveCount = dictDatas.get("maxReceiverCount", 999)

		# cooldown
		self.limitCDs = dictDatas.get("limitCDs", [1])
		self.springCDs = dictDatas.get("springCDs", [])

	def getRangeMin(self, caster):
		"""
		virtual method.
		"""
		return self.rangeMin

	def getRangeMax(self, caster):
		"""
		virtual method.
		"""
		return self.rangeMax

	def getIntonateTime(self, caster):
		"""
		virtual method.
		"""
		return self.castingTime

	def getCastMaxRange(self, caster):
		return self.getRangeMax(caster) + self.__castMaxRange

	def getSpeed(self):
		return self.speed

	def isRotate(self):
		return self.__isRotate

	def getMaxReceiverCount(self):
		return self.maxReceiverCount

	def onTimerTick(self, tid, userArg, superScript):
		if not self.getQueued():
			#self.castingAbilityTimer = 0
			return

		if self.castingAbilityTimer >= self.castingAbilityDelay:
			self.onFinished()
			print('end the damn cast')

		self.castingAbilityTimer += ServerConstantsDefine.TICK_TYPE_ABILITY
		print(self.castingAbilityTimer)

	def queue(self, caster, abilityCastObject, delay):
		caster.queueAbility(self)
		self.setQueued(True)
		self.castingCaster = caster
		self.scObject = abilityCastObject
		self.castingAbilityDelay = delay
		self.castingAbilityTimer = 0

	def dequeue(self):
		self.castingCaster.dequeueAbility(self)
		self.setQueued(False)
		self.castingCaster = None
		self.scObject = None
		self.castingAbilityDelay = -1
		self.castingAbilityTimer = -1

	def canUse(self, caster, abilityCastObject):
		"""
		virtual method.
		Can use
		@param caster: Entity with Ability
		@param receiver: Entity with Ability
		"""
		if abilityCastObject.getObject().state == GlobalDefine.ENTITY_STATE_DEAD:
			return GlobalConst.GC_ABILITY_ENTITY_DEAD

		return GlobalConst.GC_OK

	def use(self, caster, abilityCastObject):
		"""
		virtual method.
		Use abilities
		@param caster: Entity with Ability
		@param receiver: Entity with Ability
		"""
		self.cast(caster, abilityCastObject)
		return GlobalConst.GC_OK

	def cast(self, caster, abilityCastObject):
		"""
		virtual method.
		Casting abilities
		"""
		delay = self.distToDelay(caster, abilityCastObject)
		INFO_MSG("%i cast ability[%i] delay=%s." % (caster.id, self.getID(), delay))
		if delay <= 0.1:
			self.onArrived(caster, abilityCastObject)
		else:
			INFO_MSG("%i add castAbility:%i. delay=%s." % (caster.id, self.getID(), delay))
			#caster.addCastAbility(self, abilityCastObject, delay)
			self.queue(caster, abilityCastObject, delay)

		self.onAbilityCastOver_(caster, abilityCastObject)

	def distToDelay(self, caster, abilityCastObject):
		"""
		"""
		return abilityCastObject.distToDelay(self.getSpeed(), caster.position)

	def onArrived(self, caster, abilityCastObject):
		"""
		virtual method.
		Reached the goal
		"""
		self.receive(caster, abilityCastObject.getObject())

	def onFinished(self):
		self.onArrived(self.castingCaster, self.scObject)
		self.dequeue()
		print('finished')

	def receive(self, caster, receiver):
		"""
		virtual method.
		Can do something for the subject
		"""
		pass

	def onAbilityCastOver_(self, caster, abilityCastObject):
		"""
		virtual method.
		Ability cast notification
		"""
		pass
