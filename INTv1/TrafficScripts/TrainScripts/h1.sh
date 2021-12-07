echo "Long 1"
hping3 -q -c 30 -i u125000 --keep 10.0.0.2
sleep 1
hping3 -q -c 10 -i u100000 --keep 10.0.0.4
sleep 0.6
hping3 -q -c 30 -i u50000 --keep 10.0.0.6

echo "Attack"
# Transmits between 500 - 1500 packets.
# The number of flows for some reason is smaller.
# timeout 0.073 hping3 -S --flood -p 80 --spoof 69.0.0.1 10.0.0.2 &

echo "Quick 1"
hping3 -q -c 15 -i u1000 --keep 10.0.0.2
sleep 2
hping3 -q -c 10 -i u2000 --keep 10.0.0.4
sleep 2
hping3 -q -c 25 -i u1000 --keep 10.0.0.4
sleep 2
hping3 -q -c 15 -i u15000 --keep 10.0.0.6
sleep 2
hping3 -q -c 10 -i u15000 --keep 10.0.0.2
sleep 2
hping3 -q -c 5 -i u5000 --keep 10.0.0.4
sleep 2
hping3 -q -c 10 -i u2500 --keep 10.0.0.2
sleep 3
hping3 -q -c 10 -i u1500 --keep 10.0.0.2
sleep 2
hping3 -q -c 5 -i u250 --keep 10.0.0.4
sleep 3
hping3 -q -c 10 -i u4500 --keep 10.0.0.6
sleep 2
hping3 -q -c 12 -i u1250 --keep 10.0.0.4
sleep 2.2
hping3 -q -c 5 -i u7500 --keep 10.0.0.6
sleep 3.5
hping3 -q -c 10 -i u2000 --keep 10.0.0.2

echo "Long 2"
hping3 -q -c 100 -i u105000 --keep 10.0.0.2
sleep 2
hping3 -q -c 40 -i u45000 --keep 10.0.0.2
sleep 2
hping3 -q -c 10 -i u25000 --keep 10.0.0.4

echo "Long 3"
hping3 -q -c 50 -i u150000 --keep 10.0.0.2
sleep 1.5
hping3 -q -c 55 -i u25000 --keep 10.0.0.4
sleep 0.8
hping3 -q -c 40 -i u45000 --keep 10.0.0.6

echo "Quick 2"
hping3 -q -c 15 -i u1000 --keep 10.0.0.2
sleep 2
hping3 -q -c 10 -i u2000 --keep 10.0.0.4
sleep 2
hping3 -q -c 25 -i u1000 --keep 10.0.0.4
sleep 2
hping3 -q -c 15 -i u15000 --keep 10.0.0.6
sleep 2
hping3 -q -c 10 -i u15000 --keep 10.0.0.2
sleep 2
hping3 -q -c 5 -i u5000 --keep 10.0.0.4
sleep 2
hping3 -q -c 10 -i u2500 --keep 10.0.0.2
sleep 3
hping3 -q -c 10 -i u1500 --keep 10.0.0.2
sleep 2
hping3 -q -c 5 -i u250 --keep 10.0.0.4
sleep 3
hping3 -q -c 10 -i u4500 --keep 10.0.0.6
sleep 2
hping3 -q -c 12 -i u1250 --keep 10.0.0.4
sleep 2.2
hping3 -q -c 5 -i u7500 --keep 10.0.0.6
sleep 3.5
hping3 -q -c 10 -i u2000 --keep 10.0.0.2

echo "Long 4"
hping3 -q -c 80 -i u125000 --keep 10.0.0.4
sleep 1.2
hping3 -q -c 55 -i u75000 --keep 10.0.0.6
sleep 1.5
hping3 -q -c 40 -i u225000 --keep 10.0.0.2

echo "Waiting to Flush, press a key when ready"
read temp

echo "Starting next Batch"

echo "Long 5"
hping3 -q -c 100 -i u105000 --keep 10.0.0.2
sleep 2
hping3 -q -c 40 -i u45000 --keep 10.0.0.2
sleep 2
hping3 -q -c 10 -i u25000 --keep 10.0.0.4

echo "Quick 3"
hping3 -q -c 15 -i u1000 --keep 10.0.0.2
sleep 2
hping3 -q -c 10 -i u2000 --keep 10.0.0.4
sleep 2
hping3 -q -c 25 -i u1000 --keep 10.0.0.4
sleep 2
hping3 -q -c 15 -i u15000 --keep 10.0.0.6
sleep 2
hping3 -q -c 10 -i u15000 --keep 10.0.0.2
sleep 2
hping3 -q -c 5 -i u5000 --keep 10.0.0.4
sleep 2
hping3 -q -c 10 -i u2500 --keep 10.0.0.2
sleep 3
hping3 -q -c 10 -i u1500 --keep 10.0.0.2
sleep 2
hping3 -q -c 5 -i u250 --keep 10.0.0.4
sleep 3
hping3 -q -c 10 -i u4500 --keep 10.0.0.6
sleep 2
hping3 -q -c 12 -i u1250 --keep 10.0.0.4
sleep 2.2
hping3 -q -c 5 -i u7500 --keep 10.0.0.6
sleep 3.5
hping3 -q -c 10 -i u2000 --keep 10.0.0.2

echo "Long 6"
hping3 -q -c 50 -i u150000 --keep 10.0.0.2
sleep 1.5
hping3 -q -c 55 -i u25000 --keep 10.0.0.4
sleep 0.8
hping3 -q -c 40 -i u45000 --keep 10.0.0.6

echo "Long 7"
hping3 -q -c 80 -i u125000 --keep 10.0.0.4
sleep 1.2
hping3 -q -c 55 -i u75000 --keep 10.0.0.6
sleep 1.5
hping3 -q -c 40 -i u225000 --keep 10.0.0.2

echo "Quick 4"
hping3 -q -c 5 -i u5000 --keep 10.0.0.4
sleep 2
hping3 -q -c 10 -i u2500 --keep 10.0.0.2
sleep 3
hping3 -q -c 10 -i u1500 --keep 10.0.0.2
sleep 2
hping3 -q -c 5 -i u250 --keep 10.0.0.4
sleep 3
hping3 -q -c 10 -i u4500 --keep 10.0.0.6
sleep 2
hping3 -q -c 12 -i u1250 --keep 10.0.0.4
sleep 2.2
hping3 -q -c 5 -i u7500 --keep 10.0.0.6
sleep 3.5
hping3 -q -c 10 -i u2000 --keep 10.0.0.2