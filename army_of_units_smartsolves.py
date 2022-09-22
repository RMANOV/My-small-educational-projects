number = int(input().strip())

few = 1
pack = 10
horde = 50
swarm = 500
legion = 1000
units = legion, swarm, horde, pack, few
names = "legion", "swarm", "horde", "pack", "few"
answer = "no army"
counter = 0

for unit in units:
    if number >= unit:
        answer = names[counter]
        break
    counter += 1

print(answer)