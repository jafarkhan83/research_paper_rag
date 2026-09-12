from parser import initializer
from chunking import parent_child_chunking

sections = initializer("papers/paper.pdf")
# parent, child = parent_child_chunking(sections)

for section in sections:
    print(section, end='\n\n')

# for p in parent:
#     print(p)

# print('\n\n')

# for c in child:
#     print(c)
