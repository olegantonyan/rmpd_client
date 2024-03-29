define release =
    DESTINATION=./rmpd_client
    SOURCE=.
    rm -rf $DESTINATION
    rsync -av --exclude='.git' --exclude='rmpd_client' --exclude='doc/' --exclude='.settings/' --exclude='tmp/' --exclude='.idea' $SOURCE $DESTINATION
    find $DESTINATION -name __pycache__ -type d -print0 | xargs -0 rm -r --
    find $DESTINATION -name '*.db3' -print0 | xargs -0 rm -r --
    find $DESTINATION -name 'statefile' -print0 | xargs -0 rm -r --
    find $DESTINATION -name 'encrypt_passwords.py' -print0 | xargs -0 rm -r --
    find $DESTINATION -name '*.conf' -print0 | xargs -0 rm -r --
    find $DESTINATION -name 'watchdogfile' -print0 | xargs -0 rm -r --
    find $DESTINATION -name '.project' -print0 | xargs -0 rm -r --
    find $DESTINATION -name '.pydevproject' -print0 | xargs -0 rm -r --
    find $DESTINATION -name '.gitignore' -print0 | xargs -0 rm -r --
    find $DESTINATION -name '*.pyc' -print0 | xargs -0 rm -r --
    find $DESTINATION -name Makefile -print0 | xargs -0 rm -r --
    VERSION=$(python3 -c 'import version; print(version.VERSION)')
    echo $VERSION
    tar -czvf rmpd-client-$VERSION.sa.tar.gz -C $DESTINATION .
    rm -rf $DESTINATION
endef

define prepare_dist =
    DESTINATION=./rmpd_client
    SOURCE=.
    rm -rf $DESTINATION
    rsync -av --exclude='.git' --exclude='rmpd_client' --exclude='doc/' --exclude='.settings/' --exclude='tmp/' --exclude='.idea' $SOURCE $DESTINATION
    find $DESTINATION -name __pycache__ -type d -print0 | xargs -0 rm -r --
    find $DESTINATION -name '*.db3' -print0 | xargs -0 rm -r --
    find $DESTINATION -name 'statefile' -print0 | xargs -0 rm -r --
    find $DESTINATION -name 'encrypt_passwords.py' -print0 | xargs -0 rm -r --
    find $DESTINATION -name '*.conf' -print0 | xargs -0 rm -r --
    find $DESTINATION -name 'watchdogfile' -print0 | xargs -0 rm -r --
    find $DESTINATION -name '.project' -print0 | xargs -0 rm -r --
    find $DESTINATION -name '.pydevproject' -print0 | xargs -0 rm -r --
    find $DESTINATION -name '.gitignore' -print0 | xargs -0 rm -r --
    find $DESTINATION -name '*.pyc' -print0 | xargs -0 rm -r --
    find $DESTINATION -name Makefile -print0 | xargs -0 rm -r --
    VERSION=$(python3 -c 'import version; print(version.VERSION)')
    echo $VERSION
    tar -czvf rmpd-client-$VERSION.tar.gz $DESTINATION
    rm -rf $DESTINATION
endef

release: ; $(value release)

prepare_dist: ; $(value prepare_dist)

.ONESHELL: