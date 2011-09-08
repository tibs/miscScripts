# Set up the aliases used to run muddle
# (using aliases means I don't have to change my PATH)
#
# Obviously, use ``source ${HOME}/bin/setup_muddle.sh`` to use this,
# so that it amends the *actual* environment of the runnng shell...


##export PATH=$PATH:${HOME}/sw/muddle
##export PYTHONPATH=${PYTHONPATH}:${HOME}/sw/muddle

# This is normally a soft link to ~/sw/muddle.svn/trunk/muddle
MY_MUDDLE_DIR=${HOME}/sw/muddle
MY_M3_DIR=${HOME}/sw/m3

# This is a reference to the "normal" version of muddle. I expect this to
# always be set to the master branch
alias muddle="python ${MY_MUDDLE_DIR}/muddled/"

# m3 is my experimental version of muddle...
# It may be set to master, or to any other branch
alias m3="python ${MY_M3_DIR}/muddled/"

# visdep get to use the safe muddle...
alias visdep="${MY_MUDDLE_DIR}/sandbox/visdep.py"

