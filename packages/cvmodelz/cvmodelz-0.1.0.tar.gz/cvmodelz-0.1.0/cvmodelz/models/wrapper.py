import chainer

from chainer import functions as F
from collections import OrderedDict

from cvmodelz.models.base import BaseModel
from cvmodelz.models.meta_info import ModelInfo



class ModelWrapper(BaseModel):
	"""
		This class is designed to wrap around chainercv2 models
		and provide the loading API of the BaseModel class.
		The wrapped model is stored under self.wrapped
	"""

	def __init__(self, model: chainer.Chain, *args, **kwargs):
		super().__init__(*args, **kwargs)

		name = model.__class__.__name__
		self.__class__.__name__ = name
		self.meta.name = name

		if hasattr(model, "meta"):
			self.meta = model.meta

		with self.init_scope():
			self.wrapped = model
			delattr(self.wrapped.features, "final_pool")

		self.meta.feature_size = self.clf_layer.W.shape[-1]

	def init_model_info(self):
		self.meta = ModelInfo(
			classifier_layers=("output/fc",),
			conv_map_layer="features",
			feature_layer="pool",
		)

	@property
	def model_instance(self) -> chainer.Chain:
		return self.wrapped

	@property
	def functions(self) -> OrderedDict:

		links = [
			("features", [self.wrapped.features]),
			("pool", [self.pool]),
			("output/fc", [self.wrapped.output.fc]),
		]

		return OrderedDict(links)

	def load(self, *args, path="", **kwargs):
		paths = [path, f"{path}wrapped/"]
		for _path in paths:
			try:
				return super().load(*args, path=_path, **kwargs)
			except KeyError as e:
				pass

		raise RuntimeError(f"tried to load weights with paths {paths}, but did not succeeed")

	def forward(self, X, layer_name=None):
		if layer_name is None:
			res = self.wrapped(X)

		elif layer_name == self.meta.conv_map_layer:
			res = self.wrapped.features(X)

		elif layer_name == self.meta.feature_layer:
			conv = self.wrapped.features(X)
			res = self.pool(conv)

		elif layer_name == self.clf_layer_name:
			conv = self.wrapped.features(X)
			feat = self.pool(conv)
			res = self.wrapped.output(feat)

		else:
			raise ValueError(f"Dont know how to compute \"{layer_name}\"!")

		return res

