#!/usr/bin/env ruby
#
# 'ls' as a tree, e.g.
#
# % ls_tree     #
# % ls_tree .   # Same as above
#  [suess]
#   lorax.txt
#  [websockets]
#   [websockets/client]
#    client.php
#    socket.js
#   readme.txt
#   [websockets/server]
#    socket.class.php
#    socketWebSocket.class.php
#    socketWebSocketTrigger.class.php
#    startDaemon.php
#

class FileTree
  
  def main(argv)
    files = argv.empty? ? ['.'] : argv
    files.each do |f|
      process f
    end
  end
  
  def process(f)
    def munge(s)
      s.gsub /^\.+\//,''
    end
    def loop(f,indent)
      Dir[File.join f,'*'].each do |ff|
        n = File.directory?(ff) ? '[' + munge(ff) + ']' : File.basename(ff)
        puts ' '*indent + n
        loop ff,indent+1 if File.directory? ff
      end
    end
    loop f,0
  end

end

FileTree.new.main ARGV
