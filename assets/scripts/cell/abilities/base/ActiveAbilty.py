# -*- coding: utf-8 -*-
import Ouroboros
import random
import time
import math
import OuroMath
import GlobalConst
import GlobalDefine
import ServerConstantsDefine
from OURODebug import *
from abilitybases.AbilityObject import AbilityObject
from abilitybases.AbilityCastObject import AbilityCastObject

class ActiveAbility(AbilityObject):
	def __init__(self):
		AbilityObject.__init__(self)
		self.castingTimer = -1

		self.travelingTimer = -1

		self.cooldownTimer = -1

		self.applyOrderTimer = -1

		self.interrupted = False
		self.scObject = None
		self.castingCaster = None
		self.receivingReceiver = None
		self.interruptingInterrupter = None
		self.superScript = None

	def loadFromDict(self, dictDatas):
		"""
		virtual method.
		Create this object from the dictionary
		"""
		AbilityObject.loadFromDict(self, dictDatas)

	def onTimerTick(self, tid, userArg, superScript):
		# Interrupt
		if self.interrupted:
			self.onInterrupt()
		# Casting
		if self.getCasting() and self.hasCastTime() and time.time() >= self.getCastingFinishedTime():
			# Prevent ability use when moving
			if not self.getCastableWhileMoving() and self.castingCaster.isMoving:
				self.onInterrupt()
			if self.castingTimer >= self.getCastTime():
				self.finishCasting()
		# Traveling
		if self.getTraveling() and self.hasTravelTime() and time.time() >= self.getTravelingFinishedTime():
			# Check position until close enough to target entity if we are pulling or charging
			if
			if self.travelingTimer >= self.getTravelTime():
				self.finishTraveling()
		# Cooldown
		if self.getOnCooldown() and time.time() >= self.getCooldownFinishedTime():
			if self.cooldownTimer >= self.getCooldown():
				self.finishCooldown()

		# Timed Ability Calculation
		if self.getEffectOneOrder() is GlobalDefine.EFFECT_APPLY_ORDER_TIME:
			if self.getEffectOneOrderTime() > 0:
				if time.time() >= self.applyOrderTimer:
					self.onAbilityOrderTimerFinished()

		# Timers

		# Casting
		if self.getCasting():
			self.castingTimer += ServerConstantsDefine.TICK_TYPE_ABILITY
		# Traveling
		if self.getTraveling():
			self.travelingTimer += ServerConstantsDefine.TICK_TYPE_ABILITY
		# Cooldown
		if self.getOnCooldown():
			self.cooldownTimer += ServerConstantsDefine.TICK_TYPE_ABILITY

		# Apply Order
		if self.getEffectOneOrder() is GlobalDefine.EFFECT_APPLY_ORDER_TIME:
			if self.getEffectOneOrderTime() > 0:
				self.applyOrderTimer += ServerConstantsDefine.TICK_TYPE_ABILITY

	def startCasting(self):
		"""
		This ability must be delayed by either cast time or distance it must travel
		:param caster: Who cast the ability
		:param abilityCastObject: Ability object
		:param delay: Total delay to wait
		:return:
		"""
		self.setCasting(True)
		self.setCastingFinishedTime(time.time() + self.getCastTime())
		self.castingTimer = 0
		self.castingCaster.addAbilityToCasting(self)
		self.initiateClientsCasting(self.castingCaster)
		self.superScript.onStartCasting(self.castingCaster, self.receivingReceiver)

	def finishCasting(self):
		"""
		Remove the ability from the queue, as it is now over
		:return:
		"""
		self.setCasting(False)
		self.setCastingFinishedTime(-1)
		self.castingTimer = -1
		self.castingCaster.removeAbilityFromCasting(self)
		# Switch to next phase possibilities
		# Recalculate things too before switching to next phase if applicable
		self.calculateTravelTime()
		self.superScript.onStopCasting(self.castingCaster, self.receivingReceiver)
		if self.hasTravelTime():
			self.startTraveling()
		elif self.hasCooldown() and not self.hasTravelTime():
			self.startCooldown()
		else:
			self.onFinished()

	def startTraveling(self):
		#Determine if we still need to travel at this stage
		self.calculateTravelTime()
		if not self.hasTravelTime():
			if self.hasCooldown():
				self.startCooldown()
				return

		self.setTraveling(True)
		self.setTravelingFinishedTime(time.time() + self.getTravelTime())
		self.travelingTimer = 0
		self.castingCaster.addAbilityToTravelers(self)
		self.initiateClientsTravel(self.castingCaster)
		self.superScript.onStartTraveling(self.castingCaster, self.receivingReceiver)

	def finishTraveling(self):
		# Make contact with target if it hasn't been done yet
		# This will already check for contact before executing so double hits will not occur
		self.onContact()
		self.setTraveling(False)
		self.setTravelTime(-1)
		self.setTravelingFinishedTime(-1)
		self.travelingTimer = -1
		self.castingCaster.removeAbilityFromTravelers(self)
		self.superScript.onStopTraveling(self.castingCaster, self.receivingReceiver)
		# Switch to next phase possibilities
		if self.hasCooldown():
			self.startCooldown()

	def startCooldown(self):
		self.setOnCooldown(True)
		self.setCooldownFinishedTime(time.time() + self.getCooldown())
		self.cooldownTimer = 0
		self.castingCaster.addAbilityToCooldowns(self)
		self.initiateClientCooldown(self.castingCaster, True)
		self.superScript.onStartCooldown(self.castingCaster, self.receivingReceiver)

	def finishCooldown(self):
		self.setOnCooldown(False)
		self.setCooldownFinishedTime(-1)
		self.cooldownTimer = -1
		self.castingCaster.removeAbilityFromCooldowns(self)
		self.initiateClientCooldown(self.castingCaster, False)
		self.superScript.onFinishedCooldown(self.castingCaster, self.receivingReceiver)
		self.onFinished()

	def interrupt(self, interrupter):
		self.interrupted = True
		self.interruptingInterrupter = interrupter

	def setup(self, caster, abilityCastObject):
		self.castingCaster = caster
		self.scObject = abilityCastObject

	def cleanup(self):
		self.receivingReceiver = None
		self.castingCaster = None
		self.scObject = None
		self.setTravelTime(-1)
		self.setContacted(False)
		self.interrupted = False
		# This must happen last as it will cause AbilityBox to remove this Ability as active
		self.setActive(False)

	def canUse(self, caster, target, abilityCastObject):
		"""
		virtual method.
		Can use
		@param caster: Entity with Ability
		@param receiver: Entity with Ability
		"""
		# Cast while moving
		if not self.getCastableWhileMoving():
			if caster.isMoving:
				return GlobalConst.GC_ABILITY_NOT_CASTABLE_WHILE_MOVING
		# Cost
		if self.hasCost():
			if self.getCostType() == GlobalDefine.ABILITY_COST_TYPE_HP:
				if caster.HP < self.getCost():
					return GlobalConst.GC_ABILITY_COST_INSUFFICIENT_HP
			if self.getCostType() == GlobalDefine.ABILITY_COST_TYPE_EG:
				if caster.EG < self.getCost():
					return GlobalConst.GC_ABILITY_COST_INSUFFICIENT_EG

		# TODO
		# Invalid entity target - figure out better way to handle this
		if abilityCastObject.getObject().state is None:
			return GlobalConst.GC_ABILITY_INVALID_TARGET_ENTITY
		# Dead
		if abilityCastObject.getObject().state == GlobalDefine.ENTITY_STATE_DEAD:
			return GlobalConst.GC_ABILITY_ENTITY_DEAD

		# Max Range
		if caster.position.distTo(target.position) > self.getRangeMax():
			return GlobalConst.GC_ABILITY_OUT_OF_MAX_RANGE

		# Min Range
		if caster.position.distTo(target.position) < self.getRangeMin():
			return GlobalConst.GC_ABILITY_OUT_OF_MIN_RANGE

		# Fov
		if self.hasFov():
			res = OuroMath.inFieldOfView(caster, target, self.getFov())
			if res is False:
				return GlobalConst.GC_ABILITY_NOT_IN_FOV

		self.receivingReceiver = target
		return GlobalConst.GC_OK

	def use(self, caster, abilityCastObject):
		"""
		virtual method.
		Use abilities
		@param caster: Entity with Ability
		@param receiver: Entity with Ability
		"""
		self.superScript = self
		self.cast(caster, abilityCastObject)
		return GlobalConst.GC_OK

	def cast(self, caster, abilityCastObject):
		"""
		virtual method.
		Casting abilities
		"""
		# Delay caused by travel time
		travelTimeDelay = self.distToDelay(caster, abilityCastObject)
		INFO_MSG("activeAbility::cast: %i casted ability=[%i] TravelDelay=%s CastTime=%d." % (caster.id, self.getID(), travelTimeDelay, self.getCastTime()))
		# Determine the stages of the ability to do
		# No travel time, cooldown or cast time
		# Instant Cast
		if travelTimeDelay <= GlobalConst.GC_ABILITY_ARRIVED_THRESHOLD and not self.hasCastTime() and not self.hasCooldown():
			self.setup(caster, abilityCastObject)
			self.onContact()
			self.onFinished()
		else:
			# Track this ability as it was not an instant cast
			caster.addAbilityToActives(self)
			self.setActive(True)
			INFO_MSG("activeAbility::cast: %i started casting ability: %i. TravelDelay=%s CastTime=%d." % (caster.id, self.getID(), travelTimeDelay, self.getCastTime()))
			# Setup
			self.setup(caster, abilityCastObject)
			self.setTravelTime(travelTimeDelay)
			# Travel and Cast Time
			if self.hasTravelTime() and self.hasCastTime():
				self.startCasting()
			# Travel Time and No Cast Time
			elif self.hasTravelTime() and not self.hasCastTime():
				self.startTraveling()
			# No Travel time and Cast Time
			elif not self.hasTravelTime() and self.hasCastTime():
				self.startCasting()
			else:
				ERROR_MSG("activeAbility::cast[BAD ERROR]: %i started casting ability: %i. TravelDelay=%s CastTime=%d." % (caster.id, self.getID(), travelTimeDelay, self.getCastTime()))

		self.onAbilityInitializeOver(caster, abilityCastObject)

	def onContact(self):
		if not self.getContacted():
			self.onArrived(self.castingCaster, self.scObject)
		self.setContacted(True)
		self.initiateClientsImpact(self.castingCaster)

	def onInterrupt(self):
		self.cancelCast()
		self.onFinished()
		self.superScript.onInterrupted(self.castingCaster, self.receivingReceiver, self.interruptingInterrupter)

	def onFinished(self):
		"""
		virtual method.
		Ability has completed
		"""
		self.castingCaster.removeAbilityFromActives(self)
		# Cleanup last, as it will erase the saved variables
		self.cleanup()

	def onAbilityOrderTimerFinished(self):
		self.superScript.onFinishedAbilityOrderTimer(self.castingCaster, self.receivingReceiver)

	def cancelCast(self):
		self.initiateClientCastCancel(self.castingCaster)

	def calculateTravelTime(self):
		return self.distToDelay(self.castingCaster, self.scObject)

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

	def receive(self, caster, receiver):
		"""
		virtual method.
		Can do something for the subject
		"""
		pass

	def onAbilityInitializeOver(self, caster, abilityCastObject):
		"""
		virtual method.
		Ability cast notification
		"""
		pass
