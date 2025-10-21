#################################################
When You Can’t Stop Working, Automate Saying “No”
#################################################
:date: 2025-09-26 22:36
:author: wwakabobik
:tags: macos, productivity, burnout, python, automation
:slug: self_blocker
:category: python
:status: published
:summary: When you're too tired to stop working, a brutal set of scripts can save you from yourself. MacOS, Python, and some shell magic.
:cover: assets/images/bg/python.png


Ever been in that situation where you’re busting your ass on multiple projects, grinding day and night, and somehow your bank account is *not* reflecting your heroic effort? Clients forget to pay. Partners burn through budgets. Project scopes balloon while the paycheck politely declines.

And yet we keep going. Because who else will do it? The overworked developers, freelance warriors, silent soldiers of the digital age. It’s "fine." For now. The only thing we’re running out of is time — and maybe a little soul.

That’s how I ended up building a thing to make me stop.

The Problem: Your Brain Is the Worst Boss You Could Have
========================================================

Let’s be blunt: the problem isn’t laziness. The problem is that you’re *too good* at your job. Your brain has learned to reward you for doing more, so it keeps conning you into overtime and guilt-tripped evenings.

Every hour of downtime becomes a failure. You tell yourself: "Just one more ticket," and three hours later you’re debugging something that can wait until morning. The more you grind, the worse you feel. The harder you try to fix the situation with sheer will, the more you burn out.

When your mind is both the problem and the manager, you can’t just fire yourself. You need external constraints.

Enter: the Self-Blocker.

The Self-Blocker: Not a Productivity App, a Survival Mechanism
--------------------------------------------------------------

This is not a "workflow optimization" toy. This is for the person who literally can’t stop working. It’s for the type who will work for a client who hasn’t paid in a year and a half, who will tolerate a salary well below market, and who will mentally flog themselves to squeeze another hour out of the day.

What it does: it blocks access to *work*, not to life. It can lock directories, open apps, and network resources that are directly associated with paid work — while leaving your personal projects and leisure untouched.

Philosophy in one sentence: if your willpower fails, automate your refusal.

Why Blocker, and Why Not Just Turn Off the Computer?
----------------------------------------------------

At first, I thought about just going the easy route and *locking myself out* of my computer completely. Maybe using a keyboard and screen blocker, or some productivity app that would make me feel better about not working for a few hours. But here’s the thing: aside from the fact that *blocking* everything feels like a major overkill, I actually have things I *want* to work on outside of my paid work. Like pet projects that keep me going, ideas I want to experiment with, or just the need to escape from the grind and get creative.

So, as much as I wanted to "force myself" to stop working, completely locking down the machine — especially my IDEs, which I use for both work and side projects — just didn’t make sense.

Here’s where I hit a crossroads:

I needed something that could help me focus on *not working*, but still allow me to access those pet projects. The goal wasn’t to put my whole computer into a "working lockdown" but to specifically block *work* — not the things I enjoy doing on the side.

I know there are productivity solutions out there, tools that force you to take breaks or limit your screen time. But most of these come with a hefty price tag, and they aren't as flexible as I needed them to be. They either block *everything*, including my personal stuff, or they’re just not targeted enough. Plus, part of me was just like: “Hey, I could do this myself. I want something that works *exactly* for me.”

That’s how I ended up building a tool that was strictly targeted to block *only work-related stuff*. Because in the end, it’s not about shutting down the entire system, it’s about keeping work out while giving space for the things I want to *choose* to do.


**What Are We Blocking? Only Work.**

Now, you might be thinking: *Why don’t you just use a general productivity app that shuts down everything after certain hours?*

Here’s the thing: I have my pet projects, right? These are the ones I enjoy working on. I can’t just shut down everything, including my own creative space. But work? Work *can* get blocked. The goal is to target only the work stuff — the stuff that doesn't *deserve* my attention after hours.

So, I asked myself: *How do I block just my work stuff*? My first idea was to block access to the code repositories — Git is easy to lock, right? Wrong. I need access to my GitHub for personal projects too, so blocking the whole Git service wouldn't work. Then I thought: *What about blocking access to the directories where my work stuff is?*

