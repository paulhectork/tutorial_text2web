#!/bin/bash

root=$(pwd)
utils="$root/utils"
output="$root/output"
input="$root/input"
git="$utils/1_OutputData"

echo "début de l'installation..."

# delete all outputs that could exist
for f in $output/*; do
  if [[ -f $f ]]; then
    rm "$f"
  fi
done

# delete source git
if [[ -d $git ]]; then
  rm -rf $git
fi

# check if any sources are missing; if they are, delete them
if [[ ! -d $utils/static ]] || [[ ! -f "${utils}/catalog_web_skeleton.html" ]] || [[ ! -f "${utils}/to_text.py" ]]; then
  echo "script incomplet. vous devriez réinstaller les sources depuis le dépôt git."
  exit 1
fi

# check that there's not aldready a virtualenv
for dir in ./*/; do
  if [[ -f $dir/bin/activate ]]; then
    echo "un environnement existe déjà dans ce dossier. veuillez le supprimer pour continuer l'installation automatique."
    exit 1
  fi
done

# if all is fine, begin the process
# create a virtualenv
python3 -m venv env_tutoriel
source env_tutoriel/bin/activate
pip install -r requirements.txt

# if there's no input source text, clone the source git and run the raw text building script
if [[ ! -f $input/source.txt ]]; then
  cd $utils
  git clone https://github.com/katabase/1_OutputData.git && python to_text.py
  cd $root
fi

# delete source git
if [[ -d $git ]]; then
  rm -rf $git
fi

echo "installation terminée avec succès !"
