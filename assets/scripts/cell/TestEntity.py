import Ouroboros
import ServerConstantsDefine

from interfaces.Ability import Ability
from interfaces.AbilityBox import AbilityBox
from interfaces.Aura import Aura
from interfaces.AuraBox import AuraBox
from OURODebug import *

class TestEntity(Ouroboros.Entity,
				 #Ability,
				 #AbilityBox,
				 Aura,
				 AuraBox):
	"""
	The cell part of the Scene
	A space on the cell represents an abstract space
	The scene is an entity representation of the abstract space for easy control
	"""
	def __init__(self):
		#AbilityBox.__init__(self)
		AuraBox.__init__(self)

		self.onEnable()
		pass

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		Ouroboros method.
		Engine callback timer trigger
		"""
		#DEBUG_MSG('TID: %i %s' % (tid, userArg))

		if ServerConstantsDefine.TIMER_TYPE_HEARTBEAT == userArg:
			self.onHeardTimer()

		#GameObject.onTimer(self, tid, userArg)
		if ServerConstantsDefine.TIMER_TYPE_AURA_TICK == userArg:
			#Aura.onTimer(tid, userArg)
			AuraBox.onTimer(self, tid, userArg)

	def onEnter(self, entityCall):
		"""
		Entering the Scene
		Called by the base part of Scene, the cell part is notified, and Entity enters this scenario.
		:param entityCall:
		:return:
		"""
		DEBUG_MSG('Scene[%i]::onEnter: entityID = %i.' % (self.id, entityCall.id))

	def onLeave(self, entityId):
		"""
		Leaving the Scene
		Called by the base part of Scene, the cell part is notified, and Entity leaves the scene.
		:param entityId:
		:return:
		"""
		DEBUG_MSG('Scene[%i]::onLeave: entityID = %i.' % (self.id, entityId))

	def onDestroy(self):
		"""
		Called when an entity is destroyed
		:return:
		"""
		pass

	#--------------------------------------------------------------------------------------------
	#                              Custom
	#--------------------------------------------------------------------------------------------


	def onEnable(self):
		DEBUG_MSG("enabled!")
		self.heartbeatTimer = self.addTimer(0, ServerConstantsDefine.TICK_TYPE_HEARTBEAT, ServerConstantsDefine.TIMER_TYPE_HEARTBEAT)
		self.buffTimer = self.addTimer(0, ServerConstantsDefine.TICK_TYPE_AURA, ServerConstantsDefine.TIMER_TYPE_AURA_TICK)

	def onDisable(self):
		DEBUG_MSG("disabled!")

	def onHeardTimer(self):
		"""
		Entity heartbeat
		"""
		#DEBUG_MSG('Heard timer')

	def ComeOn(self):
		pass
