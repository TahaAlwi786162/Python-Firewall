# Python Firewall Project

This is a firewall I made in Python that watches network traffic and blocks certain IP addresses using Windows Firewall. It doesn't just detect bad traffic, it actually blocks it for real.

## Why I made this

I run my school's cybersecurity club and I wanted to make something that actually does stuff instead of just using tools other people made. I started with just a dictionary of IPs and it turned into a lot more once I started running into problems.

## What it actually does

1. Uses `scapy` to watch live traffic on my network
2. Checks the IP of every packet against a list of blocked IPs
3. If it matches, it runs a Windows command (`netsh advfirewall`) that actually blocks that IP
4. Writes everything it does to a log file with timestamps
5. Has a "safe list" so it can never block my router by accident (this happened almost happened to me lol)

## What you need

- Python 3
- Scapy (`pip install scapy`)
- Npcap (scapy needs this on Windows to actually capture packets, get it from npcap.com)
- Windows (this uses `netsh` so it only works on Windows)
- You need to run it as admin or it won't work

## How to run it

1. Run `ipconfig` in cmd to find your own IP and your router's IP
2. Put your IPs into the `blocked_ips` dictionary in the code
3. Add your router IP to `safe_list` so you don't lock yourself out
4. Open cmd as admin
5. Run: python firewall.py
6. Do stuff like open a website or ping something and watch it detect and block IPs

## Warning

This actually changes your real Windows Firewall settings. If you block an IP it stays blocked until you delete the rule: netsh advfirewall firewall delete rule name="Block_(ip goes here)"
Only test this on your own stuff, don't be dumb and run it on a network that's not yours.

## Stuff I learned / problems I ran into

- I had a bug where my code would `return` inside the for loop instead of after it, so it basically only ever checked the first rule and let everything else through without me noticing for a while
- The first time I tried to actually block an IP nothing happened and it took me a while to realize it was because I wasn't running it as admin, the code was failing silently and not telling me anything was wrong
- I almost blocked my own router which would've messed up my wifi for my whole house, so I added a safe list so that can't happen again
- I found a random second network adapter with a weird `169.254` address while doing this and had to look up what that even was (turns out its just a placeholder address windows gives when something isn't actually connected)

## What I want to add next

- Make blocks expire after a certain time instead of being permanent
- Block by port/protocol too, not just IP
- Use this to protect an IoT project I'm building separately
- Maybe a simple webpage to see the logs instead of opening a text file

## Note

This was made for learning purposes on my own home network. Not meant to be used on networks or devices that aren't mine.
