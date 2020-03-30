# -*- coding: utf-8 -*-
import Ouroboros
import GlobalDefine
import data_entities
from OURODebug import *
from interfaces.GameObject import GameObject
from interfaces.Combat import Combat
from interfaces.Ability import Ability
from interfaces.Teleport import Teleport
#from interfaces.Dialog import Dialog
from interfaces.State import State
from interfaces.Motion import Motion
from interfaces.AbilityBox import AbilityBox

class Avatar(Ouroboros.Entity,
				GameObject,
				State,
				Motion,
			 	AbilityBox,
				Combat,
			 	Ability,
				Teleport):
				#Dialog):
	'''
	Cell Implementation
	'''
	def __init__(self):
		Ouroboros.Entity.__init__(self)
		GameObject.__init__(self)
		State.__init__(self)
		Motion.__init__(self)
		AbilityBox.__init__(self)
		Ability.__init__(self)
		Teleport.__init__(self)
		#Dialog.__init__(self)
		self.resetProperties()
		Combat.__init__(self)

		# Set the fastest speed allowed per second, the speed will be pulled back
		self.topSpeed = self.moveSpeed + 15.0
		# self.topSpeedY = 10.0

		self.lastPositionSyncTime = 0.0

	def isPlayer(self):
		"""
		Virtual method.
		"""
		return True

	def dropNotify(self, itemId, UUid, itemCount):
		'''data = data_entities.data.get(40001003)

		if data is None:
			ERROR_MSG("SpawnPoint::spawn:%i not found." % 40001003)
			return

		params = {
			"uid": data["id"],
			"utype": data["etype"],
			"modelID": data["modelID"],
			"dialogID": data["dialogID"],
			"name": data["name"],
			"descr": data.get("descr", ''),
			"itemId": itemId,
			"itemCount": itemCount,
		}

		e = Ouroboros.createEntity("DroppedItem", self.spaceID, tuple(self.position), tuple(self.direction), params)

		self.client.dropItem_re(itemId, UUid)'''

	def resetProperties(self):
		self.attack_Max = self.strength * 2
		self.attack_Min = self.strength * 1
		self.defence = int(self.dexterity / 4)
		self.HP_Max = self.stamina * 10

	def equipNotify(self, itemId):
		self.equipWeapon = itemId

	def updatePositionSynced(self, entityId, position, yaw, syncTime):
		senderEntity = Ouroboros.entities[entityId]

		self.position = position
		self.yaw = yaw
		self.syncTime = syncTime

		# Call the sender's client method onFirstEntityHello
		senderEntity.client.onUpdatePositionSynced(entityId, position, yaw, syncTime)
		#self.allClients.client.

		DEBUG_MSG("Avatar::updatePositionSynced: ID: %i | Pos: (%d, %d, %d) | Dir: %d | SyncTime: %d" % (entityId, position.x, position.y, position.z, yaw, syncTime))

	def updateLastSyncTime(self, entityId, updateTime):
		self.lastPositionSyncTime = updateTime
		#DEBUG_MSG("Avatar::updateLastSyncTime: ID: %i | SyncTime: %d" % (entityId, updateTime))

	def updateEG(self, entityId, newValue):
		self.EG = newValue
		DEBUG_MSG("Avatar::updateEG: ID: %i | Value: %d" % (entityId, newValue))

	# --------------------------------------------------------------------------------------------
	#                              Callbacks
	# --------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		Ouroboros method.
		Engine callback timer trigger
		"""
		# DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		GameObject.onTimer(self, tid, userArg)
		Ability.onTimer(self, tid, userArg)

	def onGetWitness(self):
		"""
		Ouroboros method.
		Bind an observer(Client)
		"""
		DEBUG_MSG("Avatar::onGetWitness: %i." % self.id)

	def onLoseWitness(self):
		"""
		Ouroboros method.
		Unbind an observer(Client)
		"""
		DEBUG_MSG("Avatar::onLoseWitness: %i." % self.id)

	def onDestroy(self):
		"""
		Ouroboros method.
		Entity destruction
		"""
		DEBUG_MSG("Avatar::onDestroy: %i." % self.id)
		Teleport.onDestroy(self)
		Combat.onDestroy(self)

	def relive(self, exposed, type):
		"""
		defined.
		resurrection
		"""
		if exposed != self.id:
			return

		DEBUG_MSG("Avatar::relive: %i, type=%i." % (self.id, type))

		# Return to the city
		if type == 0:
			pass

		self.fullPower()
		self.changeState(GlobalDefine.ENTITY_STATE_FREE)

	def onAddEnemy(self, entityID):
		"""
		virtual method.
		Enemy enters the list
		"""
		if not self.isState(GlobalDefine.ENTITY_STATE_FIGHT):
			self.changeState(GlobalDefine.ENTITY_STATE_FIGHT)

	def onEnemyEmpty(self):
		"""
		virtual method.
		The enemy list is empty
		"""
		self.changeState(GlobalDefine.ENTITY_STATE_FREE)