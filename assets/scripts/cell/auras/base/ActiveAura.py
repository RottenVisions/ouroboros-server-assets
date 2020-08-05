# -*- coding: utf-8 -*-
import Ouroboros
import GlobalConst
import ServerConstantsDefine

from OURODebug import *

from aurabases.AuraObject import AuraObject

class ActiveAura(AuraObject):
	def __init__(self):
		AuraObject.__init__(self)
		self.auraTimer = -1
		self.tickCount = -1
		self.scObject = None

	def loadFromDict(self, dictDatas):
		"""
		virtual method.
		Create this object from the dictionary
		Runs when all Auras are added to the from their files on init
		"""
		AuraObject.loadFromDict(self, dictDatas)
		#self._period = dictDatas.get('period', 0)
		#self._duration = dictDatas.get('duration', 0)

	def onTimerTick(self, tid, userArg, superScript):
		if not AuraObject.getActiveState(self) or self.auraTimer <= 0:
			self.auraTimer = 0
			return

		self.auraTimer -= ServerConstantsDefine.TICK_TYPE_AURA

		if self.auraTimer % AuraObject.getPeriod(self) == 0:
			self.tickCount += 1
			self.onAuraTick(tid, userArg, superScript)
		if self.auraTimer <= 0:
			self.detachFrom(superScript)

	def onAttachedTo(self, attacher, auraCastObject):
		"""
		virtual method.
		When an aura is bound
		"""
		if self.auraTimer is not -1:
			return False

		self.auraTimer = AuraObject.getDuration(self)
		self.tickCount = 0

		AuraObject.setActiveState(self, True)
		ActiveAura.setSource(self, attacher)

	def onDetachedFrom(self, context):
		"""
		virtual method.
		When an aura is unbound
		"""
		AuraObject.setActiveState(self, False)
		ActiveAura.setSource(self, None)

		self.auraTimer = -1
		self.tickCount = -1

	def onAuraTick(self, tid, userArg, superScript):
		"""
		virtual method.
		Cycle trigger
		"""
		superScript.onAuraCycleTick(tid, userArg, ActiveAura)
	
	def canAttachTo(self, attacher, auraCastObject):
		#Run any checks here then, run the super
		return GlobalConst.GC_OK

	def canDetachFrom(self, detacher, auraCastObject):
		# Run any checks here then, run the super
		return GlobalConst.GC_OK
	
	def attachTo(self, attacher, auraCastObject):
		self.onAttachedTo(attacher, auraCastObject)
		return self # Note this return self here is re-used when attaching to a de-tached aura. If this becomes a problem use deep copy when creating an aura (like with items)

	def detachFrom(self, superScript):
		# Run checks both here and super script to see if we can detach successfully
		# Super

		ret = superScript.canDetach(self, AuraObject, True)
		if ret != GlobalConst.GC_OK:
			return GlobalConst.GC_ERROR
		# Self
		ret = self.canDetachFrom(self, AuraObject)
		if ret != GlobalConst.GC_OK:
			return GlobalConst.GC_ERROR
		# We can detach!
		superScript.detach(AuraObject, True)
		self.onDetachedFrom(AuraObject)
	
	def refreshIt(self, attacher, auraCastObject, superScript):
		if self.auraTimer > AuraObject.getDuration(self) and \
				self.auraTimer > 0:
			return False

		self.auraTimer = AuraObject.getDuration(self)
		self.tickCount = 0
		AuraObject.setActiveState(self, True)
		ActiveAura.setSource(self, attacher)
		superScript.onRefreshed()
