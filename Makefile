# default var dataset = mnist
data_set ?= MNIST
pipeline_name ?= mnist_flwr
num_client ?= 2
epochs ?= 3
datastore_name ?= mnist
batch_size ?= 128
lr ?= 0.001
orchestrator_name ?= orchestrator-01

prepare-data:
	python ./examples/pipelines/utils/upload_data/submit.py --example $(data_set)

run-fl:
	python ./examples/pipelines/${pipeline_name}/submit.py

gen-config:
	python ./examples/pipelines/utils/gen_config/main.py \
	--output_dir . \
	--number_silos ${num_client} \
	--orchestrator ${orchestrator_name} \
	--epochs ${epochs} \
	--lr ${lr} \
	--batch_size ${batch_size} \
	--datastore_name ${datastore_name}