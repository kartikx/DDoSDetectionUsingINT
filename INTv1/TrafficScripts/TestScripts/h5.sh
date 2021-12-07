hping3 -q -c 30 -i u200000 --keep 10.0.0.6
sleep 0.7

hping3 -q -c 50 -i u125000 --keep 10.0.0.4

hping3 -q -c 25 -i u100 --keep 10.0.0.2
sleep 2
hping3 -q -c 15 -i u1000 --keep 10.0.0.4
sleep 2

timeout 0.073 hping3 -S --flood -p 80 --spoof 69.0.0.1 10.0.0.2 &
