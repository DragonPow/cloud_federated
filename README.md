# Run a Federated Learning to Cloud Azure

> ⚠️ This repo is cloned from repo [azure-ml-federated-learning](https://github.com/Azure-Samples/azure-ml-federated-learning) with some implemented

## Prepare before train

1. Create [azure ml workspace](https://ml.azure.com/home) account
   1. You need using azure account for student to free first 100$ in 1 year. Subscribe [here](https://portal.azure.com/) (resource name `Azure for Students`
)
2. Create [compute](https://ml.azure.com/compute/list) job: which use to run train model as a node computer:
   1. Job will pricing by hour starting, so whenever you need to train model, start it
   2. You can custom time schedule stop after 15 minutes not using job (but be careful job is stop in a model when waiting another job done)
3. Create [datastore](https://ml.azure.com/data/datastore): save model, file, dataset,...
   1. The datastore will make much money, so limit uploading/downloading from here
4. Download config file subscription of account as a `config.yaml` files, and store in this project
5. Using [azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) to connect from your machine local to azure cloud easily
   1. You need to connect to azure using command `az login` first to run script above

## Launch the demo

1. Create a conda environment with all the python dependencies, then activate it.
```
conda env create --file ./examples/pipelines/environment.yml
conda activate fl_experiment_conda_env
```
Alternatively, you can install the dependencies directly:
```
python -m pip install -r ./examples/pipelines/requirements.txt
```
2. To connect to your newly created Azure ML workspace, you'll need to provide the following info in the sample python script as CLI arguments.
```
python ./pipelines/mnist_scatter_gather/submit.py --subscription_id <subscription_id> --resource_group <resource_group> --workspace_name <workspace_name> --example MNIST
```
With some parameter can get from root `config.yaml` you ownload in step prepare azure, or you can override config in `pipelines/mnist_scatter_gather/config.yaml`

## Custom new model to train

1. Create new folder in pipelines name `my_model` with template like `pipelines/mnist_flwr/`
2. Custom flower alg in file `components/FLWR/client`
   1. Custom aggregate if needed in `components/utils/aggregatemodelweights/`
3. Suggest how to get dataset from cloud, see in file `pipelines/utils/upload_data/submit.py`