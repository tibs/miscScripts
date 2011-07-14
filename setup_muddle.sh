# Set up the aliases used to run muddle
# (using aliases means I don't have to change my PATH)
#
# Obviously, use ``source ${HOME}/bin/setup_muddle.sh`` to use this,
# so that it amends the *actual* environment of the runnng shell...


##export PATH=$PATH:${HOME}/sw/muddle
##export PYTHONPATH=${PYTHONPATH}:${HOME}/sw/muddle

# This is normally a soft link to ~/sw/muddle.svn/trunk/muddle
MY_MUDDLE_DIR=${HOME}/sw/muddle

alias muddle="python ${MY_MUDDLE_DIR}/muddled/"
# m3 is my experimental version of muddle...
#alias m3='python /home/tibs/sw/muddle.svn/branches/new_vcs/muddle/muddled/'
# But sometimes it is just another name for the mainstream...
alias m3="python ${MY_MUDDLE_DIR}/muddled/"

alias visdep="${MY_MUDDLE_DIR}/sandbox/visdep.py"

