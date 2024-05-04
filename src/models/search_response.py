class PostHighlight:
	def __init__(self, name=None, lastname=None, nickname=None, description=None):
		self.name = name
		self.lastname = lastname
		self.nickname = nickname
		self.description = description

	@staticmethod
	def from_map(map):
		return PostHighlight(
			name=map.get('name'),
			lastname=map.get('lastname'),
			nickname=map.get('nickname'),
			description=map.get('description'),
		)


class PostRecommendation:
	def __init__(self, id, name, type, lastname=None, nickname=None, description=None, picture=None):
		self.id = id
		self.name = name
		self.type = type
		self.lastname = lastname
		self.nickname = nickname
		self.description = description
		self.picture = picture

	@staticmethod
	def from_map(map):
		return PostRecommendation(
			id=map['id'],
			name=map['name'],
			type=map['type'],
			lastname=map.get('lastname'),
			nickname=map.get('nickname'),
			description=map.get('description'),
			picture=map.get('picture'),
		)


class SearchModel:
	def __init__(self, highlight, post):
		self.highlight = highlight
		self.post = post

	@staticmethod
	def from_map(map):
		return SearchModel(
			highlight=PostHighlight.from_map(map=map['highlight']),
			post=PostRecommendation.from_map(map=map['post']),
		)