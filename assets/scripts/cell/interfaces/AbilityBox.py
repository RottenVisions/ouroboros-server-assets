# -*- coding: utf-8 -*-
import Ouroboros
import abilities
import GlobalConst
import ServerConstantsDefine
from OURODebug import *

class AbilityBox:
	def __init__(self):
		self.queuedAbilities = []
		self.queuedAbilitiesData = []
		self.castingAbility = None
		self.castingAbilityObject = None
		self.castingAbilityDelay = -1
		self.castingAbilityTimer = -1
		print('hahaha', self.id)

	def onTimer(self, tid, userArg):
		#Run one timer for all abilities this entity has queued
		for ability in self.queuedAbilitiesData:
			#If an ability is active and bound, run its timer
			if ability.getQueued():
				ability.onTimer(tid, userArg)
			#Ability has expired, remove it
			else:
				self.dequeueAbility(ability)

	def queueAbility(self, ability):
		if not ability.getID() in self.queuedAbilities:
			self.queuedAbilities.append(ability.getID())
		if not ability in self.queuedAbilitiesData:
			self.queuedAbilitiesData.append(ability)

	def dequeueAbility(self, ability):
		if ability.getID() in self.queuedAbilities:
			self.queuedAbilities.remove(ability.getID())
		if ability in self.queuedAbilitiesData:
			self.queuedAbilitiesData.remove(ability)
			del ability

	def hasAbility(self, abilityID):
		"""
		"""
		return abilityID in self.abilities

	#--------------------------------------------------------------------------------------------
	#                              defined
	#--------------------------------------------------------------------------------------------

	def requestPull(self, exposed):
		"""
		exposed
		"""
		if self.id != exposed:
			return

		DEBUG_MSG("AbilityBox::requestPull: %i abilities=%i" % (self.id, len(self.abilities)))
		for abilityID in self.abilities:
			self.client.onAddAbility(abilityID)

	# ABILITIES

	def addAbilityPoints(self, count):
		if (self.abilityPoints + count) >= GlobalConst.GC_ABILITY_AP_CAP:
			self.abilityPoints = GlobalConst.GC_ABILITY_AP_CAP
			return
		self.abilityPoints += count

	def removeAbilityPoints(self, count):
		if (self.abilityPoints - count) <= 0:
			self.abilityPoints = 0
			return
		self.abilityPoints -= count

	def addAbility(self, abilityID):
		"""
		defined method.
		"""
		if not abilityID in self.abilities:
			self.abilities.append(abilityID)
			self.reqAbility()
			return True
		return False

	def removeAbility(self, abilityID):
		"""
		defined method.
		"""
		if abilityID in self.abilities:
			self.abilities.remove(abilityID)
			return True
		return False

	def addCastAbility(self, ability, abilityCastObject, delay):
		self.castingAbility = ability
		self.castingAbilityObject = abilityCastObject
		self.castingAbilityDelay = delay
		self.castingAbilityTimer = 0
		print('added ability', ability, self.castingAbilityDelay)
		print('adding with', self.id)

	def onCastCastingAbility(self):
		self.castingAbility.onArrived(self, self.castingAbilityObject)
		self.castingAbility = None
		self.castingAbilityObject = None
		self.castingAbilityDelay = -1
		self.castingAbilityTimer = -1
		print('fire away!')

	def purchaseAbility(self, abilityID):
		cost = -1
		# Get the cost of the ability
		ability = abilities.getAuraByID(abilityID)
		if ability is not None:
			cost = ability.getAPCost()
		if -1 < cost <= self.abilityPoints:
			if abilityID not in self.abilities:
				self.abilities.append(abilityID)
				self.removeAbilityPoints(cost)
				return True
		return False

	def useTargetAbility(self, srcEntityID, abilityID, targetID):
		"""
		exposed.
		Cast a ability on a target entity
		"""
		if srcEntityID != self.id:
			return

		self.abilityTarget(abilityID, targetID)
		print('starting with', self.id)
