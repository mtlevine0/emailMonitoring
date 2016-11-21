# Dynamically load properties 

d = {}
with open('properties.txt') as f:
    for line in f:
        if line[0] != '#' and line[0] != '\n':
            key, value = line.split('=')
            d[key] = value.strip('\n')