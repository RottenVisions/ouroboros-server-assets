# -*- coding: utf-8 -*-
import Ouroboros
import random
from OURODebug import *
from auras.base.ActiveAura import ActiveAura

class HelpfulAura(ActiveAura):
	def __init__(self):
		ActiveAura.__init__(self)

	def canAttach(self, caster, scObject):
		"""
		virtual method.
		Can use
		@param caster: Entity that gives Aura
		@param receiver: Entity
		"""
		return ActiveAura.canAttach(self, caster, scObject)

	def attach(self, caster, scObject):
		"""
		virtual method.
		Attach an aura
		@param caster: Entity that casts Aura
		@param receiver: Entity
		"""
		return ActiveAura.attach(self, caster, scObject)

	def receive(self, caster, receiver):
		"""
		virtual method.
		Can do something for the subject
		"""
