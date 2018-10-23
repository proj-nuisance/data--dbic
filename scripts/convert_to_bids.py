#!/usr/bin/env python3

# Script to make conversion to bids
# Chris Cheng 2018

import pydicom
import re
from optparse import OptionParser, Option


def get_opt_parser():
    # use module docstring for help output
    p = OptionParser()

    p.add_options([
        Option("-p", "--placeholder",
               dest="hopa", default="leaving room for future options to be added",
               help="out of order"),

    ])

    return p


def run_command(cmd):
    print(cmd)
    # later -- actually run it


def get_date_from_dicom_tarball(filename):
    dataset = pydicom.dcmread(filename)
    date = dataset.StudyDate

    return date


def get_sid_form_filename(filename):
    # e.g. for Haxby/Sam/1021_actions/sourcedata/sub-sid000416/ses-raiders/anat/sub-sid000416_ses-raiders_T2w.dicom.tgz
    # it would be  sid000416
    sid = re.search('.*/sub-(?P<sid>sid\d+)/.*', filename)

    return sid.group('sid')


def convert_tarball(filename):
    date = get_date_from_dicom_tarball(filename)
    subjid = get_sid_from_filename(filename)
    # run the command which does conversion
    run_command('heudiconv --bids -f reproin -s {} -ss {} --files {}'.format(subjid, date, filename))

if __name__ == '__main__':
    parser = get_opt_parser()

    (options, files) = parser.parse_args(args)

    for filename in files:
        convert_tarball(filename)
