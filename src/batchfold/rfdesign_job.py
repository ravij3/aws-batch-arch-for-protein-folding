# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from attrs import define, field
from batchfold.batchfold_job import BatchFoldJob
from datetime import datetime
import logging
import uuid

@define(kw_only=True)
class RFDesignHallucinateJob(BatchFoldJob):
    """Define RFDesign Hallucinate Job"""
    target_id: str
    input_s3_uri: str
    output_s3_uri: str 
    pdb: str    
    output_dir: str = uuid.uuid4().hex
    job_definition_name: str = "RFDesignJobDefinition"
    weights_dir: str = "/database/rfdesign_params/hallucination"
    params: dict = {}
    job_name: str = field(default="RFDesignHallucinateJob" + datetime.now().strftime("%Y%m%d%s"))
    job_definition_name: str = field(default="RFDesignJobDefinition")
    cpu: int = field(default=4)
    memory: int = field(default=16)
    gpu: int = field(default=1)
       
    def __attrs_post_init__(self) -> None:
        """Override default BatchFoldJob command"""

        command_list = [f"-i {self.input_s3_uri}:{self.output_dir}/input/"]
        command_list.extend([f"-o {self.output_dir}/output/:{self.output_s3_uri}/"])
        command_list.extend([
            "python hallucination/hallucinate.py",
            f"--pdb={self.output_dir}/input/{self.pdb}",
            f"--out={self.output_dir}/predictions/output",
            f"--weights_dir={self.weights_dir}" 
        ])
        command_list.extend([f"--{key}={value}" for key, value in self.params.items()])
        logging.info(f"Command is \n{command_list}")
        self.define_container_overrides(command_list, self.cpu, self.memory, self.gpu)
        return None

@define(kw_only=True)
class RFDesignInpaintJob(BatchFoldJob):
    """Define RFDesign Inpainting Job"""
    target_id: str
    input_s3_uri: str
    output_s3_uri: str 
    pdb: str    
    output_dir: str = uuid.uuid4().hex
    job_definition_name: str = "RFDesignJobDefinition"
    checkpoint: str = "/database/rfdesign_params/inpainting/BFF_mix_epoch25.pt"
    params: dict = {}
    job_name: str = field(default="RFDesignInpaintingJob" + datetime.now().strftime("%Y%m%d%s"))
    job_definition_name: str = field(default="RFDesignJobDefinition")
    cpu: int = field(default=4)
    memory: int = field(default=16)
    gpu: int = field(default=1)
       
    def __attrs_post_init__(self) -> None:
        """Override default BatchFoldJob command"""

        command_list = [f"-i {self.input_s3_uri}:{self.output_dir}/input/"]
        command_list.extend([f"-o {self.output_dir}/output/:{self.output_s3_uri}"])
        command_list.extend([
            "python inpainting/inpaint.py",
            f"--pdb={self.output_dir}/input/{self.pdb}",
            f"--out={self.output_dir}/predictions/output",
            f"--checkpoint={self.weights_dir}" 
        ])
        command_list.extend([f"--{key}={value}" for key, value in self.params.items()])
        logging.info(f"Command is \n{command_list}")
        self.define_container_overrides(command_list, self.cpu, self.memory, self.gpu)
        return None        