That seemed like a reasonable solution. Instead of shutting down the entire system, I could block access to specific directories where all the work-related files are stored.


The Approach: Targeted Blocks
=============================

Three layers of blocking:

* **File-level** — block the directories where paid-work lives.
* **Process-level** — kill and prevent relaunch of work apps.
* **Network-level** — block domains and IPs for cloud services that are
  work-only.

You can stack these. Each layer compensates for weaknesses in another.

Directory Blocking (a.k.a. "Make Your Files Temporarily Invisible")
-------------------------------------------------------------------

The simplest, most reliable strike: change file permissions so you can’t open or edit the stuff you shouldn’t touch.

.. code-block:: bash

    # Make the directory inaccessible
    chmod -R 000 /path/to/work/project


This removes read/write/execute permissions for owner, group and others. It doesn't delete anything — it merely makes the files inaccessible until you restore permissions.

Pros:

* Simple, system-level, and portable on Unix-like systems (macOS included).
* Reversible: you can *chmod* back when it’s work time
* No third-party lock-in; no subscription.

Cons:

* It only blocks access to files. It won't stop you from opening web tools or
  streaming from a cloud IDE unless you combine it with other measures.
* If you forget to restore permissions, you'll be annoyed — intentionally so.
* Determined you as sudo may reset it; this is a soft-but-nasty friction.

Implementation sketch (Python)

.. code-block:: python

    import os
    import stat

    def block_path(path: str) -> None:
        """Set permissions to 0 for all files and directories under *path*."""
        if not os.path.exists(path):
            log(f"Path not found: {path}")
            return
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                try:
                    os.chmod(os.path.join(root, name), 0)
                except Exception as e:
                    log(f"Error chmod file {name}: {e}")
            for name in dirs:
                try:
                    os.chmod(os.path.join(root, name), 0)
                except Exception as e:
                    log(f"Error chmod dir {name}: {e}")
        os.chmod(path, 0)
        log(f"Blocked: {path}")


And the reverse:


.. code-block:: python

    import subprocess

    def unblock_path(path: str) -> None:
        """Restore directories to 755 and files to 644 using *find* + *chmod*.
        Requires sudo for some cases.
        """
        subprocess.run(["sudo", "find", path, "-type", "d", "-exec",
                        "chmod", "755", "{}", "+"], check=True)
        subprocess.run(["sudo", "find", path, "-type", "f", "-exec",
                        "chmod", "644", "{}", "+"], check=True)
        log(f"Unblocked: {path}")


Alternatives: Renaming and Encryption (and Why They Suck)
---------------------------------------------------------

So, I thought, maybe I could take it a step further. Instead of just using *chmod*, why not rename directories or even encrypt them? After all, renaming them would make it harder to find them and encryption could make sure even if I *did* find them, they’d be unreadable. Problem solved, right?

Well, not quite.

**Renaming** is a viable option, but it’s honestly a pain in the ass. I could rename every folder to something unrecognizable, like *Work_12345*, but then I’d spend the next 10 minutes wondering where my projects are. Plus, it's *manual*. If I forget to rename a folder before my “off-hours,” I’m back to square one.

As for **encryption**... sure, I could encrypt my work files. It adds a layer of protection and prevents me from accessing them unless I decrypt them manually. But the problem with this approach is that it’s cumbersome. You’re adding unnecessary complexity to the process, and it’s easy to break the flow. And trust me — when you’re dealing with a gazillion files, decrypting them just to *not* work becomes the new form of procrastination.

In the end, I decided that renaming and encryption were overkill for what I wanted to achieve: a simple, flexible, and effective way to block myself from work during off-hours without completely removing my ability to work on things I *actually care about*.

Well, I might be more brutal to *rm -rf* my work directory if I ever get desperate enough, but for now, *chmod* does the trick. Honestly, I like my git repos to stay intact, so I can always clone them back when it’s time to work again.

App Dropping: Because "Quit" Is for the Weak
--------------------------------------------

Quitting apps is polite. Force-killing them is decisive.

