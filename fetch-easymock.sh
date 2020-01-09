#!/bin/sh
VERSION=2.5.2
svn export https://easymock.svn.sourceforge.net/svnroot/easymock/tags/easymock-$VERSION/ easymock
tar -czf easymock-$VERSION.tgz easymock