# SONiC Custom Minigraphs

# Description
This repo is used to generate & deploy custom minigraph configurations for devices running SONiC

## Usage
ansible-playbook generate_config.yml -e topology=t1/t1-lag -e platform=Z9100

--- deploy.yml
|-- generate_config.yml
|-- group_vars
|   |-- Z9100.yml
|-- hosts
|-- minigraph
|   |-- T0-1.xml
|   |-- T0-2.xml
|   |-- T1-1.xml
|   |-- T1-2.xml
|-- roles
    |-- clos
        |-- tasks
        |   |-- main.yml
        |-- templates
        |   |-- cpg.j2
        |   |-- device.j2
        |   |-- dpg.j2
        |   |-- meta.j2
        |   |-- minigraph.j2
        |   |-- png.j2
        |-- vars
            |-- pod.yml
            |-- T0-28D-4U.yml
            |-- Z9100.yml

