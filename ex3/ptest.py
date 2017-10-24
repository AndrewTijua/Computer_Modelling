from Particle3D import Particle3D as p3d

file = open('my_butt.txt', 'r')
bums = p3d.make_from_file(file)
print(bums.__str__())
file.close()
