from spyne import ComplexModel, Unicode, Integer, Array

class PostHighlight(ComplexModel):
	__namespace__ = 'highlight'
	
	name = Unicode
	lastname = Unicode
	nickname = Unicode
	description = Unicode

class PostRecommendation(ComplexModel):
	__namespace__ = 'post'
	
	id = Integer
	name = Unicode
	type = Unicode
	lastname = Unicode
	nickname = Unicode
	description = Unicode
	picture = Unicode

class SearchModel(ComplexModel):
	__namespace__ = 'search'
	
	highlight = PostHighlight
	post = PostRecommendation

