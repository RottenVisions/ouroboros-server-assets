# -*- coding: utf-8 -*-
import Ouroboros
import GlobalDefine
from OURODebug import *


class CombatProperties:
	"""
	All about combat attributes
	"""

	def __init__(self):
		# self.HP_Max = 100
		# self.EG_Max = 100

		# Non-death status needs to be filled
		if not self.isState(GlobalDefine.ENTITY_STATE_DEAD) and self.HP == 0 and self.EG == 0:
			self.fullPower()

	def fullPower(self):
		"""
		"""
		self.setHP(self.HP_Max)
		self.setEG(self.EG_Max)

	def addHP(self, val):
		"""
		defined.
		"""
		v = self.HP + val
		if v < 0:
			v = 0
		if v > self.HP_Max:
			v = self.HP_Max

		if self.HP == v:
			return

		self.HP = v

	def addEG(self, val):
		"""
		defined.
		"""
		v = self.EG + val
		if v < 0:
			v = 0
		if v > self.EG_Max:
			v = self.EG_Max

		if self.EG == v:
			return

		self.EG = v

	def addDefence(self, val):
		v = self.defence + val
		if v < 0:
			v = 0

		if self.defence == v:
			return
		self.defence = v

	def addAttack_Max(self, val):
		v = self.attack_Max + val
		if v < 0:
			v = 0

		if self.attack_Max == v:
			return
		self.attack_Max = v

	def addAttack_Min(self, val):
		v = self.attack_Min + val
		if v < 0:
			v = 0

		if self.attack_Min == v:
			return
		self.attack_Min = v

	def setHP(self, hp):
		"""
		defined
		"""
		hp = hp
		if hp < 0:
			hp = 0
		if hp > self.HP_Max:
			hp = self.HP_Max

		if self.HP == hp:
			return

		self.HP = hp

	def setEG(self, eg):
		"""
		defined
		"""
		eg = eg
		if eg < 0:
			eg = 0
		if eg > self.EG_Max:
			eg = self.EG_Max
		if self.EG == eg:
			return

		self.EG = eg

	def setHPMax(self, hpMax):
		"""
		defined
		"""
		hpmax = hpMax
		self.HP_Max = hpmax

	def setEGMax(self, egMax):
		"""
		defined
		"""
		egMax = egMax
		self.EG_Max = egMax
	
	def addEndurance(self, val):
		v = self.endurance + val
		if v < 0:
			v = 0

		if self.endurance == v:
			return
		self.endurance = v

	def setEndurance(self, val):
		"""
		defined
		"""
		val = val
		if val < 0:
			val = 0

		if self.endurance == val:
			return

		self.endurance = val
		
	def addWill(self, val):
		v = self.will + val
		if v < 0:
			v = 0

		if self.will == v:
			return
		self.will = v
		
	def setWill(self, val):
		"""
		defined
		"""
		val = val
		if val < 0:
			val = 0

		if self.will == val:
			return

		self.will = val
	
	def addDodge(self, val):
		v = self.dodge + val
		if v < 0:
			v = 0

		if self.dodge == v:
			return
		self.dodge = v
		
	def setDodge(self, val):
		"""
		defined
		"""
		val = val
		if val < 0:
			val = 0

		if self.dodge == val:
			return

		self.dodge = val
		
	def addCrit(self, val):
		v = self.crit + val
		if v < 0:
			v = 0

		if self.crit == v:
			return
		self.crit = v
		
	def setCrit(self, val):
		"""
		defined
		"""
		val = val
		if val < 0:
			val = 0

		if self.crit == val:
			return

		self.crit = val
		
	def addHit(self, val):
		v = self.hit + val
		if v < 0:
			v = 0

		if self.hit == v:
			return
		self.hit = v
		
	def setHit(self, val):
		"""
		defined
		"""
		val = val
		if val < 0:
			val = 0

		if self.hit == val:
			return

		self.hit = val

	def addParry(self, val):
		v = self.parry + val
		if v < 0:
			v = 0

		if self.parry == v:
			return
		self.parry = v
		
	def setParry(self, val):
		"""
		defined
		"""
		val = val
		if val < 0:
			val = 0

		if self.parry == val:
			return

		self.parry = val

	def addStealth(self, val):
		v = self.stealth + val
		if v < 0:
			v = 0

		if self.stealth == v:
			return
		self.stealth = v
		
	def setStealth(self, val):
		"""
		defined
		"""
		val = val
		if val < 0:
			val = 0

		if self.stealth == val:
			return

		self.stealth = val

	def addAttackPower(self, val):
		v = self.attackPower + val
		if v < 0:
			v = 0

		if self.attackPower == v:
			return
		self.attackPower = v
		
	def setAttackPower(self, val):
		"""
		defined
		"""
		val = val
		if val < 0:
			val = 0

		if self.attackPower == val:
			return

		self.attackPower = val
		
	def addDefencePower(self, val):
		v = self.defencePower + val
		if v < 0:
			v = 0

		if self.defencePower == v:
			return
		self.defencePower = v
		
	def setDefencePower(self, val):
		"""
		defined
		"""
		val = val
		if val < 0:
			val = 0

		if self.defencePower == val:
			return

		self.defencePower = val

	def addStrength(self, val):
		v = self.strength + val
		if v < 0:
			v = 0

		if self.strength == v:
			return
		self.strength = v

	def setStrength(self, val):
		"""
		defined
		"""
		val = val
		if val < 0:
			val = 0

		if self.strength == val:
			return

		self.strength = val
		
	def addProperty(self, property, value):
		if property == GlobalDefine.ATTRIBUTE_HEALTH:
			self.addHP(value)
		if property == GlobalDefine.ATTRIBUTE_ENERGY:
			self.addEG(value)
		if property == GlobalDefine.ATTRIBUTE_STRENGTH:
			self.addStrength(value)
		if property == GlobalDefine.ATTRIBUTE_WILL:
			self.addWill(value)
		if property == GlobalDefine.ATTRIBUTE_ENDURANCE:
			self.addEndurance(value)
		if property == GlobalDefine.ATTRIBUTE_ATTACK_POWER:
			self.addAttackPower(value)
		if property == GlobalDefine.ATTRIBUTE_DEFENSE_POWER:
			self.addDefencePower(value)
		if property == GlobalDefine.ATTRIBUTE_HIT:
			self.addHit(value)
		if property == GlobalDefine.ATTRIBUTE_DODGE:
			self.addDodge(value)
		if property == GlobalDefine.ATTRIBUTE_PARRY:
			self.addParry(value)
		if property == GlobalDefine.ATTRIBUTE_STEALTH:
			self.addStealth(value)
		if property == GlobalDefine.ATTRIBUTE_CRITICAL:
			self.addCrit(value)

	def getProperty(self, property):
		if property == GlobalDefine.ATTRIBUTE_HEALTH:
			return self.HP
		if property == GlobalDefine.ATTRIBUTE_ENERGY:
			return self.EG
		if property == GlobalDefine.ATTRIBUTE_STRENGTH:
			return self.strength
		if property == GlobalDefine.ATTRIBUTE_WILL:
			return self.will
		if property == GlobalDefine.ATTRIBUTE_ENDURANCE:
			return self.endurance
		if property == GlobalDefine.ATTRIBUTE_ATTACK_POWER:
			return self.attackPower
		if property == GlobalDefine.ATTRIBUTE_DEFENSE_POWER:
			return self.defencePower
		if property == GlobalDefine.ATTRIBUTE_HIT:
			return self.hit
		if property == GlobalDefine.ATTRIBUTE_DODGE:
			return self.dodge
		if property == GlobalDefine.ATTRIBUTE_PARRY:
			return self.parry
		if property == GlobalDefine.ATTRIBUTE_STEALTH:
			return self.stealth
		if property == GlobalDefine.ATTRIBUTE_CRITICAL:
			return self.crit
		
	def setProperty(self, property, value):
		if property == GlobalDefine.ATTRIBUTE_HEALTH:
			self.setHP(value)
		if property == GlobalDefine.ATTRIBUTE_ENERGY:
			self.setEG(value)
		if property == GlobalDefine.ATTRIBUTE_STRENGTH:
			self.setStrength(value)
		if property == GlobalDefine.ATTRIBUTE_WILL:
			self.setWill(value)
		if property == GlobalDefine.ATTRIBUTE_ENDURANCE:
			self.setEndurance(value)
		if property == GlobalDefine.ATTRIBUTE_ATTACK_POWER:
			self.setAttackPower(value)
		if property == GlobalDefine.ATTRIBUTE_DEFENSE_POWER:
			self.setDefencePower(value)
		if property == GlobalDefine.ATTRIBUTE_HIT:
			self.setHit(value)
		if property == GlobalDefine.ATTRIBUTE_DODGE:
			self.setDodge(value)
		if property == GlobalDefine.ATTRIBUTE_PARRY:
			self.setParry(value)
		if property == GlobalDefine.ATTRIBUTE_STEALTH:
			self.setStealth(value)
		if property == GlobalDefine.ATTRIBUTE_CRITICAL:
			self.setCrit(value)