If you've ever tried to simply close your applications to "stop working," you might as well be whispering sweet nothings to your workaholic brain. Just closing an app doesn't stop it from secretly running in the background, silently mocking your attempts at self-care. For those who require a tougher solution, let's get down to the dirty business of killing those processes completely.
It's not just about shutting things down anymore—no, no, no. It's about forcefully terminating your productivity nightmares, using system commands that will make even the most stubborn apps go away. Welcome to the world of SIGTERM, SIGKILL, and a few choice scripts designed to obliterate your distractions in a way that even your "chill" after-hours self will approve of.
Remember that "just quit" mindset? Forget it. You can quit like a civilized human being, or you can kill a process like the data-hungry monster that it is. This isn't a mere closing of windows; we're talking about full-on termination. Enter pkill, pgrep, and a healthy dose of kill signals. Let’s break down the code that will make your unwanted apps disappear faster than your desire to work.

Processes linger. Some apps auto-relaunch. Some live in the menu bar. Idea is simple: find process IDs and send SIGTERM, then SIGKILL if they refuse to die. Also, unload their launch agents so macOS doesn't restart them behind your back.
First, let’s look at this handy script:

.. code-block:: python

    #!/usr/bin/env python3

    import subprocess
    import os
    import time

    PKILL = '/usr/bin/pkill'
    PGREP = '/usr/bin/pgrep'

    def run(cmd, check=False, capture=False):
        return subprocess.run(cmd, check=check, capture_output=capture, text=True)

    def pgrep_pids(pattern: str):
        res = run([PGREP, '-f', pattern], capture=True)
        return [int(x) for x in res.stdout.strip().splitlines() if x.strip().isdigit()]

    def kill_pids(pids, sig=15):
        for pid in pids:
            try:
                os.kill(pid, sig)
                log(f"Sent signal {sig} to {pid}")
            except Exception as e:
                log(f"Error signaling {pid}: {e}")

    def drop_entry(entry: str):
        pids = pgrep_pids(entry)
        if pids:
            kill_pids(pids, sig=15)
            time.sleep(0.8)
            pids = pgrep_pids(entry)
            if pids:
                kill_pids(pids, sig=9)
                log(f"Force-killed: {entry}")
        else:
            log(f"No processes for: {entry}")


Notice how the script uses pkill and pgrep to ruthlessly hunt down and terminate processes. It's like playing the predator, but instead of chasing down small mammals, you're hunting down Slack, Spotify, or any other productivity-sucking monstrosity.
Understanding SIGTERM and SIGKILL: Your New Best Friends
Let’s take a quick detour to talk about the stars of the show: SIGTERM and SIGKILL.
* SIGTERM (signal 15): This is your "let's be polite" approach. It tells the application to gracefully shut down. Think of it like trying to talk someone out of staying at your party after you've had enough. It's the nice way out.
* SIGKILL (signal 9): But when that polite request doesn’t work, it's time to bring out the big guns. SIGKILL forcefully terminates the application without warning. It’s like smashing the “end call” button during an awkward conversation. There's no coming back from this one.
The kill_pids function in the script does both: first it sends SIGTERM to allow the process to exit peacefully, and if that fails, it uses SIGKILL to terminate the application with extreme prejudice.
The Art of Unloading Launch Agents (Because We Hate Reboots)
It’s not just about killing apps in the foreground. Oh no, we’re going deeper. We’re talking about launch agents—those sneaky little background services that restart applications as soon as you try to close them. Because nothing says “I’m a rebel” like quitting your job only for it to restart in the background.
Enter launchctl—the macOS tool for interacting with launch agents. With the script's unload_launch_agent function, we can force macOS to stop these persistent little buggers from restarting. So, if you want to be the absolute master of your work environment, it's time to get familiar with how launchctl bootout and launchctl unload work.

Unloading launch agents (to stop auto-restarts):

