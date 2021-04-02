restart=""
while true; do
    timeout 3600 python3 /mnt/device/script.py $restart
    restart="restart"
done &
