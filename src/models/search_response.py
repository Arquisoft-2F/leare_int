from spyne import ComplexModel, Unicode, Integer, Array

class PostHighlight(ComplexModel):
	__namespace__ = 'highlight'
	
	name = Array(Unicode)
	lastname = Array(Unicode)
	nickname = Array(Unicode)
	description = Array(Unicode)

class PostRecommendation(ComplexModel):
	__namespace__ = 'post'
	
	id = Unicode
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

