#!/bin/bash

seconds=$1
# Do something
printf "%02d:%02d:%02d" $(( $seconds / 3600 )) $(( $seconds / 60 % 60 )) $(( $seconds % 60 ))

_____________________________________
#!/bin/bash

seconds=$1

((hours=${1}/3600))
((minutes=${1}%3600/60))
((secs=${1}%60))

printf "%02d:%02d:%02d\n" $hours $minutes $secs

_____________________________________
#!/bin/bash

seconds=$1
# Do something
hour=`echo "$seconds/3600" |bc`
min=`echo "($seconds - $hour*3600)/60" |bc`
sec=`echo "$seconds%60" |bc`
result=`awk -F"+" -v var_h=$hour -v var_min=$min -v var_sec=$sec '
BEGIN{
printf("%02d:%02d:%02d", var_h, var_min, var_sec)
}'`

echo $result

_____________________________________
#!/bin/bash

seconds=$1
printf '%02d:%02d:%02d\n' $((seconds/3600)) $((seconds%3600/60)) $((seconds%60))
_____________________________________
seconds=$1
# Do something
sec=$((seconds%60))
min=$(((seconds/60)%60))
hour=$((seconds/60/60))
seconds=$(printf "%02d:%02d:%02d" $hour $min $sec)
echo $seconds
