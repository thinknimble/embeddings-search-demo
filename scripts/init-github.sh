#!/bin/bash

#
# Creating vector_demonstration git repo
#
git init
git add .
git commit -m "Initial commit"
# git remote add origin git@github.com:thinknimble/vector_demonstration.git
gh repo create thinknimble/vector_demonstration --private -y
git push origin main
printf "\033[0;32mRepo https://github.com/thinknimble/vector_demonstration/\033[0m \n"