.. code-block:: python

    LAUNCHCTL = '/bin/launchctl'

    def unload_launch_agent(plist_path: str) -> None:
        try:
            run([LAUNCHCTL, 'bootout', plist_path], check=False)
            log(f"Bootout attempted: {plist_path}")
        except Exception:
            try:
                run([LAUNCHCTL, 'unload', plist_path], check=False)
                log(f"Unload attempted: {plist_path}")
            except Exception as e:
                log(f"Failed to unload {plist_path}: {e}")


A small, mercifully brutal script that kills and prevents relaunch will stop most app-based temptations. Pair it with directory-blocking and you’ve got a ridiculously reliable deterrent.

So, what's the takeaway from all of this? The next time you're tempted to tell yourself, “I’ll just close Slack for the night,” remember that there's a much more satisfying (and permanent) way to do it. Use pkill to obliterate those pesky processes. Use launchctl to disable the auto-start of those launch agents. Because you’re not just quitting; you’re winning at not working.
This script will turn your nightly routine into a warzone where your work apps are the unwelcome intruders, and you're the ruthless commander sending them to oblivion. And when it's time to get back to work? Just run the opposite: unblock, reload, and pick up where you left off. But for now, let’s enjoy some well-deserved freedom.

Website Blocking: Because Slack Is a Hydra
------------------------------------------

Alright, we’ve locked ourselves out of the working directories, and we’ve ruthlessly murdered every app that dared to run during off-hours. But let’s face it: we can still fall into the trap of checking emails, reading Slack messages, or—god forbid—staring at Jira tickets. All this while we pretend we're being productive.

So, it's time for the ultimate move: blocking access to those glorious websites. The only thing we want to see during non-work hours is a cat video, not a task list. For that, I use macOS’s PF (packet filter) to block specific IPs.

The idea:

* List domains in a *work_domains.txt* file (one per line).
* Resolve domains to IPv4 addresses with *dig*.
* Write *block* rules to a PF anchor file.
* Load the anchor via */etc/pf.conf* and *pfctl*.

Why PF and not */etc/hosts*? Because IPs change and hosts-based blocking is
fragile. PF blocks at the network layer and is harder for your impulse to bypass.

Resolve and write anchor (sketch):

.. code-block:: python

    import subprocess
    from pathlib import Path

    DOMAINS_FILE = Path('work_domains.txt')
    ANCHOR_FILE = '/etc/pf.anchors/work_blocker'

    def resolve_ips(domains: list[str]) -> list[str]:
        ips = set()
        for d in domains:
            res = subprocess.run(['dig', '+short', d], capture_output=True, text=True)
            for line in res.stdout.splitlines():
                line = line.strip()
                if line and all(c.isdigit() or c == '.' for c in line):
                    ips.add(line)
        return sorted(ips)


This snippet takes a list of domains, runs a dig command to resolve them, and collects the IPs. You’ll notice we’re being picky about the format—only valid IP addresses are added to our list.
Now why not use hosts or DNS blocking? Because domains can resolve to multiple IP addresses, and DNS caching can screw you over. In the grand scheme of things, we need to work on real-time IP addresses.

.. code-block:: python

    def write_anchor_file(ips: list[str]):
        with open(ANCHOR_FILE, 'w') as f:
            for ip in ips:
                f.write(f"block drop out quick to {ip}\n")


        sys.exit(1)


In the above code, we're writing our rules to the pf anchor file. Important: You will need to run this script as sudo because modifying firewall rules requires admin privileges. No surprises here, we’re doing this to make sure nothing slips past.
Ensuring Rules Are Loaded
Now, we need to ensure that these rules are actually being loaded into macOS’s pf system. This is where things get slightly annoying because macOS uses pf as a packet filter for firewall rules, but its configuration files aren’t automatically set up to include custom rules.

.. code-block:: python

    def ensure_pf_conf_includes_anchor() -> None:
        anchor_rule = f'anchor "{ANCHOR_NAME}"'
        anchor_load = f'load anchor "{ANCHOR_NAME}" from "{ANCHOR_FILE}"'

        with open(PF_CONF_FILE, "r") as f:
            contents = f.read()

        if anchor_rule not in contents:
            try:
                with open(PF_CONF_FILE, "a") as f:
                    f.write(f"\n{anchor_rule}\n{anchor_load}\n")
                log("Added anchor rules to /etc/pf.conf")
            except PermissionError:
                log(f"Permission denied: cannot write to {PF_CONF_FILE}. Use sudo.")
                sys.exit(1)


