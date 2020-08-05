# -*- coding: utf-8 -*-
import Ouroboros
import random
import GlobalDefine
from OURODebug import *
from abilities.base.ActiveAbilty import ActiveAbility

class AttackAbility(ActiveAbility):
	def __init__(self):
		ActiveAbility.__init__(self)

	def onTimer(self, tid, userArg):
		"""
		Ouroboros method.
		Engine callback timer trigger
		"""
		ActiveAbility.onTimerTick(self, tid, userArg, self)

	def canUse(self, caster, target, scObject):
		"""
		virtual method.
		Can use
		@param caster: Entity with Ability
		@param receiver: Entity
		"""
		return ActiveAbility.canUse(self, caster, target, scObject)

	def use(self, caster, scObject):
		"""
		virtual method.
		Use abilities
		@param caster: Entity with Ability
		@param receiver: Entity
		"""
		return ActiveAbility.use(self, caster, scObject)

	def activate(self, caster):
		"""
		virtual method.
		Take the cost of the ability
		"""
		if self.hasCost():
			if self.getCostType() == GlobalDefine.ABILITY_COST_TYPE_HP:
				caster.addHP(-self.getCost())
			if self.getCostType() == GlobalDefine.ABILITY_COST_TYPE_EG:
				caster.addEG(-self.getCost())

	def receive(self, caster, receiver):
		"""
		virtual method.
		Can do something for the subject
		"""
		attack = random.randint(caster.attack_Min, caster.attack_Max)
		defence = receiver.defence
		damage = 0
		if self.getID() == 1:
			damage = attack - defence + 10
		elif self.getID() == 2:
			damage = attack - defence + 30
		elif self.getID() == 4:
			damage = attack - defence + 30
		elif self.getID() == 5:
			damage = attack - defence + 40
		elif self.getID() == 6:
			damage = attack - defence + 30

		if damage < 0:
			damage = 0
		receiver.receiveDamage(receiver.id, caster.id, GlobalDefine.SOURCE_TYPE_ABILITY, self.getID(), self.getIcon(), self.getSchool(), damage)
		if self.getID() == 6: #Bloodsucking, add blood to yourself
			caster.receiveDamage(receiver.id, caster.id, GlobalDefine.SOURCE_TYPE_ABILITY, self.getID(), self.getIcon(), self.getSchool(), damage * 0.1)

	# Callbacks

	def onStartCasting(self, caster, receiver):
		DEBUG_MSG('got it!')
		if (self.hasEffectOne() and self.getEffectOneOrder() is GlobalDefine.EFFECT_APPLY_ORDER_START):
			self.processAbilityEvents(caster, receiver, GlobalDefine.EFFECT_APPLY_ORDER_START, GlobalDefine.ABILITY_CALCULATION_POSITION_SOURCE)

	def onStopCasting(self, caster, receiver):
		pass

	def onStartTraveling(self, caster, receiver):
		pass

	def onStopTraveling(self, caster, receiver):
		if (self.hasEffectOne() and self.getEffectOneOrder() is GlobalDefine.EFFECT_APPLY_ORDER_FINISH):
			self.processAbilityEvents(caster, receiver, GlobalDefine.EFFECT_APPLY_ORDER_FINISH, GlobalDefine.ABILITY_CALCULATION_POSITION_DESTINATION)

	def onStartCooldown(self, caster, receiver):
		pass

	def onFinishedCooldown(self, caster, receiver):
		pass

	def onFinishedAbilityOrderTimer(self, caster, receiver):
		if (self.hasEffectOne() and self.getEffectOneOrder() is GlobalDefine.EFFECT_APPLY_ORDER_TIME):
			self.processAbilityEvents(caster, receiver, GlobalDefine.EFFECT_APPLY_ORDER_TIME, GlobalDefine.ABILITY_CALCULATION_POSITION_DESTINATION)

	def processAbilityEvents(self, caster, receiver, order, abilityCalculationPosition):
		# Process all potential ability workings
		# Calculate the amount before
		amountCalc = self.getEffectOneAmount() * caster.getProperty(self.getEffectOneAmountCalculation())
		# Health
		if self.getEffectOneTarget() is GlobalDefine.ATTRIBUTE_HEALTH:
			# Increase
			if self.getEffectOneType() is GlobalDefine.ABILITY_TYPE_INCREASE:
				if self.getEffectOneTargetType() is GlobalDefine.ABILITY_TARGET_TYPE_SELF:
					if self.getEffectOneAmountCalculationPosition() is abilityCalculationPosition:
						caster.addHP(amountCalc)
				elif self.getEffectOneTargetType() is GlobalDefine.ABILITY_TARGET_TYPE_SINGLE:
					if self.getEffectOneAmountCalculationPosition() is abilityCalculationPosition:
						receiver.addHP(amountCalc)
			# Decrease
			elif self.getEffectOneType() is GlobalDefine.ABILITY_TYPE_DECREASE:
				if self.getEffectOneTargetType() is GlobalDefine.ABILITY_TARGET_TYPE_SELF:
					if self.getEffectOneAmountCalculationPosition() is abilityCalculationPosition:
						caster.addHP(-amountCalc)
				elif self.getEffectOneTargetType() is GlobalDefine.ABILITY_TARGET_TYPE_SINGLE:
					if self.getEffectOneAmountCalculationPosition() is abilityCalculationPosition:
						receiver.addHP(-amountCalc)
		# Energy
		elif self.getEffectOneTarget() is GlobalDefine.ATTRIBUTE_ENERGY:
			# Increase
			if self.getEffectOneType() is GlobalDefine.ABILITY_TYPE_INCREASE:
				if self.getEffectOneTargetType() is GlobalDefine.ABILITY_TARGET_TYPE_SELF:
					if self.getEffectOneAmountCalculationPosition() is abilityCalculationPosition:
						caster.addEG(amountCalc)
				elif self.getEffectOneTargetType() is GlobalDefine.ABILITY_TARGET_TYPE_SINGLE:
					if self.getEffectOneAmountCalculationPosition() is abilityCalculationPosition:
						receiver.addEG(amountCalc)
			# Decrease
			elif self.getEffectOneType() is GlobalDefine.ABILITY_TYPE_DECREASE:
				if self.getEffectOneTargetType() is GlobalDefine.ABILITY_TARGET_TYPE_SELF:
					if self.getEffectOneAmountCalculationPosition() is abilityCalculationPosition:
						caster.addEG(-amountCalc)
				elif self.getEffectOneTargetType() is GlobalDefine.ABILITY_TARGET_TYPE_SINGLE:
					if self.getEffectOneAmountCalculationPosition() is abilityCalculationPosition:
						receiver.addEG(-amountCalc)
		# Interrupt
		if self.getEffectOneType() is GlobalDefine.ABILITY_TYPE_INTERRUPT:
			if self.getEffectOneTargetType() is GlobalDefine.ABILITY_TARGET_TYPE_SELF:
				if self.getEffectOneAmountCalculationPosition() is abilityCalculationPosition:
					caster.interrupt(caster.id)
			elif self.getEffectOneTargetType() is GlobalDefine.ABILITY_TARGET_TYPE_SINGLE:
				if self.getEffectOneAmountCalculationPosition() is abilityCalculationPosition:
					receiver.interrupt(caster.id)
		# Apply Attribute 1
		if self.hasEffectOneAttributeOne():
			receiver.addAttribute(caster.id, self.getEffectOneAttributeOne())
		# Apply Attribute 2
		if self.hasEffectOneAttributeTwo():
			receiver.addAttribute(caster.id, self.getEffectOneAttributeTwo())
		# Apply Attribute 3
		if self.hasEffectOneAttributeThree():
			receiver.addAttribute(caster.id, self.getEffectOneAttributeThree())
		# Apply Aura 1
		if self.hasEffectOneAppliesAuraID():
			caster.applyTargetAura(self.getEffectOneAppliesAuraID, receiver.id, caster.id)

		#TODO
		# Proc Chance

	def onInterrupted(self, caster, receiver, interrupter):
		pass

	# Force floats for all values that must adhere to avoid any errors
	def initiateClientsTravel(self, caster):
		if caster.allClients:
			caster.allClients.onAbilityStateChange(GlobalDefine.ENTITY_ABILITY_STATE_LAUNCH_PROJECTILE, self.getID(), self.getTargetID(), self.getDisplayID(), float(self.getSpeed()))

	def initiateClientCooldown(self, caster, value):
		if caster.client:
			if value:
				caster.client.onAbilityStateChange(GlobalDefine.ENTITY_ABILITY_STATE_COOLDOWN_START, self.getID(), self.getTargetID(), self.getDisplayID(), float(self.getCooldown()))
			else:
				caster.client.onAbilityStateChange(GlobalDefine.ENTITY_ABILITY_STATE_COOLDOWN_END, self.getID(), self.getTargetID(), self.getDisplayID(), float(-1))

	def initiateClientCastCancel(self, caster):
		if caster.allClients:
			caster.allClients.onAbilityStateChange(GlobalDefine.ENTITY_ABILITY_STATE_CAST_CANCELED, self.getID(), self.getTargetID(), self.getDisplayID(), float(-1))

	def initiateClientsCasting(self, caster):
		if caster.allClients:
			caster.allClients.onAbilityStateChange(GlobalDefine.ENTITY_ABILITY_STATE_CASTING, self.getID(), self.getTargetID(), self.getDisplayID(), float(self.getCastTime()))

	def initiateClientsImpact(self, caster):
		if caster.allClients:
			caster.allClients.onAbilityStateChange(GlobalDefine.ENTITY_ABILITY_STATE_IMPACT, self.getID(), self.getTargetID(), self.getDisplayID(), float(-1))