#!/usr/bin/env python3

# Script to make conversion to bids
# Chris Cheng 2018

import pydicom
import re


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
    for filename in files:
       convert_tarball(filename)
