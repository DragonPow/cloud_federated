import argparse
from os import path
from string import Template

TEMPLATE_FILE = 'template.yaml'
CONFIG_FILE = 'config.yaml'
CURRENT_DIR = path.dirname(__file__)
print('Current dir', CURRENT_DIR)

def generate_silos(number_silos, datastore_name):
    silos = []
    for i in range(number_silos):
        silos.append(f"""
    - name: silo{i}
      computes:
      - silo-{i}
      datastore: datastore_silo{i}
      silo_data:
        type: uri_folder
        mode: 'download'
        path: azureml://datastores/datastore_silo{i}/paths/federated_learning/{datastore_name}""")
    return "\n".join(silos)

def generate_config(number_silos, datastore_name, orchestrator, training_parameters):
    silos = generate_silos(number_silos, datastore_name)
    # read content from template.yaml
    with open(path.join(CURRENT_DIR, TEMPLATE_FILE), 'r') as f:
        templateStr = f.read()

    template = Template(templateStr)
    config_content = template.substitute(
        orchestrator=orchestrator,
        silos=silos,
        num_of_iterations=training_parameters['num_of_iterations'],
        epochs=training_parameters['epochs'],
        lr=training_parameters['lr'],
        batch_size=training_parameters['batch_size']
    )
    return config_content

if __name__ == "__main__":
    # Define command-line arguments
    parser = argparse.ArgumentParser(description='Generate config.yaml from arguments.')
    parser.add_argument('--number_silos', type=int, required=True, help='Number of silos to generate.')
    parser.add_argument('--output_dir', type=str, default=CURRENT_DIR, help='Output directory for config.yaml.')
    parser.add_argument('--datastore_name', type=str, default='pneumonia', help='Name of the Azure ML datastore.')
    parser.add_argument('--orchestrator', required=True, help='Name of the orchestrator compute.')
    parser.add_argument('--num_of_iterations', type=int, default=3, help='Number of iterations (in-silo training).')
    parser.add_argument('--epochs', type=int, default=3, help='Number of epochs per iteration (in-silo training).')
    parser.add_argument('--lr', type=float, default=0.01, help='Learning rate.')
    parser.add_argument('--batch_size', type=int, default=64, help='Batch size.')
    args = parser.parse_args()

    # Create training_parameters object
    training_parameters = {
        "num_of_iterations": args.num_of_iterations,
        "epochs": args.epochs,
        "lr": args.lr,
        "batch_size": args.batch_size
    }

    # Generate config.yaml
    content = generate_config(args.number_silos, args.datastore_name, args.orchestrator, training_parameters)
    with open(path.join(args.output_dir, CONFIG_FILE), 'w') as f:
        f.write(content)
    print(f"Generated config.yaml in {args.output_dir} successfully.")
