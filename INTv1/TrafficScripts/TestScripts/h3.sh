sleep 0.5

hping3 -q -c 20 -i u185000 --keep 10.0.0.4
sleep 0.5

hping3 -q -c 10 -i u15000 --keep 10.0.0.4
sleep 2
hping3 -q -c 5 -i u5000 --keep 10.0.0.6
sleep 2

timeout 0.073 hping3 -S --flood -p 80 --spoof 69.0.0.1 10.0.0.2 &

hping3 -q -c 10 -i u2500 --keep 10.0.0.2
sleep 3

hping3 -q -c 100 -i u85000 --keep 10.0.0.2
sleep 2