We’re checking if the pf.conf file already includes our custom anchor rules. If not, we append the necessary lines to make sure our rules get loaded every time the firewall is applied. Again, expect to run this with sudo for the necessary permissions.

Once everything is set up, we simply need to apply the rules. But don't worry—if you change your mind and decide to start "working" again, we can easily revert the blocking.
To apply the rules, we use pfctl:

.. code-block:: python

    PFCTL_BIN = '/sbin/pfctl'
    PF_CONF_FILE = '/etc/pf.conf'

    def apply_pf() -> None:
        try:
            subprocess.run([PFCTL_BIN, "-f", PF_CONF_FILE], check=True)
            subprocess.run([PFCTL_BIN, "-e"], check=False)
            log("pfctl rules applied and pf enabled")
        except subprocess.CalledProcessError as e:
            log(f"Failed to apply pfctl rules: {e}")
            sys.exit(1)


In short, you’ll activate pfctl with the rules we’ve added and block the domains. When you’re ready to unblock, it’s as simple as running another command that clears the anchor and reloads the config.
And don't worry—if you suddenly need to reconnect with the outside world (or un-apply your firewall rules), we've got you covered with a function to disable the blocking:

.. code-block:: python

    def disable_pf_block() -> None:
        try:
            with open(ANCHOR_FILE, "w") as f:
                pass  # Empty the anchor file
            subprocess.run([PFCTL_BIN, "-f", PF_CONF_FILE], check=True)
            log("pfctl reloaded with cleared rules")
        except Exception as e:
            log(f"Failed to disable PF blocking rules: {e}")
            sys.exit(1)


The beauty of this solution is that it’s both flexible and aggressive. Want to block access to Slack? Great, just add it to your work_domains.txt. Want to shut down Jira tickets like they never existed? No problem, put those domain names in the file, and this script will handle the rest. You’ve got your personal firewall. Go ahead—be "productive" somewhere else.

That’s how we use real firewall rules to ensure we're not getting sucked into digital work addiction. Want to know what other digital distractions you could block? Get creative, and you’ll never have to see those godforsaken task lists ever again.

How It Works: An Overly Complicated Way to Avoid Temptation
Now that you have the code, here’s a quick rundown of what’s going on behind the scenes. We're using PF, the packet filter in macOS, which is kind of like a bouncer at the club of the internet. This is not your average "edit the /etc/hosts file" nonsense. No, this is real-deal firewall stuff.
Here’s how this works, step by step:
1. Resolving Domains to IPs: We need to resolve the domains (e.g., slack.com, jira.com) to their IP addresses. Why? Because, while domains are nice and human-friendly, the network speaks in IPs. And if you try blocking a domain directly, you’ll quickly discover that they can change their IPs on you. The process of resolving to IP addresses is done with the dig command, which gets us the current IPs for any domain we throw at it.
2. Blocking the IPs: Once we’ve resolved these IP addresses, we write them into PF's anchor file. Think of it as a blacklist of sites we should never visit during work hours (or any hours, really).
3. Applying the Block: The PF configuration file is updated with our custom blocking rules. Once that’s done, we use pfctl to enforce the block on those IPs. Now, anytime you try to visit a site on the list, it’s as if the internet just refuses to acknowledge your existence. Bye, work distractions!
4. Reversing the Block: If, for some reason, you want to get back to working (and pretending to be productive), the script can clear the block by removing the anchor rules and reloading PF without those rules. Simple, effective, and a perfect reminder that we’re all just doing the bare minimum.

At the end of the day, this is all about one thing: shutting down your productivity-killing habits before they even start. You've blocked the apps, you've locked down directories, and now you've blocked the very websites that you would otherwise use to procrastinate. You've practically built a fortress around your work life—and if you're feeling like a rebellious coder, you can always unblock things later.
But for now, go ahead and enjoy the sweet silence of being free from distraction. Until the next time you forget about all this and try to cheat your way back into work—because we both know that’s inevitable.

