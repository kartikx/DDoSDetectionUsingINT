echo "Long 1"
hping3 -q -c 30 -i u200000 --keep 10.0.0.6
sleep 0.7
hping3 -q -c 15 -i u80000 --keep 10.0.0.2
sleep 0.5
hping3 -q -c 50 -i u125000 --keep 10.0.0.4

echo "Quick 1"
hping3 -q -c 25 -i u100 --keep 10.0.0.2
sleep 2
hping3 -q -c 15 -i u1000 --keep 10.0.0.4
sleep 2
hping3 -q -c 5 -i u1500 --keep 10.0.0.6
sleep 2
hping3 -q -c 25 -i u1500 --keep 10.0.0.4
sleep 2
hping3 -q -c 5 -i u1250 --keep 10.0.0.2
sleep 3
hping3 -q -c 10 -i u3000 --keep 10.0.0.4
sleep 2

echo "Quick 2"
hping3 -q -c 5 -i u2250 --keep 10.0.0.4
sleep 2.2
hping3 -q -c 10 -i u5500 --keep 10.0.0.2
sleep 3.5
hping3 -q -c 20 -i u100 --keep 10.0.0.6
sleep 2
hping3 -q -c 10 -i u2500 --keep 10.0.0.6
sleep 2
hping3 -q -c 5 -i u5000 --keep 10.0.0.2
sleep 2
hping3 -q -c 10 -i u1250 --keep 10.0.0.4
sleep 3
hping3 -q -c 15 -i u1000 --keep 10.0.0.6
sleep 2

echo "Long 2"
hping3 -q -c 50 -i u50000 --keep 10.0.0.4
sleep 2.5
hping3 -q -c 55 -i u65000 --keep 10.0.0.6
sleep 0.8
hping3 -q -c 40 -i u45000 --keep 10.0.0.2

echo "Long 3"
hping3 -q -c 10 -i u125000 --keep 10.0.0.4
sleep 1.8
hping3 -q -c 55 -i u65000 --keep 10.0.0.6
sleep 1.5
hping3 -q -c 90 -i u125000 --keep 10.0.0.2

echo "Quick 3"
hping3 -q -c 5 -i u2250 --keep 10.0.0.4
sleep 2.2
hping3 -q -c 10 -i u5500 --keep 10.0.0.2
sleep 3.5
hping3 -q -c 20 -i u100 --keep 10.0.0.6
sleep 2
hping3 -q -c 10 -i u2500 --keep 10.0.0.6
sleep 2
hping3 -q -c 5 -i u5000 --keep 10.0.0.2
sleep 2
hping3 -q -c 10 -i u1250 --keep 10.0.0.4
sleep 3
hping3 -q -c 15 -i u1000 --keep 10.0.0.6
sleep 2

echo "Waiting to Flush, press a key when ready"
read temp

echo "Starting next Batch"

echo "Long 4"
hping3 -q -c 20 -i u35000 --keep 10.0.0.6
sleep 0.2
hping3 -q -c 45 -i u40000 --keep 10.0.0.4
sleep 1.5
hping3 -q -c 60 -i u50000 --keep 10.0.0.4

echo "Long 5"
hping3 -q -c 50 -i u50000 --keep 10.0.0.4
sleep 2.5
hping3 -q -c 55 -i u65000 --keep 10.0.0.6
sleep 0.8
hping3 -q -c 40 -i u45000 --keep 10.0.0.2

echo "Attack started"
timeout 0.073 hping3 -q -S --flood -p 80 --spoof 69.0.0.5 10.0.0.4 &

echo "Quick 4"
hping3 -q -c 25 -i u100 --keep 10.0.0.2
sleep 2
hping3 -q -c 15 -i u1000 --keep 10.0.0.4
sleep 2
hping3 -q -c 5 -i u1500 --keep 10.0.0.6
sleep 2
hping3 -q -c 25 -i u1500 --keep 10.0.0.4
sleep 2
hping3 -q -c 5 -i u1250 --keep 10.0.0.2
sleep 3
hping3 -q -c 10 -i u3000 --keep 10.0.0.4
sleep 2

echo "Quick 5"
hping3 -q -c 5 -i u2250 --keep 10.0.0.4
sleep 2.2
hping3 -q -c 10 -i u5500 --keep 10.0.0.2
sleep 3.5
hping3 -q -c 20 -i u100 --keep 10.0.0.6
sleep 2
hping3 -q -c 10 -i u2500 --keep 10.0.0.6
sleep 2
hping3 -q -c 5 -i u5000 --keep 10.0.0.2
sleep 2
hping3 -q -c 10 -i u1250 --keep 10.0.0.4
sleep 3
hping3 -q -c 15 -i u1000 --keep 10.0.0.6
sleep 2

echo "Long 4"
hping3 -q -c 10 -i u125000 --keep 10.0.0.4
sleep 1.8
hping3 -q -c 55 -i u65000 --keep 10.0.0.6
sleep 1.5
hping3 -q -c 90 -i u125000 --keep 10.0.0.2