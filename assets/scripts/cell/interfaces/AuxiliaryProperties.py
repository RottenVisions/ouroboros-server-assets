# -*- coding: utf-8 -*-
import Ouroboros
import GlobalDefine
from ATTRIBUTE_INFO import TAttributeInfo
from ATTRIBUTE_INFO import TAttributeInfoList
from OURODebug import *


class AuxiliaryProperties:
	"""
	All about Auxiliary attributes
	"""

	def __init__(self):
		# Clear list if empty
		if len(self.activeAttributes.items()) == 0:
			self.clearAttributeList()

	def addAttribute(self, attacher, attribute):
		newAttrib = TAttributeInfo()
		newAttrib.extend([attacher, attribute])
		if newAttrib not in self.activeAttributes.items():
			self.activeAttributes[attribute] = newAttrib

	def removeAttribute(self, attacher, attribute):
		for key, info in list(self.activeAttributes.items()):
			if key == attribute:
				if info[0] == attacher:
					del self.activeAttributes[key]

	def clearAttributeList(self):
		self.currentEntityItemListInfo = TAttributeInfoList()