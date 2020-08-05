# -*- coding: utf-8 -*-
import Ouroboros
import GlobalDefine
import GlobalConst
import random
import time
from OURODebug import *
from interfaces.CombatProperties import CombatProperties
import data_avatar_initial

class Combat(CombatProperties):
	"""
	Some features about combat
	"""
	def __init__(self):
		CombatProperties.__init__(self)
		self.lastAutoAttack = -1
		self.autoAttacking = False

	def onTimer(self, tid, userArg):
		self.processAutoAttack()

	def processAutoAttack(self):
		if self.mainTarget != -1:
			if self.mainTargetEntity is not None:
				if self.withinDistanceToEntity(self.mainTargetEntity, GlobalConst.GC_AUTO_ATTACK_MELEE_DISTANCE):
					if self.state is GlobalDefine.ENTITY_STATE_FIGHT:
						if time.time() >= GlobalConst.GC_AUTO_ATTACK_INTERVAL + self.lastAutoAttack:
							self.onAutoAttack()
							self.lastAutoAttack = time.time()

	def onAutoAttack(self):
		DEBUG_MSG('attack')
		pass

	def canUpgrade(self):
		"""
		virtual method.
		"""
		return True

	def upgrade(self):
		"""
		for real
		"""
		if self.canUpgrade():
			self.addLevel(1)

	def addLevel(self, lv):
		"""
		for real
		"""
		self.level += lv
		self.onLevelChanged(lv)

	def setTarget(self, targetID):
		# Do not target ourselves
		if targetID == self.id:
			targetID = 0

		mainTargetEntity = Ouroboros.entities.get(targetID)

		if mainTargetEntity:
			self.mainTarget = targetID
			self.mainTargetEntity = mainTargetEntity
			return True
		return False

	def startAutoAttack(self, targetID = -1):
		if targetID != -1:
			success = self.setTarget(targetID)
			if not success:
				return False
		if self.mainTarget is -1:
			DEBUG_MSG("%s::startAutoAttack: No valid target for id=%i, target=%i." % (self.getScriptName(), self.id, self.mainTarget))
			return False
		if self.mainTargetEntity is None:
			DEBUG_MSG("%s::startAutoAttack: No valid target for id=%i, target=%i." % (
			self.getScriptName(), self.id, self.mainTarget))
			return False
		if not self.withinDistanceToEntity(self.mainTargetEntity, GlobalConst.GC_AUTO_ATTACK_MELEE_DISTANCE):
			return False
		self.changeState(GlobalDefine.ENTITY_STATE_FIGHT)
		self.lastAutoAttack = 0
		self.autoAttacking = True
		return True

	def stopAutoAttack(self):
		if self.mainTarget == -1:
			DEBUG_MSG("%s::stopAutoAttack: No valid target was available id=%i, target=%i." % (self.getScriptName(), self.id, self.mainTarget))
			return False
		if self.mainTargetEntity is None:
			DEBUG_MSG("%s::stopAutoAttack: No valid target for id=%i, target=%i." % (
			self.getScriptName(), self.id, self.mainTarget))
			return False
		self.state = GlobalDefine.ENTITY_STATE_FREE
		self.lastAutoAttack = -1
		self.autoAttacking = False
		return True

	def stun(self, inflictor):
		self.changeState(GlobalDefine.ENTITY_STATE_STUNNED)

	def isDead(self):
		"""
		"""
		return self.state == GlobalDefine.ENTITY_STATE_DEAD

	def die(self, killerID):
		"""
		"""
		if self.isDestroyed or self.isDead():
			return

		if killerID == self.id:
			killerID = 0

		INFO_MSG("%s::die: %i i die. killerID:%i." % (self.getScriptName(), self.id, killerID))
		killer = Ouroboros.entities.get(killerID)
		if killer:
			killer.onKiller(self.id)

		self.onBeforeDie(killerID)
		self.onDie(killerID)
		self.changeState(GlobalDefine.ENTITY_STATE_DEAD)
		self.onAfterDie(killerID)
		if self.isEnemy():
			if random.randint(0, 10) == 1: #The probability of falling is 10
				self.dropNotify(random.randrange(1, 11),1)
			killer.exp += random.randrange(1, 10)
			if killer.exp > killer.level*5+20:
				killer.upgrade()

	def canDie(self, attackerID, abilityID, damageType, damage):
		"""
		virtual method.
		Can you die?
		"""
		return True

	def receiveDamage(self, targetID, sourceID, origin, typeID, icon, school, amount):
		"""
		defined.
		"""
		if self.isDestroyed or self.isDead():
			return

		self.addEnemy(sourceID, amount)

		DEBUG_MSG("%s::receiveDamage: %i sourceID=%i, origin=%i, typeID=%i, icon=%s, school=%s, amount=%i" % \
			(self.getScriptName(), self.id, sourceID, origin, typeID, icon, school, amount))

		if self.HP <= amount:
			if self.canDie(sourceID, typeID, school, amount):
				self.die(sourceID)
		else:
			self.setHP(self.HP - amount)

		if self.allClients:
			self.allClients.receiveDamage(targetID, sourceID, origin, typeID, icon, school, amount)

	def receiveHealing(self, targetID, sourceID, origin, typeID, icon, school, amount):
		"""
		defined.
		"""
		if self.isDestroyed or self.isDead():
			return

		DEBUG_MSG("%s::receiveHealing: %i sourceID=%i, origin=%i, typeID=%i, icon=%s, school=%s, amount=%i" % \
				  (self.getScriptName(), self.id, sourceID, origin, typeID, icon, school, amount))

		self.addHP(amount)

		if self.allClients:
			self.allClients.receiveHealing(targetID, sourceID, origin, typeID, icon, school, amount)

	def addEnemy(self, entityID, enmity):
		"""
		defined.
		Add enemy
		"""
		if entityID in self.enemyLog:
			return

		DEBUG_MSG("%s::addEnemy: %i entity=%i, enmity=%i" % \
						(self.getScriptName(), self.id, entityID, enmity))

		self.enemyLog.append(entityID)
		self.onAddEnemy(entityID)

	def removeEnemy(self, entityID):
		"""
		defined.
		Delete enemy
		"""
		DEBUG_MSG("%s::removeEnemy: %i entity=%i" % \
						(self.getScriptName(), self.id, entityID))

		self.enemyLog.remove(entityID)
		self.onRemoveEnemy(entityID)

		if len(self.enemyLog) == 0:
			self.onEnemyEmpty()

	def checkInTerritory(self):
		"""
		virtual method.
		Check if you are in an active territory
		"""
		return True

	def checkEnemyDist(self, entity):
		"""
		virtual method.
		Check enemy distance
		"""
		dist = entity.position.distTo(self.position)
		if dist > 30.0:
			INFO_MSG("%s::checkEnemyDist: %i id=%i, distance=%f." % (self.getScriptName(), self.id, entity.id, dist))
			return False

		return True

	def withinDistanceToEntity(self, entity, distance):
		"""
		virtual method.
		Check enemy distance
		"""
		dist = entity.position.distTo(self.position)
		if dist > distance:
			INFO_MSG("%s::withinDistanceToEntity: %i id=%i, distance=%f." % (self.getScriptName(), self.id, entity.id, dist))
			return False

		return True

	def checkEnemys(self):
		"""
		Check the enemy list
		"""
		for idx in range(len(self.enemyLog) - 1, -1, -1):
			entity = Ouroboros.entities.get(self.enemyLog[idx])
			if entity is None or entity.isDestroyed or entity.isDead() or \
				not self.checkInTerritory() or not self.checkEnemyDist(entity):
				self.removeEnemy(self.enemyLog[idx])

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onLevelChanged(self, addlv):
		"""
		virtual method.
		"""
		self.experience = 0
		if self.roleTypeCell == 1:#warrior
			self.strength = data_avatar_initial.datas[self.roleTypeCell]["strength"] + 1*self.level
			self.endurance = data_avatar_initial.datas[self.roleTypeCell]["endurance"] + 2*self.level
			self.will = data_avatar_initial.datas[self.roleTypeCell]["will"] + 4*self.level

		else:				#Mage
			self.strength = data_avatar_initial.datas[self.roleTypeCell]["strength"] + 2*self.level
			self.endurance = data_avatar_initial.datas[self.roleTypeCell]["endurance"] + 1*self.level
			self.will = data_avatar_initial.datas[self.roleTypeCell]["will"] + 1*self.level
		self.base.updateProperties()
		pass

	def onDie(self, killerID):
		"""
		virtual method.
		"""
		self.setHP(0)
		self.setEG(0)
		if self.isPlayer() and self.level > 1:
			self.level -= 1
			self.onLevelChanged(self.level)

	def onBeforeDie(self, killerID):
		"""
		virtual method.
		"""
		pass

	def onAfterDie(self, killerID):
		"""
		virtual method.
		"""
		pass

	def onKiller(self, entityID):
		"""
		defined.
		I killed the entity
		"""
		pass

	def onDestroy(self):
		"""
		Entity destruction
		"""
		pass

	def onAddEnemy(self, entityID):
		"""
		virtual method.
		Enemy enters the list
		"""
		pass

	def onRemoveEnemy(self, entityID):
		"""
		virtual method.
		Delete enemy
		"""
		pass

	def onEnemyEmpty(self):
		"""
		virtual method.
		The enemy list is empty
		"""
		pass
