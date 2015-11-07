from fabric.api import local, run, env, put
import os, time
import urllib, urllib2, json
import sys

for arg in sys.argv:
    print arg

env.port = 22
env.use_ssh_config = False
# remote ssh credentials
env.host_string = 'navyug@192.168.3.223'
env.user = 'navyug'
env.password = 'new life' #ssh password for user
# or, specify path to server public key here:
#env.key_filename="/home/jigserv/.ssh/id_rsa.pub"
env.no_keys = True 
# specify path to files being deployed
env.archive_source = '.'
 
# archive name, arbitrary, and only for transport
env.archive_name = 'release'
 
# specify path to deploy root dir - you need to create this
env.deploy_project_root = '/home/navyug/'
 
# specify name of dir that will hold all deployed code
env.deploy_release_dir = 'releases'
 
# symlink name. Full path to deployed code is env.deploy_project_root + this
env.deploy_current_dir = 'current'

TOKEN="0b3fad910b1e253f8c624163e51873bdcb35744a"
user = "TheExorcist"
project = "game-of-life-in-python"


[ {
  "path" : "/tmp/circle-artifacts.8tQFahZ/game-of-life-in-python.tar.gz",
  "pretty_path" : "$CIRCLE_ARTIFACTS/game-of-life-in-python.tar.gz",
  "node_index" : 0,
  "url" : "https://circle-artifacts.com/gh/TheExorcist/game-of-life-in-python/27/artifacts/0/tmp/circle-artifacts.8tQFahZ/game-of-life-in-python.tar.gz"
} ]
 
def update_local_copy():
    #get latest / desired tag from your version control system

    run("whoami")
    print('updating local copy...')
    request = urllib2.Request('https://circleci.com/api/v1/project/TheExorcist/game-of-life-in-python/27/artifacts?\
    circle-token=0b3fad910b1e253f8c624163e51873bdcb35744a', headers={"accept": "application/json"})
    response = urllib2.urlopen(request) 
    response_data = json.load(response)
    


def upload_archive(build_num=0):

    print('updating local copy...')

    request = urllib2.Request('https://circleci.com/api/v1/project/TheExorcist/game-of-life-in-python/{0}/artifacts?\
    circle-token=0b3fad910b1e253f8c624163e51873bdcb35744a'.format(build_num), headers={"accept": "application/json"})

    response = urllib2.urlopen(request) 
    response_data = json.load(response)
    artifact= urllib2.urlopen(response_data[0]['url']).read()
    f=open('artifact.tar.gz', 'w')
    f.write(artifact)

    #create time named dir in deploy dir
    print('uploading archive...')
    deploy_timestring = time.strftime("%Y%m%d%H%M%S")
    run('mkdir -p /home/navyug/releases')
    run('cd %s && mkdir %s' % (env.deploy_project_root + \
        env.deploy_release_dir, deploy_timestring))
 
    #extract code into dir
    print('extracting code...')
    env.deploy_full_path = env.deploy_project_root + \
        env.deploy_release_dir + '/' + deploy_timestring
    print "uploading"
    put("artifact.tar.gz", env.deploy_full_path)
    #run('cd %s && unzip -q %s.zip -d . && rm %s.zip' \
    #    % (env.deploy_full_path, env.archive_name, env.archive_name))
 
def before_symlink():
    # code is uploaded, but not live. Perform final pre-deploy tasks here
    print('before symlink tasks...')
 
def make_symlink():
    # delete existing symlink & replace with symlink to deploy_timestring dir
    print('creating symlink to uploaded code...')
    run('rm -f %s' % env.deploy_project_root + env.deploy_current_dir)
    run('ln -s %s %s' % (env.deploy_full_path, env.deploy_project_root + \
        env.deploy_current_dir))
 
def after_symlink():
    # code is live, perform any post-deploy tasks here
    print('after symlink tasks...')
 
def cleanup():
    # remove any artifacts of the deploy process
    print('cleanup...')
    local('rm -rf %s.zip' % env.archive_name)
 
def deploy():
    update_local_copy()
    '''
    upload_archive()
    before_symlink()
    make_symlink()
    after_symlink()
    cleanup()
    '''
    print('deploy complete!')

