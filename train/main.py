from .train import main
import os

from pathlib import Path
from comet_ml import Experiment

comet_api_key = os.environ["COMET_API_KEY"]
project_name = "animalese"
experiment_name = "1"
experiment = Experiment(api_key=comet_api_key, project_name=project_name, parse_args=False)
experiment.set_name(experiment_name)
# experiment.display()

learning_rate = 5e-4
batch_size = 10
epochs = 10
dataset_path = str(Path(__file__).parent.parent / "data" / "BlathersSpeech-1.2")

main(learning_rate, batch_size, epochs, dataset_path, experiment)