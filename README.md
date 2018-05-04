# SONiC Custom Minigraphs

## Description
This repo is used to generate & deploy custom minigraph configurations for 
devices running SONiC

## Usage
ansible-playbook generate_config.yml -e topology=t1/t1-lag -e platform=Z9100
ansible-playbook deploy.yml -i hosts

## Ansible folder tree
sonic-demo
|____deploy.yml
|____generate_config.yml
|____.gitlab-ci.yml
|____minigraph
| |____T0-2.xml
| |____T1-2.xml
| |____T0-1.xml
| |____T1-1.xml
|____README.md
|____roles
| |____clos
| | |____templates
| | | |____minigraph.j2
| | | |____device.j2
| | | |____png.j2
| | | |____meta.j2
| | | |____cpg.j2
| | | |____dpg.j2
| | |____vars
| | | |____32portlayout.yml
| | | |____64portlayout.yml
| | | |____main.yml
| | |____tasks
| | | |____main.yml
|____group_vars
| |____S6100.yml
| |____Z9100.yml
|____hosts
