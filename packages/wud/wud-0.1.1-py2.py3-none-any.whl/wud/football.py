#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 18:08:49 2021

@author: nattawoot
"""
import copy
from collections import namedtuple
from wud.aws import s3bucket_json_get

convar_dict = s3bucket_json_get('wud-cloudhouse','maruball_convar.json')

def team_name_revise(team, source_input, source_output):
    
    
    epl = copy.deepcopy(convar_dict['team_name']['epl'])
    ucl_erp = copy.deepcopy(convar_dict['team_name']['ucl_erp'])
    tpl = copy.deepcopy(convar_dict['team_name']['tpl'])
    etc = copy.deepcopy(convar_dict['team_name']['etc'])

    Team = namedtuple("Team", ['footballapi', 'livescore', 'shortname', 'league'])   

    
    
    team_set = []
    for t in epl:
        t.append('epl')
        team_set.append(Team(*t))
    for t in ucl_erp:
        t.append('ucl_erp')
        team_set.append(Team(*t))
        
    for t in tpl:
        t.append('tpl')
        team_set.append(Team(*t))
        
    for t in etc:
        t.append('etc')
        team_set.append(Team(*t))
        
        
    result = team
    
    for i in team_set:
        if getattr(i, source_input) == team:
            result = getattr(i, source_output)
            break
        
    return result
       
