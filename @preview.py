import os

os.system('python @prepare.py')
os.system('hexo clean')
os.system('hexo g')
os.system('hexo s')