Utility Glue: Logging and Notifications
---------------------------------------

You’ll want logs and notifications so the thing doesn’t feel like a random punishment. Logging gives you a trail; notifications give you context when you try to cheat.

.. code-block:: python

    from datetime import datetime
    import subprocess

    LOG_FILE = '/var/log/self_blocker.log'
    OSASCRIPT_BIN = '/usr/bin/osascript'

    def log(msg: str) -> None:
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"{ts}: {msg}"
        try:
            with open(LOG_FILE, 'a') as f:
                f.write(line + "\n")
        except Exception:
            pass
        print(line)

    def notify(message: str, title: str = '🚫 Self-Blocker') -> None:
        try:
            subprocess.run([OSASCRIPT_BIN, '-e',
                            f'display notification "{message}" with title "{title}"'],
                           check=True)
        except Exception as e:
            log(f"Notify failed: {e}")

We use AppleScript (osascript) under the hood to trigger the notifications. This is a simple but powerful way to alert you when something important happens during the script’s operation. For example, when the websites are successfully blocked or unblocked, or when an error occurs, you’ll get a notification, keeping you updated without needing to check logs manually.
Customization: You can even add a subtitle or choose a custom sound for the notification. For instance, using the "Submarine" sound effect gives it a bit more flair. You know, for when you need to feel like you're in control of your digital life—or when you just want to hear the notification sound over and over again.

Blocking websites is only useful if you're not constantly second-guessing yourself and saying, “Oh, I’ll just unblock everything for 5 minutes…” That’s a recipe for disaster. In the script, we ensure you can’t unblock access unless you're officially in "off-hours."

.. code-block:: python

    from pathlib import Path

    WORK_MODE_FILE = Path.home() / '.work_mode'

    def check_work_mode_file() -> None:
        """Prevent unblock unless .work_mode exists (i.e. it's not work time)."""
        if WORK_MODE_FILE.exists():
            log("❌ Cannot unblock: not work time.")
            sys.exit(1)

Here, we’ve added a little guardrail: the script checks for the presence of a .work_mode file before allowing you to unblock access. If that file exists, it’s your own personal signal that you’ve entered “work mode” and shouldn’t be messing around with your internet access. This simple file-based check helps reinforce the boundaries between work and personal time.
If you try to unblock during work time, the script will log it and promptly stop you. This is your safety net, helping you resist the urge to slip into that black hole of productivity-sucking websites.

Automation: launchd, Because Cron Is Ancient
--------------------------------------------

You’ve done the hard part—blocking those productivity-draining websites and setting up notifications and logs. Now, you need to automate it all, right? Well, let’s talk about running this script at scheduled times, because let's face it, no one’s got time to run this manually.
And no, cron isn’t the answer. Sure, it’s been around forever, and people still use it like it’s some kind of sacred relic, but let’s be real: it’s not even close to being as neat and modern as macOS’s launchd. Cron is an ancient tool that doesn't handle macOS’s security features, sudo permissions, or the finer details of system scheduling—plus, it won’t even run GUI-based processes properly. This is macOS, not some Linux server where you can get away with just typing a cron job every week to download logs.

*launchd* is macOS’s native service manager. It's more powerful and flexible than cron could ever dream of being. With launchd, you can schedule tasks with precision down to the minute, manage those tasks while they’re running, and, most importantly, make sure they run even after a reboot. And you definitely need that for something as crucial as blocking access to websites, right?
But before you go setting it up, there’s one little hurdle you’ll need to cross—getting your script to run with sudo. Most of the time, you won’t need sudo for launchd, but there are situations where elevated privileges are necessary (like changing firewall rules or modifying network settings). When that’s the case, we have to tweak the sudoers file to grant the necessary permissions.

**Giving sudo Permissions**.

When the script calls for sudo, you’ll probably get an error like this:

.. code-block:: text

    Sorry, user yourusername may not run sudo on this host.


