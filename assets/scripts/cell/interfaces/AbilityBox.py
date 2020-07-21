# -*- coding: utf-8 -*-
import Ouroboros
import abilities
import GlobalConst
import ServerConstantsDefine
from OURODebug import *

class AbilityBox:
	def __init__(self):
		# Abilities by their actual object
		self.activeAbilitiesData = []
		# Stage 1: Casting
		self.castingAbilitiesData = []
		# Stage 2: Traveling
		self.travelingAbilitiesData = []
		# Stage 3: On Cooldown
		self.abilitiesOnCooldownData = []

	def onTimer(self, tid, userArg):
		#Run one timer for all abilities this entity has startcasting
		for ability in self.activeAbilitiesData:
			#If an ability is active and bound, run its timer
			if ability.getActive():
				ability.onTimer(tid, userArg)
			#Ability has expired, remove it
			else:
				self.removeAbilityFromActives(ability)

	def addAbilityToActives(self, ability):
		if not ability in self.activeAbilitiesData:
			self.activeAbilitiesData.append(ability)

	def removeAbilityFromActives(self, ability):
		if ability in self.activeAbilitiesData:
			self.activeAbilitiesData.remove(ability)
			del ability

	def addAbilityToCasting(self, ability):
		if not ability in self.castingAbilitiesData:
			self.castingAbilitiesData.append(ability)

	def removeAbilityFromCasting(self, ability):
		if ability in self.castingAbilitiesData:
			self.castingAbilitiesData.remove(ability)
			del ability

	def addAbilityToTravelers(self, ability):
		if not ability in self.travelingAbilitiesData:
			self.travelingAbilitiesData.append(ability)

	def removeAbilityFromTravelers(self, ability):
		if ability in self.travelingAbilitiesData:
			self.travelingAbilitiesData.remove(ability)

	def addAbilityToCooldowns(self, ability):
		if not ability in self.abilitiesOnCooldownData:
			self.abilitiesOnCooldownData.append(ability)

	def removeAbilityFromCooldowns(self, ability):
		if ability in self.abilitiesOnCooldownData:
			self.abilitiesOnCooldownData.remove(ability)

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

	def purchaseAbility(self, abilityID):
		cost = -1
		# Get the cost of the ability
		ability = abilities.getAbilityByID(abilityID)
		if ability is not None:
			cost = ability.getAPCost()
		if -1 < cost <= self.abilityPoints:
			if abilityID not in self.abilities:
				self.abilities.append(abilityID)
				self.removeAbilityPoints(cost)
				return True
		return False

	def useTargetAbility(self, srcEntityID, abilityID, targetID):
		ret = self.executeTargetAbility(srcEntityID, abilityID, targetID)
		if ret != GlobalConst.GC_OK:
			if self.client:
				self.client.onErrorReceived(ret)

	def executeTargetAbility(self, srcEntityID, abilityID, targetID):
		"""
		exposed.
		Cast a ability on a target entity
		"""
		# Disallow non source entity to cast abilities through other entities
		if srcEntityID != self.id:
			return GlobalConst.GC_ABILITY_CAST_NON_SOURCE_ENTITY

		for ability in self.activeAbilitiesData:
			if ability.getCasting():
				return GlobalConst.GC_ALREADY_CASTING_ABILITY

		ability = abilities.getAbility(abilityID)
		if ability is None:
			ERROR_MSG("Ability::abilityTarget(%i):abilityID=%i not found" % (self.id, abilityID))
			return GlobalConst.GC_INVALID_ID

		# Cooldown
		for ability in self.activeAbilitiesData:
			if abilityID == ability.getID():
				if ability.getOnCooldown():
					return GlobalConst.GC_ABILITY_ON_COOLDOWN
				if ability.getCasting():
					return GlobalConst.GC_ABILITY_IS_CASTING

		# Self Casting
		if not ability.getSelfCasting():
			if srcEntityID == targetID:
				return GlobalConst.GC_ABILITY_SELF_CAST_FORBIDDEN


		return self.abilityTarget(abilityID, targetID)
