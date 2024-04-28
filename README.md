# Introduction
This report presents the instruction to install and run the code for the project.


# Installation
    -Install [azfuse](https://github.com/microsoft/azfuse). The tool is used to automatically download the data. The configuration of AzFuse has already been in this repo.

    -Download the source code by
        shell
        git clone https://github.com/microsoft/GenerativeImage2Text.git
        cd GenerativeImage2Text

    - install the package
        shell
        pip install -r requirements.txt
        python setup.py build develop
        Note: CUDA is required compulsory for the code to run. If you don't have a GPU, you can use the CPU version of the code by changing the `device` parameter in the `config.py` file to `cpu`.
    - download the model
        https://drive.google.com/file/d/1poXLUaxzlkDNE4kJBDnil_bORO6req87/view?usp=drive_link

# Inference
    -Inference on a single image
    # single image, captioning
    python -m generativeimage2text.inference -p "{'type': 'test_git_inference_single_image', 'image_path': 'aux_data/images/1.jpg', 'model_name': 'GIT_BASE_COCO', 'prefix': ''}"

    -Inference on a [TSV](https://en.wikipedia.org/wiki/Tab-separated_values) file, which is a collection of multiple images.
    - Data format (for information only)
        - image TSV: Each row has two columns. The first is the image key; the second is base64-encoded jpg or png bit string.
        - caption or question tsv: Each row has two columns. The first is the image key; the second is a list of dictionaries in the json format. For caption TSV,
                the dictionary should contain at least the field of `'caption'`. For the question answering TSV, it should contain at least `question_id` and `question`.

    - Inference on [COCO](https://cocodataset.org) Karpathy test.

        1. Prepare the coco test TSV

           mkdir -p aux_data/raw_data
           wget http://images.cocodataset.org/zips/val2014.zip -O aux_data/raw_data/val2014.zip
           wget http://cs.stanford.edu/people/karpathy/deepimagesent/caption_datasets.zip -O aux_data/raw_data/caption_datasets.zip
           cd aux_data/raw_data
           unzip val2014.zip
           unzip caption_datasets.zip
           python -m generativeimage2text.data_prepare -p "{'type': 'prepare_coco_test'}"

        2. Inference on the coco test TSV
        python -m generativeimage2text.inference -p "{'type': 'test_git_inference_single_tsv', 'image_tsv': 'data/coco_caption/test.img.tsv', 'model_name': 'GIT_BASE_COCO', 'question_tsv': null,'out_tsv': 'inference/GIT_BASE_COCO/coco.tsv'}"
            (optional) To exactly reproduce the number:
             nvidia-docker run --ipc=host amsword/setup:py38pt19u20cu11
                   bash -c "mkdir -p /tmp/code
                   && cd /tmp/code
                   && pip install git+https://github.com/microsoft/azfuse.git
                   && git clone https://github.com/amsword/generativeimage2text.git
                   && cd generativeimage2text
                   && pip install -r requirements.txt
                   && python setup.py build develop
                   && AZFUSE_TSV_USE_FUSE=1 python -m generativeimage2text.inference -p "{'type': 'test_git_inference_single_tsv',
                            'image_tsv': 'data/coco_caption/test.img.tsv',
                            'model_name': 'GIT_BASE_COCO',
                            'question_tsv': null,
                            'out_tsv': 'inference/GIT_BASE_COCO/coco.tsv',
                      }"
                   &&  AZFUSE_TSV_USE_FUSE=1 python -m generativeimage2text.inference -p "{'type': 'evaluate_on_coco_caption',
                       'res_file': 'inference/GIT_BASE_COCO/coco.tsv',
                       'label_file': 'data/coco_caption/test.caption.tsv',
                       'outfile': 'inference/GIT_BASE_COCO/coco.score.json',
                       }"
                   && cat inference/GIT_BASE_COCO/coco.score.json
                   "
                   
#   Evaluate the result
        python -m generativeimage2text.inference -p "{'type': 'evaluate_on_coco_caption', 'res_file': 'inference/GIT_BASE_COCO/coco.tsv','label_file': 'data/coco_caption/test.caption.tsv'}"
        Scores could be varied due to the misalignment of the environment, e.g. pytorch version.
