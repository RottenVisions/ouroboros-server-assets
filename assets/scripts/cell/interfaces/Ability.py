# -*- coding: utf-8 -*-
import Ouroboros
import abilities
import GlobalConst
import ServerConstantsDefine
from OURODebug import *
import abilitybases.AbilityCastObject as AbilityCastObject

class Ability:
	def __init__(self):
		pass

	def casting(self, ability, abilityCastObject):
		"""
		casting abilities
		"""
		pass

	def abilityTarget(self, abilityID, targetID):
		"""
		defined.
		Cast a ability on a target entity
		"""
		DEBUG_MSG("Ability::abilityTarget(%i): AbilityID=%i, targetID=%i" % (self.id, abilityID, targetID))

		ability = abilities.getAbility(abilityID)
		if ability is None:
			ERROR_MSG("Ability::abilityTarget(%i): AbilityID=%i not found" % (self.id, abilityID))
			return GlobalConst.GC_INVALID_ID

		target = Ouroboros.entities.get(targetID)

		if target is None:
			ERROR_MSG("Ability::abilityTarget(%i): TargetID=%i not found" % (self.id, targetID))
			return GlobalConst.GC_INVALID_TARGET

		ability.setTargetID(targetID)

		abilityCastObject = AbilityCastObject.createAbilityCastEntity(target)

		ret = ability.canUse(self, target, abilityCastObject)

		if ret != GlobalConst.GC_OK:
			DEBUG_MSG("Ability::abilityTarget(%i): Cannot cast ability abilityID=%i, targetID=%i, code=%i" % (self.id, abilityID, targetID, ret))
			return ret
		else:
			ability.activate(self)

		# Send to player to begin casting
		ability.use(self, abilityCastObject)
		return GlobalConst.GC_OK

	def abilityPosition(self, position):
		pass

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		Ouroboros method.
		Engine callback timer trigger
		"""
		pass

