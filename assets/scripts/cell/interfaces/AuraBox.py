# -*- coding: utf-8 -*-
import Ouroboros
import auras
import GlobalConst
import GlobalDefine
import ServerConstantsDefine
from OURODebug import *

"""
Important Notes
Entity Objects contain both AuraBox & Aura
Use AuraBox to spawn an aura, and Aura to configure the Aura
Result = HarmfulAura -> ActiveAura
ScObject = AuraCastEntity
"""
class AuraBox:
	def __init__(self):
		self.auraData = []

	def addAura(self, aura):
		"""
		defined method.
		"""
		if not aura.getID() in self.auras:
			self.auras.append(aura.getID())
		if not aura in self.auraData:
			self.auraData.append(aura)


	def removeAura(self, aura):
		"""
		defined method.
		"""
		if aura.getID() in self.auras:
			self.auras.remove(aura.getID())
		if aura in self.auraData:
			self.auraData.remove(aura)
			del aura

	def removeAllAuras(self):
		for aura in self.auraData:
			self.removeAura(aura)
			if self.allClients:
				self.allClients.onAuraStatusUpdate(aura.getID(), aura.getIcon(), aura.getDescription(),
										   GlobalDefine.AURA_UPDATE_REMOVED, 0)

	def hasAura(self, auraID):
		"""
		"""
		return auraID in self.auras

	def onTimer(self, tid, userArg):
		#Run one timer for all auras this entity contains
		for aura in self.auraData:
			#If an aura is active and bound, run its timer
			if aura.getActiveState():
				aura.onTimer(tid, userArg)
			#Aura has expired, remove it
			else:
				self.removeAura(aura)
				if self.allClients:
					self.allClients.onAuraStatusUpdate(aura.getID(), aura.getIcon(), aura.getDescription(),
													   GlobalDefine.AURA_UPDATE_FINISHED, 0)

	def applyTargetAura(self, auraID, targetID, sourceID = -1):
		"""
		Exposed.
		Cast a aura on a target entity
		"""
		target = Ouroboros.entities.get(targetID)
		if target is None:
			DEBUG_MSG("Aura::applyTargetAura(%i): cannot attach aura auraID=%i, targetID=%i. Target not found!" % (
				self.id, auraID, targetID))
			return GlobalConst.GC_INVALID_TARGET
		return target.applyTargetAuraOnEntity(auraID, targetID, sourceID)


	def applyTargetAuraOnEntity(self, auraID, targetID, sourceID = -1):
		if auraID in self.auras:
			aura = self.getAura(auraID)
			if aura.getStackable():
				self.applyStackTargetAura(aura, targetID)
			self.refreshTargetAura(aura, targetID)

		aura = auras.getAuraByID(auraID)

		completed = False
		if aura is None:
			DEBUG_MSG("Aura::applyTargetAuraOnEntity(%i): Failed to find aura auraID=%i." % (
				self.id, auraID))
			return GlobalConst.GC_INVALID_ID

		# Solve by types
		if aura.getEffectTargetType() == GlobalDefine.AURA_TARGET_TYPE_MULTIPLE and aura.hasEffectTargetTypeRange():
			appliedAuras = []
			entities = self.entitiesInRange(aura.getEffectTargetTypeRange(self), None, self.position)
			for entity in entities:
				# TODO : come up with better way of knowing which entities to target
				if entity.className is 'Avatar' or entity.className is 'Enemy':
					newAura = entity.multipleApplyTargetAuraOnEntity(auraID, targetID, sourceID)
					appliedAuras.append(newAura)
					completed = True
					return GlobalConst.GC_OK
		elif aura.getEffectTargetType() == GlobalDefine.AURA_TARGET_TYPE_SELF:
			if targetID != self.id:
				return GlobalConst.GC_AURA_SELF_CAST_ONLY

		elif aura.getEffectTargetType() == GlobalDefine.AURA_TARGET_TYPE_SINGLE:
			newAura = self.attachTargetAura(auraID, targetID, sourceID)

			if newAura is not None:
				self.addAura(newAura)
				completed = True
				return GlobalConst.GC_OK

		return GlobalConst.GC_ERROR

	def multipleApplyTargetAuraOnEntity(self, auraID, targetID, sourceID = -1):
		if auraID in self.auras:
			aura = self.getAura(auraID)
			if aura.getStackable():
				self.applyStackTargetAura(aura, targetID)
			self.refreshTargetAura(aura, targetID)

		newAura = self.attachTargetAura(auraID, targetID, sourceID)

		if newAura is not None:
			self.addAura(newAura)
			return newAura

		return None

	def unApplyTargetAura(self, auraID, targetID, sourceID = -1):
		target = Ouroboros.entities.get(targetID)
		if target is None:
			DEBUG_MSG("Aura::unApplyTargetAura(%i): cannot attach aura auraID=%i, targetID=%i. Target not found!" % (
				self.id, auraID, targetID))

		return target.unApplyTargetAuraOnEntity(auraID, targetID, sourceID)

	def unApplyTargetAuraOnEntity(self, auraID, targetID, sourceID=-1):
		if auraID in self.auras:
			for aura in self.auraData:
				if aura.getID() == auraID:
					self.removeTargetAura(aura, targetID, sourceID)
					self.removeAura(aura)
					return True
		return False

	def getActiveAurasAsString(self):
		return ', '.join(map(str, self.auras))