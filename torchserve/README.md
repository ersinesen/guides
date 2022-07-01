# Serving PyTorch Models with TorchServe

TorchServe is a tool for serving PyTorch eager mode and torschripted models.

1. [Install](https://github.com/pytorch/serve/blob/master/README.md#install-torchserve) or get docker ```docker pull pytorch/torchserve```.

2. Prepare the required model archive file (.mar) with [torch-model-arhiver](https://github.com/pytorch/serve/tree/master/model-archiver):

```
pip install torch-model-archiver
torch-model-archiver --model-name X --version 1.0 --model-file XModel.py --serialized-file weights/XModel.pt -r requirements.txt --export-path models --handler handler.py --extra-files my.pickle

```

**-r**: required libraries to install for your model

**--handler**: your inference code will be here

**--extra-files**: if you need additional files (data, etc.) list them here

**Warning for pytorch-lightning**: its Trainer save checkpoint in its custom format. weigth file should be saved by torch.

3. Serve with torchserver container (overwrite default config.properties to install additional requirements in the mar file):

```
docker run --rm --shm-size=1g \
        --ulimit memlock=-1 \
        --ulimit stack=67108864 \
        -v $(pwd)/torchserve.config.properties:/home/model-server/config.properties \
        -p8080:8080 \
        -p8081:8081 \
        -p8082:8082 \
        -p7070:7070 \
        -p7071:7071 \
        --mount type=bind,source=/home/X/models,target=/home/model-server/model-store\
        pytorch/torchserve torchserve --model-store=/home/model-server/model-store \
        --models X.mar 
```

4. [Inference](https://pytorch.org/serve/inference_api.html)

```
curl http://localhost:8080/ping
curl -X OPTIONS http://localhost:8080
curl http://localhost:8080/predictions/X -T input_file
```


# Links
 
* [TorchServe](https://pytorch.org/serve/)

* [torch-model-arhiver](https://github.com/pytorch/serve/tree/master/model-archiver):

* [Inference API](https://pytorch.org/serve/inference_api.html)

* [TorchServe: Model Serving on PyTorch](https://morioh.com/p/b3c854aa2828)

* [Create custom torchserve handlers](https://www.pento.ai/blog/custom-torchserve-handlers)
