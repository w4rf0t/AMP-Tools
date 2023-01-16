#!/usr/bin/python3
# !/usr/bin/python

# import http.cookiejar
import subprocess
import httplib2
import http.client
import queue
import subprocess
import time
from argparse import ArgumentParser
from os import getpid, kill
from signal import SIGINT, signal
from socket import *
from sys import argv, stdout
from threading import Thread, Lock
import os


def killpid(signum=0, frame=0):
    print("\r\x1b[K")
    os.kill(getpid(), 9)


signal(SIGINT, killpid)


class myThread(Thread):
    def __init__(self, threadID, name, q):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        getresponse(self.name, self.q)


class Timer:
    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        taken = time.time() - self.start
        seconds = int(time.strftime("%S", time.gmtime(taken)))
        minutes = int(time.strftime("%M", time.gmtime(taken)))
        hours = int(time.strftime("%H", time.gmtime(taken)))
        if minutes > 0:
            if hours > 0:
                print(
                    " [*] Time elapsed "
                    + str(hours)
                    + " hours, "
                    + str(minutes)
                    + " minutes and "
                    + str(seconds)
                    + " seconds at "
                    + str(round(len(adminlist) / taken, 2))
                    + " lookups per second."
                )
            else:
                print(
                    " [*] Time elapsed "
                    + str(minutes)
                    + " minutes and "
                    + str(seconds)
                    + " seconds at "
                    + str(round(len(adminlist) / taken, 2))
                    + " lookups per second."
                )
        else:
            print(
                "[*] Time elapsed "
                + str(seconds)
                + " seconds at "
                + str(round(len(adminlist) / taken, 2))
                + " lookups per second."
            )
        maked = "rm -rf .cache_httplib"
        process = subprocess.Popen(maked.split(), stdout=subprocess.PIPE)
        poutput = process.communicate()[0]
        interact = input("Press any key to exit...")
        if interact:
            exit()


class Printer:
    def __init__(self, data):
        stdout.write("\r\x1b[K" + data.__str__())
        stdout.flush()


def getresponse(threadName, q):
    for i in range(len(adminlist)):
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            checkg = 1
            while checkg == 1:
                try:
                    connection = http.client.HTTPConnection(str(url))
                    connection.request("HEAD", "/" + str(data.strip()))
                    response = connection.getresponse()
                    progdone = len(adminlist) - workQueue.qsize()
                    update = (
                        "[>] Checking "
                        + str(progdone)
                        + "/"
                        + str(len(adminlist))
                        + " "
                        + str(url)
                        + "/"
                        + str(data.strip())
                        + " \t["
                        + str(response.status)
                        + "]"
                    )
                    Printer(update)
                    checkg += 1
                    reporturl = "\r\x1b[K [*] " + \
                        str(url) + "/" + str(data.strip())
                    if len(reporturl) < 60:
                        add = 60 - int(len(reporturl))
                        reporturl = str(reporturl) + str(" ") * int(add)
                        reportcode = "[" + str(response.status) + "]"
                    if response.status == 200:
                        print(str(reporturl) + str(reportcode) + " OK")
                        found.append(response.status)
                        subprocess.run(['echo', str(url) + "/" + str(data.strip())], stdout=open(
                            'results/adminfinder/'+domain+'.txt', 'a'))
                    elif 300 <= response.status < 400 and args.follow:
                        reso = httplib2.Http(".cache_httplib")
                        reso.follow_all_redirects = True
                        link = "http://" + str(url) + "/" + str(data.strip())
                        resp = reso.request(link, "HEAD")[0]
                        finalurl = resp["content-location"]
                        if finalurl[0:5] == "http:":
                            finalurl = finalurl[11:]
                        elif finalurl[0:5] == "https":
                            finalurl = " [HTTPS] " + finalurl[12:]
                        print(
                            str(reporturl)
                            + str(reportcode)
                            + " Redirect >> "
                            + str(finalurl)
                        )
                    elif response.status == 403 and args.forbidden:
                        print(str(reporturl) + str(reportcode) + " Forbidden!")
                except:
                    pass
        else:
            queueLock.release()


def killpid(signum=0, frame=0):
    print("\r\x1b[K")
    kill(getpid(), 9)


parser = ArgumentParser(prog="adminfinder", usage="adminfinder [options]")
parser.add_argument("-u", "--url", type=str, help="url eg. target.com")
parser.add_argument("-w", "--wordlist", type=str, help="wordlist")
parser.add_argument("-t", "--threads", type=int, help="number of threads")
parser.add_argument(
    "-f", "--follow", action="store_true", help="follow and resolve redirects"
)
parser.add_argument(
    "-b", "--forbidden", action="store_true", help="show forbidden pages"
)
args = parser.parse_args()

if len(argv) == 1:
    parser.print_help()
    exit()


domain = args.url
url = str(domain.strip())
adminlist = [line.strip() for line in open(args.wordlist, "r")]
queueLock = Lock()
workQueue = queue.Queue(len(adminlist))
found = []
threads = []
exitFlag = 0
threadID = 1
maxthreads = 40

if args.threads:
    maxthreads = args.threads

queueLock.acquire()
for word in adminlist:
    workQueue.put(word)
queueLock.release()

while threadID <= maxthreads:
    tname = str("Thread-") + str(threadID)
    thread = myThread(threadID, tname, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

with Timer():
    while not workQueue.empty():
        pass
    for t in threads:
        t.join()
    print("\r\x1b[K[*] All threads complete, " +
          str(len(found)) + " sites found.")
subprocess.call("clear", shell=True)
