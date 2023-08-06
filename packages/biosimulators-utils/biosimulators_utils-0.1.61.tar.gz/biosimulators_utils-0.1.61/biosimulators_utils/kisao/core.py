""" Methods for working with KiSAO

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2021-04-26
:Copyright: 2021, Center for Reproducible Biomedical Modeling
:License: MIT
"""

from ..config import get_app_dirs
from .data_model import NAMESPACE
import glob
import natsort
import os
import pronto
import requests
import warnings

__all__ = [
    'get',
    'get_term',
    'get_child_terms',
    'get_parent_terms',
    'get_term_ids',
]

KISAO_URL = 'https://raw.githubusercontent.com/SED-ML/KiSAO/{}/kisao.owl'
KISAO_TAGS_ENDPOINT = 'https://api.github.com/repos/SED-ML/KiSAO/tags'


def get_latest_version():
    """ Get the latest version of the KiSAO ontology

    Returns:
        :obj:`str`: latest version of KiSAO
    """
    response = requests.get(KISAO_TAGS_ENDPOINT)
    response.raise_for_status()
    tags = natsort.natsorted(response.json(), key=lambda tag: tag['name'])
    return tags[-1]['name']


def get_installation_dirname():
    """ Get the directory where versions KiSAO are/should be installed

    Returns:
        :obj:`str`: path where versions KiSAO are/should be installed
    """
    return os.path.join(get_app_dirs().user_data_dir, 'kisao')


def get_installation_filename(version, dirname=None):
    """ Get the path where KiSAO is/should be installed

    Args:
        version (:obj:`str`): version to install
        dirname (:obj:`str`, optional): path where KiSAO is/should be installed. Default: use
            the path managed by BioSimulators utils

    Returns:
        :obj:`str`: path where KiSAO is/should be installed
    """
    dirname = dirname or get_installation_dirname()
    return os.path.join(dirname, version + '.owl')


def get_installed_versions(dirname=None):
    """ Get the installed versions of KiSAO in descending order

    Args:
        dirname (:obj:`str`, optional): path where KiSAO is/should be installed. Default: use
            the path managed by BioSimulators utils

    Returns:
        :obj:`list` of :obj:`str:` installed versions of KiSAO in descending order
    """
    dirname = dirname or get_installation_dirname()
    filenames = glob.glob(os.path.join(dirname, '*.owl'))
    versions = [os.path.relpath(filename, dirname)[0:-4] for filename in filenames]
    return natsort.natsorted(versions, reverse=True)


def download(version='deploy'):
    """ Download the KiSAO ontology

    Args:
        version (:obj:`str`, optional): version to download

    Returns:
        :obj:`bytes`: content of KiSAO
    """
    response = requests.get(KISAO_URL.format(version))
    response.raise_for_status()
    return response.content


def install(version=None, dirname=None):
    """ Download KiSAO and save it locally

    Args:
        version (:obj:`str`, optional): version to install
        dirname (:obj:`str`, optional): path where KiSAO is/should be installed. Default: use
            the path managed by BioSimulators utils

    Returns:
        :obj:`tuple` of :obj:`str`: installed version and the path to where its installed
    """
    version = version or get_latest_version()
    filename = get_installation_filename(version, dirname=dirname)
    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    content = download(version)
    with open(filename, 'wb') as file:
        file.write(content)

    return version, filename


def read_ontology(filename):
    """ Read a version of KiSAO

    Args:
        filename (:obj:`str`): path to a version of KiSAO

    Returns:
        :obj:`pronto.Ontology`: ontology
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", pronto.utils.warnings.SyntaxWarning)
        warnings.simplefilter("ignore", pronto.utils.warnings.NotImplementedWarning)
        return pronto.Ontology(filename)


def load(version=None, dirname=None, check_for_latest=False):
    """ Load a version of KiSAO

    Args:
        version (:obj:`str`, optional): version to load; default load latest installed version
            or install the latest version if none is installed
        dirname (:obj:`str`, optional): path where KiSAO is/should be installed. Default: use
            the path managed by BioSimulators utils
        check_for_latest (:obj:`bool`, optional): if :obj:`True`, check for a newer version and
            if there is one, install it

    Returns:
        :obj:`pronto.Ontology`: ontology
    """
    if version is None:
        installed_versions = get_installed_versions(dirname=dirname)
        if installed_versions:
            version = installed_versions[0]
        else:
            version, _ = install(version=None, dirname=dirname)

    if check_for_latest:
        latest_version = get_latest_version()
        versions = natsort.natsorted([version, latest_version])
        if versions[-1] != version:
            version, _ = install(version=latest_version, dirname=dirname)

    filename = get_installation_filename(version, dirname=dirname)
    return read_ontology(filename)


def get_term_ids(terms):
    """ Get the ids of a list of KiSAO terms

    Args:
        terms (:obj:`list` of :obj:`pronto.Term`): terms

    Returns:
        :obj:`list` of :obj:`str`: ids of the terms
    """
    return [term.id.partition('#')[2] for term in terms]


__ontology = None


def get(dirname=None):
    """ Get the KiSAO ontology

    Args:
        dirname (:obj:`str`, optional): path where KiSAO is/should be installed. Default: use
            the path managed by BioSimulators utils

    Returns:
        :obj:`pronto.Ontology`: ontology
    """
    module = globals()

    if module['__ontology'] is None:
        module['__ontology'] = load(dirname=dirname)

    return module['__ontology']


def get_term(id, dirname=None):
    """ Get a term in the ontology

    Args:
        id (:obj:`str`): id of the term (e.g., ``KISAO_0000019``)
        dirname (:obj:`str`, optional): path where KiSAO is/should be installed. Default: use
            the path managed by BioSimulators utils

    Returns:
        :obj:`pronto.Term`: term
    """
    return get(dirname=dirname)[NAMESPACE + id]


def get_child_terms(id, dirname=None):
    """ Get the child terms of a term in the ontology

    Args:
        id (:obj:`str`): id of the term (e.g., ``KISAO_0000019``)
        dirname (:obj:`str`, optional): path where KiSAO is/should be installed. Default: use
            the path managed by BioSimulators utils

    Returns:
        :obj:`list` of :obj:`pronto.Term`: child terms
    """
    return list(get_term(id, dirname=dirname).subclasses())[1:]


def get_parent_terms(id, dirname=None):
    """ Get the parent terms of a term in the ontology

    Args:
        id (:obj:`str`): id of the term (e.g., ``KISAO_0000019``)
        dirname (:obj:`str`, optional): path where KiSAO is/should be installed. Default: use
            the path managed by BioSimulators utils

    Returns:
        :obj:`list` of :obj:`pronto.Term`: parent terms
    """
    return list(get_term(id, dirname=dirname).superclasses())[1:]
