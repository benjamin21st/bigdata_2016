#!/bin/bash
echo "This is a Mac specific setting up script. You will see a SUCCESS indicator if each of the following steps succeeded."

setupVirtualEnv(){
    echo "Step1: Setting up virtual environment"
    virtualenv env
    source env/bin/activate	
    echo "virtual environment setup succeeded"
    echo "env" >> .gitignore
    echo "*.pyc" >> .gitignore 
    echo "*~" >> .gitignore
}

installFlask(){
    echo "Step 2: Installing flask ... "
    pip install flask
    echo ""
    pip freeze > requirement.txt
    echo "The installed modules will be in the requirement.txt file"
    echo ""
}

setupDirs(){
    mkdir server 
    mkdir server/models server/views
}

createBasicFiles(){
    touch server/models/models.py
    touch server/views/views.py
    touch server/app.py
    touch index.html
}

writeBasicFunc(){
    # TODO: check how to inject code into a blob first
    echo "from flask import Flask" >> server/app.py
    echo "" >> server/app.py
    echo "app = Flask(__name__)" >> server/app.py 
    echo "@app.route('/')" >> server/app.py
    echo "def index():" >> server/app.py
    echo "    return 'OMG, it worked!'" >> server/app.py
    echo "" >> server/app.py
    echo "" >> server/app.py
    echo "if __name__ == '__main__':" >> server/app.py
    echo "    app.run(debug=True)"  >> server/app.py
}


if [ "$1" = "init" ]
then
    echo "Initliazing new flask project"
    setupVirtualEnv
    installFlask
fi


if [ "$2" = "full" ] 
then
    echo "==> Creating directories for basic Flask appliction set up"
    setupDirs
    createBasicFiles
    echo ""
    echo "==> Finished setting up directories and dummy files."
    echo ""
    writeBasicFunc
    echo "==> Finished compsoing basic functions, try running app.py with"
    echo ">    python server/app.py"
    echo ""
    echo "Default port is 5000, make sure this port is available. Or you can manually update it later on"
else
    echo "==>No additional operations specified, ending ..."
    echo ""
fi

# exit $?
