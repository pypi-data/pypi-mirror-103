from anyio import run
from .model import Model
from pathlib import Path

model = Model('test')
run(model.load_model, Path.cwd()/'omniblack/model/structs')
import code
code.interact(local=locals() | globals())

