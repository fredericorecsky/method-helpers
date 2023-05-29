#!/usr/bin/env python3
"""Read the structure of directory and generate a git_ignore"""

import logging
import os 
from pathlib import Path

import frontmatter


logging.basicConfig(level=logging.INFO)

def process_front_matter( filename ):
    """Get a file, loads it front-matter and return the sync value from it. 

    Args: filename

    return: Sync value
    """

    sync = None
    if os.path.exists( filename ) and os.path.isfile( filename ):
        logging.debug( "Processing {}".format( filename ))

        with open( filename ) as fh:
            file = frontmatter.load( fh )   

            if 'sync' in file:
                logging.debug( "\tsync:{}".format( file['sync']))
                sync = file['sync']

    return sync

def prep_gitignore(target_dir, lvl=0, results=None):
    """Will scan all the directories on 1st level of the Method and generate a 
    gitignore tailored for this. 

    Args: method_dir : root of the Projects
    results: dic to upkeep the key founds
    """

    logging.debug( "> lvl{}-{}".format( lvl, target_dir ))

    if lvl > 3:
        logging.debug( "Dropping here {}".format(target_dir ))
        return results

    if lvl < 1:
        if not results:
            results = {}
    else:
        logging.debug( "Added {} to results ".format(target_dir))
        results[str(Path(target_dir))] = []
    
    lvl += 1
    for item in Path(target_dir).glob("*"):
        logging.debug( "lvl{}-{}".format( lvl, item ))
        if item.is_file():
            dirname = os.path.dirname( item )
            filename = os.path.basename( item )
            if filename == "README.md":
                logging.debug("Found README.md")
                sync = process_front_matter(item)
                logging.debug( "Sync {} for {}".format(sync, dirname))
                if sync and sync == "method_git":
                    logging.info( "This {} will be allowed list on git".format( dirname ) )
                    results[dirname].append( True )
                    # Add the external directory of this to the git_ignore
                    external_dir = os.path.join( dirname, 'external')
                    results[external_dir] = []
                else:
                    logging.debug( "Let's ignore this {} ".format( item ))

                # Read the file to find sync on frontmatter
            logging.debug( "Ignoring {} as it is a file".format( item ) )
        else:
            logging.debug( "Directory: {}".format(item))
            prep_gitignore( item, lvl, results )
    
    return results

def generate_git_ignore( structure, method_dir ):
    """Receives a dict with a list of sync directories to generate a gitignore

    returns a gitignore array to be written as file
    """

    git_ignore = []
    for path in structure.keys():
        if len(structure[path]) > 0:
            logging.debug( "Will allow {}".format( path ))
            # under this directory, exclude the external 
        else:
            logging.debug( "This will be added to ignore list {}".format( path ))
            git_dir = path.replace(method_dir + '/', '')
            git_ignore.append( git_dir )

    return git_ignore

def update_git_ignore( contents, method_dir):
    git_ignore = os.path.join( method_dir, '.gitignore' )
    logging.info( "Saving git ignore to:{}".format( git_ignore ))
    with open( git_ignore, mode='w') as fh:
        for line in contents:
            print( line, file=fh)


base_dir = os.path.normpath( os.path.dirname( os.path.realpath(__file__)) )
method_dir_components = base_dir.split( os.sep )[0:-3]
method_dir = os.path.join( '/', *method_dir_components )

logging.info( "Method directory: {}".format( method_dir ))

git_ignore = generate_git_ignore( prep_gitignore( method_dir), method_dir )

update_git_ignore( git_ignore, method_dir)
