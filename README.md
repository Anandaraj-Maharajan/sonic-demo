# SONiC Custom Minigraphs

## Description
This repo is used to generate & deploy custom minigraph configurations for 
devices running SONiC

## Usage
ansible-playbook generate_config.yml -e topology=t1/t1-lag -e platform=Z9100
ansible-playbook deploy.yml -i hosts

## Ansible folder tree

--- deploy.yml

|-- generate_config.yml

|-- group_vars

|       |-- Z9100.yml                      # Add more platform files in this location

|-- hosts                                  # inventory file

|-- minigraph                              # Minigraph output file location

|   |-- T0-1.xml

|   |-- T0-2.xml

|   |-- T1-1.xml

|   |-- T1-2.xml

|-- roles

     |-- clos

        |-- tasks

        |   |-- main.yml                  # Update this file according to the additional platforms added

        |-- templates

        |   |-- cpg.j2

        |   |-- device.j2

        |   |-- dpg.j2

        |   |-- meta.j2

        |   |-- minigraph.j2

        |   |-- png.j2

        |-- vars

            |-- pod.yml              # Change this file according to physical topology

            |-- T0-28D-4U.yml        # Variables related to the given topology

