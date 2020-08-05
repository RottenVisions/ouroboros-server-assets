# -*- coding: utf-8 -*-
import Ouroboros
import GlobalDefine
import GlobalConst
import random
from OURODebug import *
from auras.base.ActiveAura import ActiveAura

class HarmfulAura(ActiveAura):
	def __init__(self):
		ActiveAura.__init__(self)
		
	def onTimer(self, tid, userArg):
		"""
		Ouroboros method.
		Engine callback timer trigger
		"""
		ActiveAura.onTimerTick(self, tid, userArg, self)

	def canAttach(self, caster, scObject):
		"""
		virtual method.
		Can use
		@param caster: Entity that gives Aura
		@param receiver: Entity
		"""
		# GlobalConst.GC_OK
		return ActiveAura.canAttachTo(self, caster, scObject)

	def attach(self, attacher, scObject):
		"""
		virtual method.
		Attach an aura
		@param attacher: Entity that attaches Aura
		@param receiver: Entity
		"""
		target = self.getTarget()

		if self.getEffectApplyAttribute() is not GlobalDefine.TYPE_NONE:
			if self.getTarget().activeAttributes is not None:
				target.addAttribute(attacher.id, self.getEffectApplyAttribute())
		if self.getEffectTarget() is not GlobalDefine.TYPE_NONE:
			if self.getEffectCalculation() is not GlobalDefine.TYPE_NONE:
				if self.getEffectCalculation() is not GlobalDefine.ATTRIBUTE_HEALTH or \
						self.getEffectCalculation() is not GlobalDefine.ATTRIBUTE_ENERGY:
							modified = self.getAmount() * target.getProperty(self.getEffectCalculation())
							target.setProperty(self.getEffectCalculation(), modified)
		self.onAttached(attacher, scObject)
		return ActiveAura.attachTo(self, attacher, scObject)

	def canDetach(self, remover, scObject, selfAsk = False):
		"""
		virtual method.
		Can use
		@param remover: Entity that wants to remove Aura
		@param receiver: Entity
		"""
		if not selfAsk:
			return ActiveAura.canDetachFrom(self, remover, scObject)
		return GlobalConst.GC_OK

	def detach(self, scObject, selfDetach = False):
		target = self.getTarget()
		if target is not None:
			if scObject.getEffectApplyAttribute(self) is not GlobalDefine.TYPE_NONE:
				if target.activeAttributes is not None:
					target.removeAttribute(self.getSource(), scObject.getEffectApplyAttribute(self))
		self.onDetached(scObject)

		if not selfDetach:
			return ActiveAura.detachFrom(self, scObject)
		return GlobalConst.GC_OK


	def refresh(self, caster, scObject):
		"""
		virtual method.
		Attach an aura
		@param caster: Entity that casts Aura
		@param receiver: Entity
		"""
		self.onAttached(caster, scObject)
		return ActiveAura.refreshIt(self, caster, scObject, self)

	def onAuraCycleTick(self, tid, userArg, auraCastObject):
		entToApplyTo = auraCastObject.getTarget(self)
		entToApplyTo.receiveDamage(entToApplyTo.id, auraCastObject.getSource(self).id, GlobalDefine.SOURCE_TYPE_AURA, auraCastObject.getID(self), auraCastObject.getIcon(self), auraCastObject.getSchool(self), auraCastObject.getAmount(self))

	def onAttached(self, attacher, auraCastObject):
		self.scObject = auraCastObject

	def onDetached(self, scObject):
		self.scObject = None
		self.setStacks(0)
	
	def onRefreshed(self):
		pass

	def applyStack(self, caster, scObject):
		if ActiveAura.getStacks(self) >= ActiveAura.getMaxStacks(self):
			ActiveAura.setStacks(self, ActiveAura.getMaxStacks(self))
			return
		ActiveAura.addStack(self)
		#print('Stacks: %i of %i' % (ActiveAura.getStacks(self), ActiveAura.getMaxStacks(self)))