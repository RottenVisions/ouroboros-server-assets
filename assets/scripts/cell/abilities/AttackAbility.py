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
			caster.receiveDamage(receiver.id, caster.id, GlobalDefine.SOURCE_TYPE_ABILITY, self.getID(), self.getIcon(), self.getSchool(), -int(damage*0.1))

	def initiateClientsTravel(self, caster):
		if caster.allClients:
			caster.allClients.onAbilityStateChange(GlobalDefine.ENTITY_ABILITY_STATE_LAUNCH_PROJECTILE)

	def initiateClientCooldown(self, caster, value):
		if caster.client:
			if value:
				caster.client.onAbilityStateChange(GlobalDefine.ENTITY_ABILITY_STATE_COOLDOWN_START)
			else:
				caster.client.onAbilityStateChange(GlobalDefine.ENTITY_ABILITY_STATE_COOLDOWN_END)

	def initiateClientsCasting(self, caster):
		if caster.allClients:
			caster.allClients.onAbilityStateChange(GlobalDefine.ENTITY_ABILITY_STATE_CASTING)

	def initiateClientsImpact(self, caster):
		if caster.allClients:
			caster.allClients.onAbilityStateChange(GlobalDefine.ENTITY_ABILITY_STATE_IMPACT)