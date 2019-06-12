# -*- coding: utf-8 -*-
import Ouroboros
from OURODebug import *
from abilitybases.AbilityObject import AbilityObject

class Aura(AbilityObject):
	def __init__(self):
		AbilityObject.__init__(self)

		self._loopTime = 0		# Cycle trigger time
		self._totalTime = 0		# duration

	def loadFromDict(self, dictDatas):
		"""
		virtual method.
		Create this object from the dictionary
		"""
		AbilityObject.loadFromDict(self, dictDatas)
		self._loopTime = dictDatas.get('looptime', 0)
		self._totalTime = dictDatas.get('totaltime', 0)

	def onLoopTrigger(self, context):
		"""
		virtual method.
		Cycle trigger
		@param context: buff/Debuff context
		"""
		pass

	def onAttach(self, context):
		"""
		virtual method.
		buff/When debuff is bound
		@param context: buff/Debuff context
		"""
		pass

	def onDetach(self, context):
		"""
		virtual method.
		buff/Debuff when unbinding
		@param context: buff/Debuff context
		"""
		pass
