#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pexpect import spawn, TIMEOUT, EOF
from re import compile
from threading import Thread
from time import sleep
from subprocess import Popen, PIPE, STDOUT
from os import getcwd, path

class OMXPlayer(object):
    exec_path = "omxplayer"
    args = "-o both"

    def __init__(self):
        self.__paused = False
        self.__subtitles_visible = True
        self.__position = 0.0
        self.__filename = None
        self.__fileinfo = None
        self.__fileinfo_parsed = {}
        self.__process = None
        
    def play(self, mediafile):
        if not self.isstopped():
            self.stop()
        self.__fileinfo = self.__get_fileinfo(mediafile)
        #New omxplayer builds will need this flag to report status
        cmd = "{ep} -s {a} {f}".format(ep=self.exec_path, a=self.args, f=mediafile)
        self.__process = spawn(cmd) 
        self.__position_thread = Thread(target=self.__get_position)
        self.__position_thread.start()
        self.__filename = mediafile
        while not self.__process.isalive():
            sleep(0.15)
    
    def __del__(self):
        self.stop()
        
    def quit(self):
        self.stop()
        
    def isstopped(self):
        try:
            return not self.__process or not self.__process.isalive()
        except OSError:
            # sometimes it throws: isalive() encountered condition where "terminated" is 0, but there was no child process. Did someone else call waitpid() on our process?
            return False

    def pause(self):
        if not self.__process:
            return
        if self.__process.send('p'):
            self.__paused = not self.__paused

    def toggle_subtitles(self):
        if not self.__process:
            return
        if self.__process.send('s'):
            self.__subtitles_visible = not self.__subtitles_visible
            
    def stop(self):
        self.__filename = None
        self.__fileinfo = None
        self.__fileinfo_parsed = {}
        self.__position = 0.0
        if not self.__process:
            return
        self.__process.send('q')
        self.__process.terminate(force=True)
    
    def time_pos(self):
        if not self.__process:
            return 0.0
        return self.__position
    
    def percent_pos(self):
        try:
            return int(self.__position / self.length() * 100)
            if not self.__process:
                raise
        except:
            return 0
    
    def filename(self):
        if not self.__process or not self.__filename:
            return None
        return path.basename(str(self.__filename))
    
    def length(self):
        if not self.__process:
            return 0.0
        self.__fileinfo_parsed["duration"] = self.__parse_duration(self.__fileinfo)
        return self.__fileinfo_parsed.get("duration", None)
    
    def __get_fileinfo(self, filename):
        (r,o) = self.__execute_shell("{ep} -i {f}".format(ep=self.exec_path, f=filename))  # @UnusedVariable
        return o if r == 0 else None
        
    def __parse_duration(self, fileinfo):
        duration_rexp = compile(r"((.|\n)*)(Duration:) (\d+:\d+:\d+.\d+)")
        m = duration_rexp.match(fileinfo)
        p = m.group(4).split(":")
        return float(p[0]) * 3600 + float(p[1]) * 60 + float(p[2])

    def __get_position(self):
        status_rexp = compile(b"M:\s*([\d.]+)\s*V:.*")
        done_rexp = compile(b"have a nice day.*")
        fileprop_rexp = compile(b".*audio streams (\d+) video streams (\d+) chapters (\d+) subtitles (\d+).*")
        videoprop_rexp = compile(b".*Video codec ([\w-]+) width (\d+) height (\d+) profile (\d+) fps ([\d.]+).*")
        audioprop_rexp = compile(b"Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*")
        while self.__process.isalive():
            try:
                index = self.__process.expect(pattern=[status_rexp, done_rexp, fileprop_rexp, videoprop_rexp, audioprop_rexp], timeout=5)
                if index == 1: 
                    self.stop()
                    break
                elif index == 0:
                    self.__position = float(self.__process.match.group(1)) / 1000000
            except EOF: #OMX hanged
                self.stop()
                break
            except TIMEOUT: #OMX hanged
                self.stop()
                break
            
            sleep(0.15)
            
    def __execute_shell(self, cli):
        popen_cli = filter(lambda x : True if len(x) > 0 else False, cli.split(" "))
        process = Popen(popen_cli, stdout=PIPE, stderr=STDOUT, cwd=getcwd())
        out, err = process.communicate()
        return (process.returncode, out.decode('utf-8'))
