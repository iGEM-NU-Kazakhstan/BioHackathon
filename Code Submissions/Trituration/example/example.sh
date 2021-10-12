#!/bin/bash

restriction_sites_hider.py find_by_pattern ./NC_005816.fna AGCCAG test_sites_hider_by_pattern.txt
restriction_sites_hider.py remove_by_pattern ./NC_005816.fna test_sites_hider_by_pattern.txt AGCCAG NC_005816_pattern.fa


restriction_sites_hider.py find_known_sites ./NC_005816.fna BamHI test_sites_hider_known_sites.txt
restriction_sites_hider.py remove_known_sites ./NC_005816.fna test_sites_hider_known_sites.txt BamHI NC_005816_known_sites.fa
