/^ipvar HOME_NET any$/i\
## SWE ## Smoothwall maintains HOME_NET and DNS_SERVERS in /etc/snort/vars\
include /etc/snort/vars\
# ipvar HOME_NET any
/^ipvar HOME_NET any$/d

/^ipvar DNS_SERVERS/i\
## SWE ## Smoothwall maintains HOME_NET and DNS_SERVERS in /etc/snort/vars\
# ipvar DNS_SERVERS $HOME_NET
/^ipvar DNS_SERVERS/d

/^portvar SSH_PORTS 22$/i\
## SWE ## Smoothwall uses port 222 for ssh so watch it and 22\
portvar SSH_PORTS [22,222]
/^portvar SSH_PORTS 22$/d

/^var RULE_PATH ..\/rules$/i\
## SWE ## Snort is based in /var/smoothwall/snort so base rule path vars from there\
var SNORT_HOME /var/smoothwall/snort\
var RULE_PATH $SNORT_HOME/rules\
var SO_RULE_PATH $SNORT_HOME/so_rules\
var PREPROC_RULE_PATH $SNORT_HOME/preproc_rules
/^var RULE_PATH ..\/rules$/,+2d

/^var WHITE_LIST_PATH ..\/rules$/i\
# Currently there is a bug with relative paths, they are relative to where snort is\
# not relative to snort.conf like the above variables\
# This is completely inconsistent with how other vars work, BUG 89986\
# Set the absolute path appropriately\
## SWE ## Smoothwall stores these in $SNORT_HOME/reputation_lists\
var WHITE_LIST_PATH $SNORT_HOME/reputation_lists\
var BLACK_LIST_PATH $SNORT_HOME/reputation_lists
/^var WHITE_LIST_PATH ..\/rules$/,+1d

/^dynamicpreprocessor directory.*local/i\
## SWE ## Smoothwall places these in /usr/lib instead of /usr/local/lib\
dynamicpreprocessor directory /usr/lib/snort_dynamicpreprocessor
/^dynamicpreprocessor directory.*local/d

/^dynamicengine.*local/i\
## SWE ## Smoothwall places these in /usr/lib instead of /usr/local/lib\
dynamicengine /usr/lib/snort_dynamicengine/libsf_engine.so
/^dynamicengine.*local/d

/^dynamicdetection directory.*local/i\
## SWE ## Smoothwall places these in /usr/lib instead of /usr/local/lib\
## SWE ## This controls if the SO rules are loaded or not\
#dynamicdetection directory /usr/lib/snort_dynamicrules
/^dynamicdetection directory.*local/d

/^preprocessor http_inspect: /i\
## SWE ## Smoothwall places the unicode.map in the $SNORT_HOME directory
/^preprocessor http_inspect: /s= unicode.map = $SNORT_HOME/unicode.map =

/^preprocessor ssh: server_ports { 22/i\
## SWE ## Smoothwall uses port 222 for ssh so watch it and 22
/^preprocessor ssh: server_ports { 22/s=22=22 222=

s/white_list.rules/white.list/

s/black_list.rules/black.list/

/classification.config/i\
## SWE ## Smoothwall stores these in the $SNORT_HOME directory
s=classification.config=$SNORT_HOME/classification.config=

s=reference.config=$SNORT_HOME/reference.config=
