from anyio import run
from .model import Model
from pathlib import Path


async def main():
    global model
    model = Model('test')
    await model.load_model_package('omniblack.model.structs')
    print(model)
    print(model.structs)
    print(model.types)
    print(model.formats)
    print(model.structs.struct)


run(main)
