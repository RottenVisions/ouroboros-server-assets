# -*- coding: utf-8 -*-
import Ouroboros
import auras
import GlobalConst
import ServerConstantsDefine

import aurabases.AuraCastObject as AuraCastObject

from OURODebug import *

class Aura:
	def __init__(self):
		pass

	def attachTargetAura(self, auraID, targetID, sourceID = -1):
		DEBUG_MSG("Aura::auraTarget(%i):auraID=%i, targetID=%i" % (self.id, auraID, targetID))

		aura = auras.getAuraByID(auraID)

		if aura is None:
			ERROR_MSG("Aura::auraTarget(%i):auraID=%i not found" % (self.id, auraID))
			return

		target = Ouroboros.entities.get(targetID)

		if target is None:
			ERROR_MSG("Aura::auraTarget(%i):targetID=%i not found" % (self.id, targetID))
			return

		auraCastObject = AuraCastObject.createAuraCastEntity(target)
		ret = aura.canAttach(self, auraCastObject)

		if ret != GlobalConst.GC_OK:
			DEBUG_MSG("Aura::auraTarget(%i): cannot attach aura auraID=%i, targetID=%i, code=%i" % (
			self.id, auraID, targetID, ret))
			return

		newAura = aura.attach(self, auraCastObject)

		if sourceID is not -1:
			newAura.setSource(sourceID)

		return newAura

	def refreshTargetAura(self, aura, targetID, sourceID = -1):
		target = Ouroboros.entities.get(targetID)

		if target is None:
			ERROR_MSG("Aura::auraRefresh(%i):targetID=%i not found" % (self.id, targetID))
			return

		ret = aura.canAttach(self, aura.scObject)

		if ret != GlobalConst.GC_OK:
			DEBUG_MSG("Aura::auraRefresh(%i): cannot attach aura auraID=%i, targetID=%i, code=%i" % (
			self.id, aura.getID(), targetID, ret))
			return

		aura.refresh(self, aura.scObject)

		if sourceID is not -1:
			aura.setSource(sourceID)

	def applyStackTargetAura(self, aura, targetID, sourceID = -1):
		if not aura.getStackable(): return

		target = Ouroboros.entities.get(targetID)

		if target is None:
			ERROR_MSG("Aura::auraRefresh(%i):targetID=%i not found" % (self.id, targetID))
			return

		ret = aura.canAttach(self, aura.scObject)

		if ret != GlobalConst.GC_OK:
			DEBUG_MSG("Aura::auraRefresh(%i): cannot attach aura auraID=%i, targetID=%i, code=%i" % (
			self.id, aura.getID(), targetID, ret))
			return

		aura.applyStack(self, aura.scObject)

		if sourceID is not -1:
			aura.setSource(sourceID)

	def getAura(self, auraID):
		return auras.getAuraByID(auraID)