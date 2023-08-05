import pkgutil
import inspect
import logging as log
from .test import Test, ScanTest, ExperimentTest


def __get_modules__(m):
    modules = []
    prefix = m.__name__ + '.'
    log.info('prefix : %s' % prefix)
    for importer, modname, ispkg in pkgutil.iter_modules(m.__path__, prefix):
        module = __import__(modname, fromlist='dummy')
        if not ispkg:
            modules.append(module)
        else:
            modules.extend(__get_modules__(module))
    return modules


def __find_all_checks__(m):
    """ Browses bbrc.validation and looks for any class inheriting from Test"""
    modules = []
    classes = []
    modules = __get_modules__(m)
    forbidden_classes = [Test, ScanTest, ExperimentTest]
    for m in modules:
        for name, obj in inspect.getmembers(m):
            if inspect.isclass(obj) and Test in obj.mro() \
                    and obj not in forbidden_classes:
                classes.append(obj)
    return classes


def __md5__(fname):
    import hashlib
    hash_md5 = hashlib.md5()
    if fname.endswith('.pyc'):
        fname = fname[:-1]
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def __is_valid_scan__(xnat_instance, scan):
    """ Determines if a given scan is usable.
    Quality flag should be `usable` and ID should not start with 0.

    Args:
        scan: should be a dict eg. as returned by
                Interface.array.scans(columns=['xnat:imageScanData/quality',
                                               'xnat:imageScanData/type',
                                               'xsiType'])."""

    import fnmatch
    prefix = [i.split('/')[0] for i in scan.keys()
              if fnmatch.fnmatch(i, '*scandata/id')][0]
    if not prefix:
        raise Exception

    sc = scan['%s/id' % prefix]
    quality = scan['%s/quality' % prefix]
    datatype = xnat_instance.select.experiment(scan['ID']).scan(sc).datatype()
    columns = ['xnat:mrScanData', 'xnat:petScanData', 'xnat:ctScanData']

    valid = (sc.isdigit() and not sc.startswith('0') and quality == 'usable'
             and datatype in columns)

    return valid


def collect_reports(xnat_instance, validator_name='ArchivingValidator',
                    project=None):
    import json

    url = '/data/experiments/%s/resources/BBRC_VALIDATOR/files/%s'
    if project:
        projects = [project]
    else:
        projects = list(xnat_instance.select.projects().get())
    reports = {}

    for p in projects:
        subjects = xnat_instance.select.project(p).subjects().get()

        for s in subjects:
            columns = ['ID', 'label', 'xsiType']
            exp_id = xnat_instance.array.experiments(subject_id=s,
                                                     columns=columns).data
            experiments = [(val['ID'], val['label']) for val in exp_id]
            for eid, e in experiments:
                uri = url % (eid, '%s_%s.json' % (validator_name, e))
                try:
                    reports[eid] = json.loads(xnat_instance.get(uri).text)
                except Exception:
                    pass
    return reports
