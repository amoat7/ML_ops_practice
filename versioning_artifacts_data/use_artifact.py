import argparse
from ast import arg
import logging
import pathlib
import wandb 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s - %(levelname)s - %(message)s",
    filename='log.log',
    filemode="w"
)
logger = logging.getLogger()

def use_artifacts(args):
    logger.info("Running use artifacts module")
    with wandb.init(project="upload_artifact", job_type="use_file") as run:
        artifact = run.use_artifact(args.artifact_name)
        logger.info("Artifact content")
        filepath = artifact.file()

        with open(filepath, "r") as fp:
            content = fp.read()
        print(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Use an artifact from wandb"
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name and version of wandb artifact", required=True
    )

    args = parser.parse_args()

    use_artifacts(args)
