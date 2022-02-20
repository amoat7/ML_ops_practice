import argparse
from ast import parse
import logging 
import pathlib
import tempfile
import wandb
import requests

logging.basicConfig(
    level=logging.INFO,
    filemode="w",
    filename="log.log",
    format="%(asctime)-15s - %(levelname)s - %(message)s",
)

def download_data(args):
    base = pathlib.Path(args.file_url).name.split("?")[0].split("#")[0]

    logging.info(f"Downloading {args.file_url} ...")
    with tempfile.NamedTemporaryFile(mode='wb+') as fp:
        logging.info("Creating run exercise_2")
        with wandb.init(project="exercise_2", job_type="download_data") as run:
            # Download the file streaming and write to open temp file
            with requests.get(args.file_url, stream=True) as r:
                for chunk in r.iter_content(chunk_size=8192):
                    fp.write(chunk)

            # Make sure the file has been written to disk before uploading
            # to W&B
            fp.flush()

            logging.info("Creating artifact")
            artifact = wandb.Artifact(
                name=args.artifact_name,
                type=args.artifact_type,
                description=args.artifact_description,
                metadata={'original_url': args.file_url}
            )

            artifact.add_file(fp.name, name=base)
            logging.info("Logging artifact")
            run.log(artifact)

            artifact.wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download a file and upload it to W&B"
    )

    parser.add_argument(
        "--file_url", type=str, help="URL to the input file", required=True
    )
    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )
    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_description", type=str, help="Description for the artifact", required=True
    )

    args = parser.parse_args()

    download_data(args)