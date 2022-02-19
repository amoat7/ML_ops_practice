'''
Name: David Amoateng
Date: Today

Description: Library to log artifacts to wandb.ai
'''

import argparse
from ast import arguments
import logging
import pathlib
import wandb

# logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s - %(levelname)s - %(message)s",
    filename='log.log',
    filemode="w"
)
logger = logging.getLogger()


def track_artifacts(args):
    '''
    Upload artifacts function

    Inputs:
       args-  Argparser arguments

    Outputs: None
    '''
    logger.info('Creating upload artifacts exercise')

    with wandb.init(project="upload_artifact") as run:
        artifact = wandb.Artifact(
            name=args.artifact_name,
            type=args.artifact_type,
            description=args.artifact_description
        )
        artifact.add_file(args.input_file)
        run.log_artifact(artifact)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload artifacts to W&B"
    )

    parser.add_argument(
        "--input_file",
        type=pathlib.Path,
        help="Path to input file",
        required=True)

    parser.add_argument(
        "--artifact_name", type=str, help="Name of artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type of artifact", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description of artifact",
        required=True)

    arguemnts = parser.parse_args()

    track_artifacts(arguments)
