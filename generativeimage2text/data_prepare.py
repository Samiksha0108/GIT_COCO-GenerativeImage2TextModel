import base64
import os.path as op
from pprint import pformat
from .common import parse_general_args, json_dump
from .common import qd_tqdm as tqdm
import logging
from .common import load_list_file, read_to_buffer
import json
from .common import init_logging, hash_sha1, write_to_file
from .taxonomy import noffset_to_synset, get_nick_name
from .tsv_io import tsv_writer


def get_imagenet_unique_nick_names():
    txt = './aux_data/imagenet/LOC_synset_mapping.txt'
    noffsets = load_list_file(txt)
    noffsets = [x.split(' ')[0] for x in noffsets]
    assert hash_sha1(noffsets) == 'fb9737bbca048296520bc35582947b3755aa948f'
    nick_name_overwrite = {
        'n02012849': 'crane bird',
        'n03126707': 'crane machine',
        'n02113186': 'cardigan dog',
        'n02963159': 'cardigan jacket',
        'n03710637': 'maillot tights',
        'n03710721': 'maillot bathing suit',
    }
    nick_names = [nick_name_overwrite[n] if n in nick_name_overwrite else
          get_nick_name(noffset_to_synset(n)) for n in noffsets]
    assert hash_sha1(nick_names) == '9c1dd12d7e8120820ffd44b75ebe8b78b659a4f4'
    assert len(set(nick_names)) == len(nick_names)
    assert len(set(map(lambda n: n.replace(' ', ''), nick_names))) == len(nick_names)
    return nick_names

def generate_imagenet_unique_names():
    nick_names = get_imagenet_unique_nick_names()
    write_to_file('\n'.join(nick_names),
                  './aux_data/imagenet/imagenet_unique_readable_names.txt')


def prepare_coco_test():
    """
    prepare the test set for coco captioning
    Returns: None
    """
    image_folder = 'aux_data/raw_data/val2014' # the folder containing the images
    json_file = 'aux_data/raw_data/dataset_coco.json' # the json file containing the captions
    infos = json.loads(read_to_buffer(json_file))['images'] # the json file
    infos = [i for i in infos if i['split'] == 'test'] # only use the test set
    assert all(i['filepath'] == 'val2014' for i in infos) # all images are in val2014

    def gen_rows():
        """
        generate the rows for the tsv file
        Returns: generator of rows
        """
        for i in tqdm(infos):
            payload = base64.b64encode(read_to_buffer(op.join(image_folder,i['filename']))) # read the image
            yield i['cocoid'], payload # yield the image
    tsv_writer(gen_rows(), 'data/coco_caption/test.img.tsv')

    def gen_cap_rows():
        """
        generate the rows for the caption tsv file
        Returns:
        """
        for i in tqdm(infos):
            caps = [{'caption': j['raw']} for j in i['sentences']]  # get the captions
            yield i['cocoid'], json_dump(caps) # yield the captions
    tsv_writer(gen_cap_rows(), 'data/coco_caption/test.caption.tsv')


if __name__ == '__main__':
    init_logging()
    kwargs = parse_general_args()
    logging.info('param:\n{}'.format(pformat(kwargs)))
    function_name = kwargs['type']
    del kwargs['type']
    locals()[function_name](**kwargs)

