import os
import shutil
from .logger import log, mywarn, myerror, check_exists, mkdir, run_cmd
from os.path import join

usage = '''This script helps you to download the arxiv paper, 
basic usage: 
'''

def check_url(url):
    if url.startswith('https'):
        paperid = url.rstrip('.pdf').split('/')[-1]
    elif len(url) == 10:
        paperid = url
    log('[Zero] paper id = {}'.format(paperid))
    return paperid

def try_to_download_paper(database, url):
    dirname = join(database, url)
    mkdir(dirname, verbose=False)
    pdfname = join(dirname, f'{url}.pdf')
    # TODO:判断下载了的版本与最新的版本
    if not check_exists(pdfname):
        cmd = 'curl https://arxiv.org/pdf/{}.pdf --output {}'.format(url, pdfname)
        run_cmd(cmd)
    tarname = join(dirname, f'{url}.tar.gz')
    if not check_exists(tarname):
        cmd = 'curl https://arxiv.org/e-print/{} --output {}'.format(url, tarname)
        run_cmd(cmd)
    sourcename = join(dirname, 'source')
    if not check_exists(sourcename):
        mkdir(sourcename, verbose=False)
        cmd = f'tar -xzf {tarname} -C {sourcename}'
        run_cmd(cmd)

def cli():
    import argparse
    parser = argparse.ArgumentParser(
        usage=usage)
    parser.add_argument('url', type=str, help='input the url link')
    parser.add_argument('comments', type=str, help='comments about this paper, seperated by `/`')
    parser.add_argument('--database', type=str, default=f"{os.environ['HOME']}/myzero",
        help='Path to database to store the files.')
    args = parser.parse_args()

    database = os.path.abspath(args.database)
    comments = args.comments.split('!')

    if not check_exists(database):
        mkdir(database, verbose=False)
    logname = join(database, 'cmd.log')
    url = check_url(args.url)
    if not check_exists(logname):
        with open(logname, 'w') as f:
            f.write('# zero log\n')
    with open(logname, 'a') as f:
        f.write('zero {} {}\n'.format(url, args.comments))
    log('[Zero] ' + ', '.join(comments))
    try_to_download_paper(database, url)

def find():
    import argparse
    parser = argparse.ArgumentParser(
        usage=usage)
    parser.add_argument('keywords', type=str, help='input the url link', nargs='+')
    parser.add_argument('--database', type=str, default=f"{os.environ['HOME']}/myzero",
        help='Path to database to store the files.')
    args = parser.parse_args()

    comments = args.keywords
    log('[Zero] Try to find' + ', '.join(comments))

def clean_compile_arxiv():
    import argparse
    parser = argparse.ArgumentParser(
        usage=usage)
    parser.add_argument('url', type=str, help='input the url link')
    args = parser.parse_args()

    log('[Zero] Clean tmp, tmp_arXiv')
    for path in ['tmp', 'tmp_arXiv', 'Source']:
        if os.path.exists(path):
            shutil.rmtree(path)
    log('[Zero] Clone {}'.format(args.url))

    cmd = 'git clone {} tmp'.format(args.url)
    run_cmd(cmd)
    cmd = 'arxiv_latex_cleaner ./tmp --keep_bib --verbose'
    run_cmd(cmd)
    shutil.copytree('tmp_arXiv', 'Source')
    # cmd = 'cd tmp_arXiv && '
    cmd = 'zip -r siggraph22conferenceproceedings-10.zip ./Source'
    run_cmd(cmd)