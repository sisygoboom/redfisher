# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 22:28:50 2019

@author: chris
"""

from beem.blockchain import Blockchain
from beem.nodelist import NodeList
from beem.account import Account
from beem import Steem
from datetime import datetime, timedelta
import time
import threading
import click

######
# TODO gauge voting and commenting
# make account checks quicker
######

n = NodeList()
nodes = n.get_nodes()
s = Steem(nodes)
b = Blockchain(s)

@click.command()
@click.option(
        '--weeks',
        default=1,
        help='How many days worth of global posts we should be looking through'
        )
@click.option(
        '--posts_per_week',
        default=2,
        help='The minimum number of times the accounts should post per week'
        )
@click.option(
        '--min_sp',
        default=60,
        help='The highest steem power an account can have to be considered'
        )
def redfisher(
        weeks,
        posts_per_week,
        min_sp):
    """
    Streams through all posts within given timeframe and sends accounts to be 
    validated.
    """
    
    t1 = time.process_time()
    
    # calculate the start block based on how many weeks the user selected
    now = datetime.now()
    start_date = now - timedelta(days=weeks*7)
    start_block = b.get_estimated_block_num(start_date)
    
    # stream comments from start block to current block
    user_list = list()
    for post in b.stream(
            opNames=['comment'],
            start=start_block,
            stop=b.get_current_block_num()
            ):
        # assure that the post is not a comment
        if post['parent_author'] == '':
            # assure the user hasn't been checked before
            if post['author'] not in user_list:
                # start a thread to check the user meets requirements
                t = threading.Thread(
                        target=check,
                        args=(post['author'], min_sp, weeks, posts_per_week))
                t.start()
                # add user to list so they can't be checked again
                user_list.append(post['author'])
    
    time.sleep(1)
    t2 = time.process_time()
    print(t2-t1)
    
def check(user, min_sp, weeks, posts_per_week):
    """
    Check that the users meet the requirements.
    """
    while True:
        try:
            acc = Account(user)
            sp = acc.get_steem_power()
            
            if sp <= min_sp:
                count = post_check(acc)
                        
                if count >= posts_per_week:
                    powered_up, powered_down = vest_check(acc)
                    
                    if powered_up and not powered_down:
                        # all checks completed
                        click.echo(user + " " + str(round(sp,3)))
            break
        except:
            failover()
                
def vest_check(acc):
    # get all time powerup and powerdown history
    vest_history = acc.history(
            only_ops=['withdraw_vesting','transfer_to_vesting']
            )
    # check for powerups and powerdowns
    powered_up = False
    powered_down = False
    for change in vest_history:
        if change['type'] == 'withdraw_vesting':
            powered_down = True
        if change['type'] == 'transfer_to_vesting':
            powered_up = True
    return powered_up, powered_down

def post_check(acc):
    t1 = time.process_time()
    # get datetime oject for a week ago
    posts_from = datetime.now() - timedelta(days=7)
    # get comment history for the last week
    post_history = acc.history(start=posts_from, only_ops=['comment'])
    # count how amny posts they made in the last week
    count = 0
    for post in post_history:
        if post['parent_author'] == acc.name:
            count += 1
    t2 = time.process_time()
    #print(t2-t1)
    return count

def failover():
    global nodes
    nodes = nodes[1:] + [nodes[0]]
                
if __name__ == '__main__':
    redfisher()