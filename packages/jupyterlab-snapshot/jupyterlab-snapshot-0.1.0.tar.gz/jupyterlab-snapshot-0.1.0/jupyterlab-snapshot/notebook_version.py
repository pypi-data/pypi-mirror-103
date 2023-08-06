
def save_version(path, nb_name, message):
    if not path:
        raise RuntimeError('sss')
    version = ''
    version_save_path = f'{nb_name}/{version}/{nb_name}.ipynb'
    # copy or upload notebook from path to version_save_path
    # todo


def get_versions_info(path):
    nb_name = ''
    versions_info_path = f'{nb_name}/versions_info.json'


def revert_to_version(path, version):
    pass


def copy_version_to_new_notebook(path, version):
    pass