To avoid this frustration, you’ll need to give your user permission to run these scripts without typing in a password every single time. But wait! Be careful—editing the sudoers file is no joke, and one wrong line could make your machine inaccessible. You don’t want that, do you?
To give the script sudo permissions, follow these steps:

1. Open the terminal and type *sudo visudo* — this opens the sudoers file in a safe editor.
2. Scroll to the bottom and add this line:

.. code-block:: bash

    yourusername ALL=(ALL) NOPASSWD: /path/to/your/script


3. Save and exit (in *visudo*, press *Ctrl + X*, then *Y*, then Enter to save).


Now, your script can run with sudo permissions without asking for your password. We love convenience, don’t we?

**Setting Up the Jobs with launchd**.

Once you’ve edited the sudoers file, it’s time to schedule your self-blocking script with launchd. The beauty of launchd is that it’s a real service manager. Forget cron’s basic time scheduling—launchd allows you to run jobs based on conditions like user login, system boot, or, in our case, custom time intervals. It’s far more robust and has much better integration with the macOS ecosystem.

In the script, we've set up multiple launchd jobs, including:

* Block and Unblock Jobs: These jobs are scheduled based on your work hours. The block job runs when you're supposed to be working, and the unblock job kicks in when it’s break time.
* Relock Job: This task checks periodically (every 5 minutes, in this case) to see if your workblocker script is still running, ensuring your system remains locked down, even if you’re distracted and forget to re-enable blocking.
* Relock Loaders: These jobs make sure to load and unload the blocking schedules at the correct times, so you don’t have to lift a finger—unless you're trying to cheat.

The core of these tasks is the plist files (launchd configuration files), which are generated by the script. They’re loaded into LaunchAgents, macOS's equivalent of cron jobs. This lets macOS know what tasks to run and when.

Tips:

* If your scripts need *sudo*, consider adding a minimal *NOPASSWD* entry in
  *sudoers* for those specific binaries. Be *very* careful editing *sudoers*.
* Generate *.plist* files for *launchd* programmatically and load them under
  *~/Library/LaunchAgents*.
* Create a periodic relock job that runs every 5 minutes to ensure your
  blocking state is intact.

A short *launchd* checklist:

* Create plists for block/unblock/relock.
* Load them with *launchctl bootstrap* / *launchctl enable* as appropriate.
* Test thoroughly — a misconfigured job can be noisy.

Final Thoughts (Philosophy)
===========================

The Self-Blocker tool offers a robust yet simple solution to a problem faced by many knowledge workers — the inability to stop working when work life bleeds into personal time. This tool is not about productivity or motivation, but about setting clear boundaries in an environment where distractions and the pressure to "do more" often come from within.
By leveraging MacOS's native launchd scheduling system, this tool automates the blocking and unblocking of work-related apps, directories, and internet access based on user-configured schedules. It empowers users to enforce boundaries for themselves, ensuring that rest and personal time are honored, even when their own willpower might fail.
It is clear that this tool’s value isn't just in the technical details — the use of chmod, sudoers, and launchd — but in its core philosophy. It offers a solution for those who are overwhelmed by the demands of an unforgiving work culture, creating a strict, automated mechanism to force users to disconnect.
With options for configuration, users can define their own "work intervals," block directories or apps, and even prevent internet access to stay focused during work hours. Outside of those intervals, it shields users from their own tendencies to slip back into overwork, offering an enforced and uncaring reset.

The Self-Blocker isn’t about "helping you be more productive." It’s about helping you *stop* working when work starts killing you. It’s a set of friction mechanisms aimed at breaking the addictive loop of "just one more" that many of us are trapped in.

It’s opinionated: it will be inconvenient. That’s the point. If you deserve to be on call 24/7, don’t use it. If you, like me, need to stop yourself from turning constant hustle into self-destruction, it’s liberating.

If you like my article, feel free to `throw a coin`_. And, for sure here are link to the `GitHub repo`_ with all code. Star and fork it if you like it.


.. _throw a coin: https://www.donationalerts.com/r/rocketsciencegeek
.. _GitHub repo: https://github.com/wwakabobik/macos_selfblocker
