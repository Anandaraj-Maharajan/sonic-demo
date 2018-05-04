# SONiC Custom Minigraphs

## Description
This repo is used to generate & deploy custom minigraph configurations for 
devices running SONiC

## Usage
ansible-playbook generate_config.yml -e topology=t1/t1-lag -e platform=Z9100
ansible-playbook deploy.yml -i hosts

## Ansible folder tree
sonic-demo

    deploy.yml
    
    generate_config.yml
    
    .gitlab-ci.yml
    
    minigraph
    
    	T0-2.xml
    
    	T1-2.xml
    
    	T0-1.xml
    
    	T1-1.xml
    
    README.md
    
    roles
    
    	clos
    
    		templates
    
    			minigraph.j2
    
    			device.j2
    
    			png.j2
    
    			meta.j2
    
    			cpg.j2
    
    			dpg.j2
    
    		vars
    
    			32portlayout.yml
    
    			64portlayout.yml
    
    			main.yml
    
    		tasks
    
    			main.yml
    group_vars
    
    	S6100.yml
    
    	Z9100.yml
    
    hosts